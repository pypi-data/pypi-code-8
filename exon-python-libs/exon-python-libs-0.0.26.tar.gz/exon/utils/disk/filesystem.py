__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import os
import re
from exon.utils.fileutils import readfileAsArray, writefileFromArray
from exon.utils.command import exec as run
from exon.utils.disk.lvm import LVM
from exon.utils.disk.mdadm import Mdadm, MdDevice
import psutil
import memcache
import uuid

class FilesytemException(Exception):
    pass

class MountPoint(object):

    _IGNORE_FSTYPE = (
        'proc',
        'sys',
        'dev',
        'run',
        'securityfs',
        'tmpfs',
        'devpts',
        'tmpfs',
        'cgroup',
        'pstore',
        'cgroup',
        'cgroup',
        'cgroup',
        'cgroup',
        'cgroup',
        'cgroup',
        'cgroup',
        'systemd-1',
        'mqueue',
        'tmpfs',
        'hugetlbfs',
        'debugfs',
        'configfs',
        'fusectl',
    )

    @classmethod
    def parseFstabStrin(cls, string):
        """
        Parse a string form /etc/fstab
        :param string: fstab sting
        :return: MountPoint object
        """
        data = re.split('\s+', string)
        if len(data) == 6:
            if data[1] == "none":
                data[1] = None
            return cls(
                source=data[0],
                mountpoint=data[1],
                type=data[2],
                options=data[3],
                dump=int(data[4]),
                fsck=int(data[5]),
                fstab=True
            )

    @classmethod
    def parseProcMountString(cls, string):
        """
        Parse a string from /proc/mounts
        :param string: mounts sting
        :return: MountPoint object
        """
        data = re.split('\s+', string)
        if len(data) >= 6 and data[0] not in cls._IGNORE_FSTYPE:
            if data[2].startswith("fuse"):
                temp = data[2].split(".")
                if temp != None and len(temp) >= 1:
                    data[0] = '%s#%s' % (temp[1], data[0])
            return cls(
                source=data[0],
                mountpoint=data[1],
                type=data[2],
                options=data[3],
                dump=int(data[4]),
                fsck=int(data[5]),
                fstab=False
            )


    def __init__(self, source = None, mountpoint = None, type = None, options = None, dump = 0, fsck = 0, fstab = False):
        self.sourceDevice = source
        if source.lower().startswith("uuid="):
            t = source.split("=")
            if len(t) >= 2:
                out = run("blkid -U %s" % t[1])
                if out.rc == 0 and len(out.stdout) >= 1:
                    self.sourceDevice = out.stdout[0].strip()
        elif source.lower().startswith('lable='):
            t = source.split("=")
            if len(t) >= 2:
                out = run("blkid -L %s" % t[1])
                if out.rc == 0 and len(out.stdout) >= 1:
                    self.sourceDevice = out.stdout[0].strip()
        self.source = source
        self.mountpoint = mountpoint
        self.type = type
        self.options = options
        self.dump = dump
        self.fsck = fsck
        self.fstab = fstab
        self.uuid = Filesystems.getUuid(self.sourceDevice)
        if self.mountpoint != None:
            size = psutil.disk_usage(self.mountpoint)
            self.size = size.total
            self.free = size.free
        else:
            self.size = None
            self.free = None

    def __eq__(self, other):
        if type(other) != MountPoint:
            return False
        if self.uuid == other.uuid:
            return True
        if self.source == other.source:
            return True
        elif self.sourceDevice == other.source:
            return True
        return False

    def toFstabString(self):
        return "%s\t%s\t%s\t%s\t%s %s" % (self.source, self.mountpoint, self.type, self.options, self.dump, self.fsck)

    def __repr__(self):
        s = self.source
        if self.sourceDevice != None and self.sourceDevice != self.source:
            s = '%s (%s)' % (self.source, self.sourceDevice)
        return "{Source: %s Mountpoint: %s Type: %s Options: %s Dump: %d Fsck: %d Fstab: %r}" %\
               (s, self.mountpoint, self.type, self.options, self.dump, self.fsck, self.fstab)

