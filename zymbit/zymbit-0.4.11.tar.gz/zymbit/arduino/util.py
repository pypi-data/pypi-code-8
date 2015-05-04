from zymbit.util import *


def get_distro():
    if os.path.exists('/etc/linino'):
        return 'linino'
