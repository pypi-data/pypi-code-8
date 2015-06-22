__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import os
import re
from exon.utils.command.execute import exec as exececute
from exon.utils.fileutils import (readfile, writefile)
from exon.utils.disk.part import createPartition
import socket
from time import sleep


class MdadmCreateRaidException(Exception):
    pass

class MdadmDeleteRaidException(Exception):
    pass

class MdDevice(object):
    """
    This class representates a software raid
    """

    def __init__(self, device=None, name=None, uuid=None, metadata=None):
        self.device = device
        self.name = name
        self.uuid = uuid
        self.metadata = metadata
        self.file = os.path.basename(self.device)
        regex = re.compile('(\w+)(\d+)')
        search = regex.search(self.file)
        if search:
            r = search.groups()
            if len(r) == 2:
                self.number = int(r[1])
        self.message = {}
        self.loadDetails()

    def loadDetails(self):
        """
        Loads the details of an array
        """
        out = exececute("mdadm --detail --detail %s" % self.device)
        if out.rc == 0:
            pareseLine = False
            deviceRegex = re.compile('\d+?\s+?\d+?\s+?\d+?\s+?[\d+?,-]\s+?(.+?)\s+?(/.+)')
            for line in out.stdout:
                line = line.strip()
                if line.startswith("Raid Level"):
                    (key, level) = line.split(":")
                    self.level = (level.strip().replace("raid", ""))
                    if int(self.level) == 1:
                        self.chunkSize = "64k"
                elif line.startswith("Array Size"):
                    a = line.split(":")
                    if len(a) >= 2:
                        a2 = a[1].strip().split(" ")
                        if len(a2) >= 1:
                            self.size = int(a2[0].strip())
                elif line.startswith('Raid Devices'):
                    (key, level) = line.split(":")
                    self.numDevices = (level.strip().replace("raid", ""))
                    self.devices = []
                elif re.match('Number\s+?Major\s+?Minor\s+?RaidDevice State', line):
                    pareseLine = True
                elif line.startswith('Chunk Size'):
                    (key, level) = line.split(":")
                    self.chunkSize = (level.strip())
                elif line.startswith('State'):
                    (key, state) = line.split(":")
                    self.state = (state.strip().replace("clean", "ok"))
                    if self.state != "ok":
                        parseMessage = False
                        failRegex = re.compile(
                            '.+?re.+? =\s+?(\d+?\.\d+?%)\s+?\((\d+?\/\d+?)\)\s+?finish=(\d+?\.\d+?.+?)\s+?speed=(.+)')
                        for line in readfile("/proc/mdstat").split('\n'):
                            if line.startswith(self.file):
                                parseMessage = True
                            elif parseMessage:
                                sFail = failRegex.search(line)
                                if sFail:
                                    failGroups = sFail.groups()
                                    if len(failGroups) >= 4:
                                        self.message["recovery"] = {
                                            "percent": failGroups[0],
                                            "blocks": failGroups[1],
                                            "remainingTime": failGroups[2],
                                            "speed": failGroups[3],
                                        }
                elif pareseLine:
                    search = deviceRegex.search(line)
                    if search:
                        g = search.groups()
                        if len(g) >= 2:
                            self.devices.append({
                                "device": g[1].strip(),
                                "status": g[0].strip(),
                            })

    def __repr__(self):
        return "Device = %s, Name = %s, UUID = %s, File = %s, Number = %s" % (
        self.device, self.name, self.uuid, self.file, self.number)