class Filesystems(object):
    """
    Class for handling Linux filesystems
    """

    SUPPORTED_FILESYSTEMS = (
        'ext4', 'ext3', 'ext2', 'xfs', 'btrfs',
    )

    _UUID = {}
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    def __init__(self):
        self.refresh()

    def findByDevice(self, device):
        self.refresh()
        out = run("lsblk -p -o name -n %s" % device)
        ret = []
        if out.rc == 0:
            dev = out.stdout[0]
            print(out.stdout)
            for f in self.fs:
                print(f.sourceDevice)
                if f.sourceDevice == dev:
                    ret.append(f)
        return ret
    def refresh(self):
        """
        Refresh all filesystems
        :return:
        """
        self.fs = []
        self._readFstab()
        self._readMounts()

    def _readFstab(self):
        """
        Reads all fstab entrys
        :return:
        """
        for line in readfileAsArray(os.path.join('/','etc','fstab')):
            line = line.strip()
            if not line.startswith("#") and line != '':
                tmp = MountPoint.parseFstabStrin(line)
                if tmp != None:
                    self.fs.append(tmp)
    def _readMounts(self):
        """
        Reads all mount points
        :return:
        """
        for line in readfileAsArray(os.path.join('/','proc','mounts')):
            line = line.strip()
            temp = MountPoint.parseProcMountString(line)
            if temp not in self.fs and temp != None:
                self.fs.append(temp)

    def getByUUUID(self, uuid):
        """"
        return a MountPoint by it's UUID
        :param uuid: uuid for a filesystem
        :return: a MountPoint object
        """
        for fs in self.fs:
            if fs.uuid == uuid:
                return fs

    def getByDevice(self, device):
        """
        return a MountPoint by it's device
        :param device: device of a filesystem
        :return: a MountPoint object
        """
        for fs in self.fs:
            if fs.source == device:
                return fs

    def getBySourceDevice(self, device):
        """
        return a MountPoint by it's source device
        :param device: source device of a filesystem
        :return: a MountPoint object
        """
        for fs in self.fs:
            if fs.sourceDevice == device:
                return fs

    def _appendFs(self, line):
        """
        Adds a new device to fstab
        :param line:
        :return:
        """
        fstabFile = os.path.join('/','etc','fstab')
        fstab = readfileAsArray(fstabFile)
        fstab.append(line)
        writefileFromArray(fstabFile, fstab)

    def _edditFs(self, fs):
        """
        edits a fs in fstab
        :param fs:
        :return:
        """
        fstabFile = os.path.join('/','etc','fstab')
        fs.fstab = True
        for i in range(0, len(self.fs) - 1):
            f = self.fs[i]
            if f.uuid == fs.uuid:
                self.fs[i] = fs
        newFstab = []
        for line in readfileAsArray(fstabFile):
            if line.startswith('#'):
                newFstab.append(line)
            else:
                t = MountPoint.parseFstabStrin(line)
                if t != fs:
                    newFstab.append(line)
                else:
                    newFstab.append(fs.toFstabString())
        writefileFromArray(fstabFile, newFstab)

    def addToFstab(self, device = None, mountpoint = None, type=None, options = None, dump = None, fsck = None, useUuid=False):
        """
        Add a device to the fstab
        :param device: device file
        :param mountpoint: the mountpoint
        :param type: the filesystem type
        :param options: options for the mount
        :param dump: should device used with dump
        :param fsck: fsck position
        :param useUuid: should uuid be used to mount the device
        :return: if successful
        """
        if device == None:
            raise FilesytemException("device must not be null")
        if mountpoint == None:
            raise FilesytemException("mountpoin must not be null")
        if type == None:
            raise FilesytemException("type must not be null")
        uuid = None
        if useUuid:
            uuid = Filesystems.getUuid(device, generate=False)
            if uuid != None:
                device='UUID=%s' % uuid
            elif device.startswith("UUID="):
                t = device.split("=")
                uuid = t[1]
        fstab = None
        if useUuid:
            fstab = self.getByUUUID(uuid)
        elif device.startswith("UUID"):
            fstab = self.getByDevice(device)
            print(fstab)
        elif device.startswith("LABLE"):
            fstab = self.getByDevice(device)
        else:
            fstab = self.getBySourceDevice(device)

        if not os.path.isdir(mountpoint):
            os.makedirs(mountpoint)

        if fstab == None:
            if options == None:
                options = "defaults"
            if dump == None:
                dump = "0"
            if fsck == None:
                fsck = "0"
            return self._appendFs("%s\t%s\t%s\t%s\t%s %s" % (device, mountpoint, type, options, dump, fsck))
        else:
            if useUuid:
                if fstab.source != device:
                    fstab.source = device
            if options != None:
                fstab.options = options
            if type != None:
                fstab.type = type
            if dump != None:
                fstab.dump = dump
            if fsck != None:
                fstab.fsck = fsck
            return self._edditFs(fstab)

    def _isRaid(self, device):
        """
        Checks if device is a raid device
        :param device:
        :return: raid device if is raid
        """
        outType = run("lsblk -ln -o NAME,TYPE %s" % device)
        if outType.rc == 0:
            if len(outType.stdout)>=0:
                data = re.split('\s+', outType.stdout[0].strip())
                if len(data) >= 2:
                    devName = data[0]
                    devType = data[1]
                    if devType == "lvm":
                        a = devName.split("-")
                        if len(a) >= 1:
                            vg = a[0]
                            lvm = LVM()
                            pvs = lvm.getPhysicalVolume()
                            for pv in pvs:
                                if pvs[pv] == vg:
                                    return self._isRaid(pv)
                    elif devType.startswith("raid"):
                        return device
        return False


    def formatDisk(self, device=None, type=None):
        """
        Formats a disk with a supported filesystem
        :param device:
        :param type:
        :return:
        """
        if device == None:
            raise FilesytemException("device must not be null")
        if type == None:
            raise FilesytemException("type must not be null")
        if type not in Filesystems.SUPPORTED_FILESYSTEMS:
            raise FilesytemException("fs type %s is not supported. Supported types are %s" % (type, Filesystems.SUPPORTED_FILESYSTEMS))
        raid = self._isRaid(device)
        options = ""
        if raid:
            mdadm = Mdadm()
            md = mdadm.getDevice(device=raid)
            level = md.level
            chunksize = md.chunkSize.lower()
            numDevs = md.numDevices
            if int(level) == 5:
                numDevs = int(numDevs) - 1
            if chunksize.endswith("k"):
                chunksize = chunksize.replace("k","")
            stride = int(int(chunksize)/4)
            strideWidth = int(int(numDevs)*stride)
            if type.startswith("ext"):
                options = " -b 4096 -E stride=%d,stripe-width=%d" % (stride, strideWidth)
            if type.startswith("xfs"):
                options = " -d su=%s -d sw=%s" % (md.chunkSize.lower(), numDevs)
        mkfs = 'mkfs.%s%s %s' % (type, options, device)
        out = run(mkfs)
        if out.rc == 0:
            return True
        else:
            raise FilesytemException("error while formation %s. STDOUT: %s STDERR: %s CMD: %s" % (device, out.stdout, out.stderr, mkfs))


    @classmethod
    def getUuid(cls, dev, generate=True):
        """
        Get or generate a uuid for a device
        :param dev: Device String
        :param generate: set if a uuid should be generated
        :return: uuid for device
        """
        if dev in cls._UUID:
            return cls._UUID[dev]
        out = run("blkid -s UUID")
        if out.rc == 0:
            regex = re.compile('(.+?):\s*?UUID="(.+?)"')
            for line in out.stdout:
                m = regex.search(line)
                if m and len(m.groups()) == 2:
                    cls._UUID[m.group(1)] = m.group(2)
        if dev in cls._UUID:
            return cls._UUID[dev]
        out2 = run("blkid -s UUID %s" % dev)
        if out2.rc == 0:
            regex = re.compile('(.+?):\s*?UUID="(.+?)"')
            for line in out2.stdout:
                m = regex.search(line)
                if m and len(m.groups()) == 2:
                    cls._UUID[m.group(1)] = m.group(2)
        if generate:
            id = cls.mc.get("sdf")
            if id == None:
                id = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'exon-api-fs'))
                cls.mc.set(dev, id)
            return id
        else:
            return None

if __name__ == "__main__":
    f = Filesystems()
    print(f.findByDevice(device="/dev/rootvg/rootlv"))
    print(f.addToFstab(device='/dev/test', mountpoint='/mnt/test', type='ext4'))