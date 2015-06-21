import subprocess
import struct
import sys


class HitchEnvironmentException(Exception):
    pass

def class_definition():
    sys.stdout.write(
        """hitchenvironment.Environment(platform="{}", systembits={}, requires_internet_access={})\n""".format(
            platform(), systembits(), has_internet()
        )
    )
    sys.stdout.flush()

def systembits():
    return struct.calcsize("P") * 8

def has_internet():
    return 0 == subprocess.call(
        ["ping", "8.8.8.8"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def platform():
    return sys.platform

class Environment(object):
    def __init__(self, platform, systembits, requires_internet_access):
        self.platform = platform
        self.systembits = systembits
        self.requires_internet_access = requires_internet_access

    def match(self):
        if systembits() != self.systembits:
            raise HitchEnvironmentException(
                "Specified environment is a {} bit system. This is a {} bit system.".format(
                    self.systembits, systembits()
                )
            )

        if platform() != self.platform:
            raise HitchEnvironmentException(
                "Specified environment is a '{}', but this platform is '{}'".format(
                    self.platform, platform()
                )
            )

        if self.requires_internet_access and not has_internet():
            raise HitchEnvironmentException(
                "No internet detected. This environment was configured to require internet access."
            )
