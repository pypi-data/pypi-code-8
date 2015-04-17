'''methods for getting data from and controlling a virtual box'''

import subprocess
from time import sleep

import click


def vm_up(vminfo):
    '''bring up vm specified by vminfo'''
    # poweron  -  VBoxManage startvm FBSD101-32 --type sdl
    if vminfo.state == 'running':
        click.echo('<vm: "%s" - %s> is already running' % (vminfo.uuid,
                                                           vminfo.name))
        return
    up_cmd = ['VBoxManage', 'startvm', vminfo.uuid,
              '--type', vminfo.drift['display']]
    try:
        _ = subprocess.check_output(up_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        click.echo('Failed to poweron <vm: "%s" - %s>' % (vminfo.name,
                                                          vminfo.uuid))
        return

    while vminfo.state != 'running':
        sleep(1)
        vminfo = VMInfo(vminfo.uuid)
    click.echo('<vm: "%s" - %s> is up' % (vminfo.uuid, vminfo.name))
    return vminfo


def vm_down(vminfo):
    '''shutdown vm specified by vminfo by sending acpipowerbutton'''
    # poweroff -  VBoxManage controlvm FBSD101-32 acpipowerbutton
    if vminfo.state == 'poweroff':
        click.echo('<vm: "%s" - %s> is not running' % (vminfo.uuid,
                                                       vminfo.name))
        return
    down_cmd = ['VBoxManage', 'controlvm', vminfo.uuid, 'acpipowerbutton']
    try:
        _ = subprocess.check_output(down_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        click.echo('Failed to poweroff <vm: "%s" - %s>' % (vminfo.name,
                                                           vminfo.uuid))
        return
    while vminfo.state != 'poweroff':
        # print vminfo.state
        sleep(1)
        try:
            vminfo = VMInfo(vminfo.uuid)
        except subprocess.CalledProcessError:
            pass
    click.echo('<vm: "%s" - %s> is down' % (vminfo.uuid, vminfo.name))
    return vminfo


def get_available_vms():
    '''return a catalog of all available vms'''
    avms = {}
    cmd = ['VBoxManage', 'list', 'vms']
    rslt = subprocess.check_output(cmd).strip()
    # print rslt
    for ln in rslt.split('\n'):
        name, uuid = ln.split('{')
        uuid = uuid.replace('}', '')
        avms[uuid] = VMInfo(uuid)
    return avms


class VMInfo(object):
    def __init__(self, uuid, config=None):
        els = []
        cmd = ['VBoxManage', 'showvminfo', uuid, '--machinereadable']
        rslt = subprocess.check_output(cmd).strip()
        for bit in rslt.split('\n'):
            ky, vl = bit.split('=')
            els.append((ky, vl.replace('"', '')))
        self.info = dict(els)
        self.name = self.info['name']
        self.uuid = self.info['UUID']
        self.state = self.info['VMState']
        self.drift = config

    def __repr__(self):
        return '<VMinfo %s>' % self.uuid
