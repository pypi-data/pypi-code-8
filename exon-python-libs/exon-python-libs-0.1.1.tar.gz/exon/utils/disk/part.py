__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import os
from exon.utils.command.execute import exec as run

def createPartition(device, type):
    if not os.path.exists(device):
        device = '/dev/%s' % device
    parted = run('parted -s -a optimal {} mklabel gpt mkpart {} 0% 100% set 1 raid on'.format(device, type))
    return parted