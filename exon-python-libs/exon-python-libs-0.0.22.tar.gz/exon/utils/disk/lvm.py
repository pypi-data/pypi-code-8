__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from exon.utils.command.execute import exec as execute
import os.path

class LVMVolumeGroupError(Exception):
    pass
class LVMLogicalVolumeError(Exception):
    pass

class LVM:

    def __init__(self):
        self._vg = {}
        self._pv = {}
        self._lv = {}

    def getPhysicalVolume(self):
        """
        Retruns all Physical Volumes with the Volume Group
        :return: hash of Physical Volumes
        """
        outPv = execute("pvdisplay -C -o pv_name,vg_name --noheading --separator :")
        if outPv.rc == 0:
            for line in outPv.stdout:
                line = line.strip()
                if line != "":
                    a = line.split(":")
                    if len(a) >= 2:
                        self._pv[a[0]] = a[1]
        return self._pv

    def getVolumeGroup(self):
        """
        Returns all Volume Groups with pv,name,uuid,size and free space
        :return: has of Volume Groups
        """
        outVgdisply = execute("vgdisplay -C -o vg_name,vg_uuid,vg_size,vg_free --units b --separator : --noheadings --nosuffix")
        if outVgdisply.rc == 0:
            for line in outVgdisply.stdout:
                line = line.strip()
                if line != "":
                    a = line.split(":")
                    if len(a) >= 4:
                        self._vg[a[0]] = {}
                        self._vg[a[0]]["name"] = a[0]
                        self._vg[a[0]]["uuid"] = a[1]
                        self._vg[a[0]]["size"] = a[2]
                        self._vg[a[0]]["free"] = a[3]
        self.getPhysicalVolume()
        for key in self._pv:
            if self._pv[key] in self._vg:
                self._vg[self._pv[key]]["pv"] = key

        return self._vg

    def createVolumeGroup(self, name = None, device = None):
        """
        Creates a volume group.
        If device is only a name it will be renamed as /dev/device
        If device is not a physical volume it will be created
        :param name: Name of the volume group
        :param device: Device for the volume group
        :return: the detail data for the lvm
        """
        if not os.path.exists(device):
            device = os.path.join('/', 'dev', device)
        if not os.path.exists(device):
            raise LVMVolumeGroupError("Device %s do not exist" % device)
        if name in self.getVolumeGroup():
            raise LVMVolumeGroupError("Volume Group %s already exists" % name)
        if device in self.getPhysicalVolume() and self._pv[device] != "":
            raise LVMVolumeGroupError("Device %s is already in a volume group" % device)
        if not device in self._pv:
            outPvcreate = execute("pvcreate %s" % device)
            if outPvcreate.rc  != 0:
                raise LVMVolumeGroupError("Error creating physical volume %s. STDOUT: %s STDERR: %s" (device, outPvcreate.stdout, outPvcreate.stderr))
        outVgcreate = execute("vgcreate %s %s" % (name, device))
        if outVgcreate.rc  != 0:
            raise LVMVolumeGroupError("Error creating volume group %s. STDOUT: %s STDERR: %s" (name, outVgcreate.stdout, outVgcreate.stderr))
        vg = self.getVolumeGroup()
        if name in vg:
            return vg[name]
        else:
            raise LVMVolumeGroupError("Error creating volume volume %s." % name)

    def deleteVolumeGroup(self, name = None):
        vg = self.getVolumeGroup()
        if not name in vg:
            raise LVMVolumeGroupError("Volume group %s not found")
        pv = vg[name]["pv"]
        outVg = execute("vgremove %s" % name)
        if outVg.rc  != 0:
            raise LVMVolumeGroupError("Error deleting volume group %s. STDOUT: %s STDERR: %s" (name, outVg.stdout, outVg.stderr))
        outPv = execute("pvremove %s" % pv)
        if outPv.rc  != 0:
            raise LVMVolumeGroupError("Error deleting physical volum %s. STDOUT: %s STDERR: %s" (name, outPv.stdout, outPv.stderr))
        return True

    def getLogicalVolumes(self, vg=None):
        """
        Returns a list of all Logical Volumes. If vg is set only the lv's of that vg are retrurned
        :param vg: Volume group name
        :return: a hash of lv's
        """
        outCmd = execute("lvdisplay -C -o lv_name,vg_name,lv_uuid,lv_path,lv_size --noheading --separator : --units b --nosuffix")
        if outCmd.rc == 0:
            for line in outCmd.stdout:
                line = line.strip()
                if line != "":
                    a = line.split(":")
                    if len(a) >= 5:
                        self._lv[a[0]] = {
                            "name": a[0],
                            "vg": a[1],
                            "uuid": a[2],
                            "path": a[3],
                            "size": a[4],
                        }
        if vg == None:
            return self._lv
        else:
            return {l: self._lv[l] for l in self._lv if self._lv[l]["vg"] == vg}

    def createLogicalVolume(self, name=None, vg=None, size=None):
        """
        creates or extends a logical volume
        :param name: name of the logical volume
        :param vg: name of the volume group
        :param size: size of the logical volume in bytes (must be a multiple of 512)
        :return: the detail infos for the lv
        """
        if name == None:
            raise LVMLogicalVolumeError("Can not create Logical Volume without name")
        if vg == None:
            raise LVMLogicalVolumeError("Can not create Logical Volume without volume group")
        if size == None:
            raise LVMLogicalVolumeError("Can not create Logical Volume without size")
        vgs = self.getVolumeGroup()
        if vg not in vgs:
            raise LVMLogicalVolumeError("Volume Group do not exists")
        free = int(vgs[vg]["free"])
        extend = False
        if type(size) == str and size.startswith("+"):
            size = "".join(size[1:])
            extend = True
        size = int(size)
        if size > free:
            raise LVMLogicalVolumeError("Can not create logical volume with size %dB when on volume group only %dB are free" % (size, free))
        lvs = self.getLogicalVolumes(vg)
        if extend:
            size = "+%sb" % size
        else:
            size = "%sb" % size
        lvcmd = "lvcreate -n %s -L %s %s" % (name, size, vg)
        if name in lvs:
            lvcmd = "lvextend -L %s %s" % (size, lvs[name]["path"])
        out = execute(lvcmd)
        if out.rc != 0:
            raise LVMLogicalVolumeError("Error createing logical volume. STDOUT: %s STDERR: %s" % (out.stdout, out.stderr))
        lvs = self.getLogicalVolumes(vg)
        if name in lvs:
            return lvs[name]
        raise  LVMLogicalVolumeError("Logical Volume could not be created")

    def deleteLogicalVolume(self, name=None, vg=None):
        """
        deletes a logical volume
        :param name: name of the volume
        :param vg: name of the volume group
        :return:
        """
        if name == None:
            raise LVMLogicalVolumeError("Can not delete logical volume without name")
        if vg == None:
            raise LVMLogicalVolumeError("Can not delte logical volume without volume group name")
        lvs = self.getLogicalVolumes(vg = vg)
        if not name in lvs:
            raise LVMLogicalVolumeError("Logical Volume %s not found" % name)
        path = lvs[name]["path"]
        out = execute("lvremove -f %s" % path)
        if out.rc != 0:
            raise LVMLogicalVolumeError("Error deleting lv %s. STDOUT: %s STDERR: %s" % (name, out.stdout, out.stderr))
        return True

if __name__ == "__main__":
    lvm = LVM()
    print(lvm.createLogicalVolume(name = "testlv2", vg = "testvg", size=(10*1023)))
    print(lvm.createLogicalVolume(name = "testlv2", vg = "testvg", size="+%d" %(10*1024)))
    print(lvm.deleteLogicalVolume(name = "testlv2", vg = "testvg"))