class Mdadm(object):
    """
    This class handels the mdamd command for creating and managing software raids
    """

    # Supported RAID Levels
    _supportedLevels = (
        0, 1, 5,
    )

    # Chunk sizes for the RAID leves
    _chunkSizes = {
        1: 64,
        0: 64,
        5: 256,
    }

    def __init__(self):
        self.devices = []
        self._getAllDevices()
        pass

    def _getAllDevices(self):
        hostname = socket.gethostname()
        out = exececute("mdadm --detail --scan")
        if out.rc == 0:
            regex = re.compile('ARRAY (.+?)\s+metadata=(.+?)\s+name=(.+?)\s+UUID=(.+)')
            for line in out.stdout:
                if line.startswith("ARRAY"):
                    groups = regex.search(line).groups()
                    if len(groups) >= 4:
                        self.devices.append(
                            MdDevice(device=groups[0], metadata=groups[1], name=groups[2].replace("%s:" % hostname, ""),
                                     uuid=groups[3]))

    def getAllDevices(self):
        """
        Retruns all found devices
        :return: array of devices
        """
        return self.devices

    def refresh(self):
        """
        refresh the device list
        """
        self._getAllDevices()

    def nextNumber(self):
        """
        Return the nex free number for the /dev/mdx device
        :return: next free number
        """
        number = -1
        self.refresh()
        for d in self.devices:
            if hasattr(d, 'number'):
                if d.number > number:
                    number = d.number
        return (number + 1)

    def getDevice(self, name=None, device=None, uuid=None):
        """
        Find a device with the given parameter
        :param name: uses the filename for search
        :param device: uses the device for search
        :param uuid: uses the uuid for search
        :return: a Mddevice object
        """
        if name != None and device == None:
            device = "/dev/%s" % name

        if device != None:
            for d in self.devices:
                if d.device == device:
                    return d
        elif uuid != None:
            for d in self.devices:
                if d.uuid == uuid:
                    return d
        return None

    def createRaid(self, name=None, devices=[], level=None, deviceName=None, part=False):
        """
        Create a RAID device
        :param name: Name of the device
        :param devices: A Array of the devices for the raid
        :param level: The raid level
        :param deviceName: the device name of the new raid if None given the name is like md[n]
        :param part: boolean if the partitons should be reated
        :return: a MdDevice object for the newly created raid device
        """

        """
        Check the parameters
        """
        if deviceName == None:
            deviceName = "/dev/md%d" % self.nextNumber()
        if not '/dev' in deviceName:
            raise MdadmCreateRaidException("Device name %s must be in /dev" % deviceName)
        if os.path.exists(deviceName):
            raise MdadmCreateRaidException("Device %s must not exits" % deviceName)
        if devices == None or len(devices) < 2:
            raise MdadmCreateRaidException("No device for Raid given")
        if not level in Mdadm._supportedLevels:
            raise MdadmCreateRaidException(
                "Raid level %s is not supported. Supported Leves are %s" % (level, Mdadm._supportedLevels))
        if level == 5 and len(devices) < 3:
            raise MdadmCreateRaidException(
                "%d devices are to low for raid level 5. Min 3 disks are required" % len(devices))
        partExists = self._checkPart(devices)
        devices = []
        # Check if partion exists and creates he partion if part = True
        for dev in partExists:
            devices.append(dev)
            if partExists[dev] == False and part == False:
                raise MdadmCreateRaidException("Partion %s do not exist and should not be created" % dev)
            elif partExists[dev] == False and part:
                if not "/dev" in dev:
                    dev = os.path.join("/dev", dev)
                match = re.match('.+?(\d+)', dev)
                dev = dev.replace(match.groups()[0], "")
                ret = createPartition(dev, "fd00")
                if ret.rc != 0:
                    raise MdadmCreateRaidException(
                        "Canont create partion on %s. STDOUT: %s STDERR: %s" % (dev, ret.stdout, ret.stderr))
        # Check if the partions have the same size
        outSize = exececute("lsblk -o name,size -bdrpn %s" % " ".join(devices))
        if outSize.rc == 0:
            devices = {}
            oldSize = -1
            for line in outSize.stdout:
                if line != '':
                    (dev, size) = line.split(" ")
                    if oldSize == -1:
                        oldSize = int(size)
                    else:
                        minSize = float(oldSize) * 0.99
                        maxSize = float(oldSize) * 1.01
                        if float(size) < minSize or float(size) > maxSize:
                            raise MdadmCreateRaidException("Device size differs more then 1%")
                        else:
                            oldSize = int(size)
                    devices[dev] = int(size)
        # Creating the raid
        if name != None:
            name = '--name="%s" ' % name
        cmd = 'mdadm --create --verbose --level=%d %s--metadata=1.2 --chunk=%d --raid-devices=%d %s %s' % (
            level,
            name,
            Mdadm._chunkSizes[level],
            len(devices),
            deviceName,
            " ".join(devices)
        )
        out = exececute(cmd)
        if out.rc == 0:
            # Update config and assemble the array
            lines = []
            for line in readfile("/etc/mdadm.conf").split("\n"):
                if not line.startswith("ARRAY"):
                    lines.append(line)
            outScan = exececute("mdadm --detail --scan")
            if outScan.rc == 0:
                for line in outScan.stdout:
                    lines.append(line)
            writefile("/etc/mdadm.conf", '\n'.join(lines))
            outAssamble = exececute("mdadm --assemble --scan")
            self.refresh()
            return self.getDevice(device=deviceName)
        else:
            return {
                "rc": out.rc,
                "stderr": out.stderr,
                "stdout": out.stdout,
                "command": cmd,
            }

    def deviceExists(self, name=None, device=None, uuid=None):
        """
        returns if device exists or not
        :param name: uses the filename for search
        :param device: uses the device for search
        :param uuid: uses the uuid for search
        :return: device exists or not
        """
        if name != None and device == None:
            device = "/dev/%s" % name

        if device != None:
            for d in self.devices:
                if d.device == device:
                    return True
        elif uuid != None:
            for d in self.devices:
                if d.uuid == uuid:
                    return True
        return False

    def delete(self, device=None, zero=False):
        if device == None:
            raise MdadmDeleteRaidException("Device is None")
        elif type(device) != MdDevice:
            raise MdadmDeleteRaidException("Device is not of type MdDevice")
        raidDevs = []
        for dev in device.devices:
            raidDevs.append(dev["device"])
        outDel = exececute("mdadm --stop %s" % device.device)
        if outDel.rc != 0:
            raise MdadmDeleteRaidException("Cannot stop Raid. STDOUT: %s STDERR: %s" % (outDel.stdout, outDel.stderr))
        if zero:
            outZero = exececute("mdadm --zero-superblock %s" % " ".join(raidDevs))
            if outZero.rc != 0:
                raise MdadmDeleteRaidException("Cannot zero superbolocks. STDOUT: %s STDERR: %s" % (outZero.stdout, outZero.stderr))


    def _checkPart(self, devices=[]):
        ret = {}
        from os import path

        for dev in devices:
            ret[path.join('/dev', path.basename(dev))] = path.exists(path.join('/dev', path.basename(dev)))
        return ret


if __name__ == "__main__":
    mdadm = Mdadm()
    m = mdadm.getAllDevices()
    print(m)
