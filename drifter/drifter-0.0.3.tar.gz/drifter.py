from collections import OrderedDict
import os
import sys
# import posixpath

import click
import yaml

import virtualbox as vbx

#
# drifter add <vboxname>  - adds another vm to drift.yaml
# drifter rm <vboxname>   - removes a vm from the drift.yaml
#
# drifter up              - starts up the vm's from the drift.yaml
# drifter down            - shutdown the vm's from drift.yaml
#
# drifter list            - lists the vm's from drift.yaml


class Drift(object):
    '''context object for sharing settings between commands'''
    def __init__(self, home, drifter_vms, available_vms):
        self.home = home
        self.available_vms = available_vms
        self.drifter_vms = OrderedDict()
        self.drifter_raw = drifter_vms
        for vm in drifter_vms:
            try:
                self.drifter_vms[vm['uuid']] = self.available_vms[vm['uuid']]
                # print vm
                self.drifter_vms[vm['uuid']].drift = vm
                self.available_vms[vm['uuid']].drift = vm
            except KeyError:
                vm_uuid_not_found(vm['name'], vm['uuid'], exit_code=0)

        self.verbose = False

    def __repr__(self):
        return '<Drift %r>' % self.home

    @staticmethod
    def load_drifterfile(fpath):
        try:
            with open(fpath) as hdrift:
                cfg = yaml.safe_load(hdrift.read())
        except IOError:
            cfg = []
        return cfg

    def save(self):
        '''persist the vm configs back to the Drifterfile'''
        # to_write = []
        # for vm in self.drifter_vms.values():
        #     to_write.append(vm.drift)

        with file(self.home, 'w') as hdrift:
            hdrift.write(stanza())
            yaml.safe_dump(self.drifter_raw, hdrift, default_flow_style=False)

    def get_uuid(self, name):
        '''given a vm name return the VMInfo object or raise VMNotFound'''
        for uuid, vminfo in self.available_vms.iteritems():
            if vminfo.name == name:
                return uuid
        vm_name_not_found(name)

    def get_vminfo(self, uuid):
        '''return the vminfo for the uuid or raise VMNotFound'''
        try:
            return self.available_vms[uuid]
        except:
            raise VMNotFound(uuid)

    def remove(self, name):
        self.drifter_raw = [v for v in self.drifter_raw if v['name'] != name]
        # for raw in self.drifter_raw:
        #     if raw['name'] == name:
        # uuid = self.get_uuid(name)
        # del(self.drifter_vms[uuid])
        # vminfo = self.get_vminfo(uuid)
        # # print vminfo.drift
        # if vminfo.drift is not None:
        #     vminfo.drift = None
        #     self.available_vms[uuid] = vminfo
        # else:
        #     vm_not_found(vminfo)


pass_drift = click.make_pass_decorator(Drift)


@click.group()
@click.option('--drifter-home', envvar='DRIFTER_HOME', default='Drifterfile',
              metavar='PATH',
              help='specify the Drifterfile config to use. (Drifterfile)')
@click.option('--verbose', '-v', is_flag=True,
              help='Enables verbose mode.')
@click.version_option('0.0.3')
@click.pass_context
def cli(ctx, drifter_home, verbose):
    """Drifter is a command line tool that can up/down specified VirtualBox vms.
    """
    # Create a repo object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_drift decorator.
    drifterfile_path = os.path.abspath(drifter_home)
    ctx.obj = Drift(home=drifterfile_path,
                    drifter_vms=Drift.load_drifterfile(drifterfile_path),
                    available_vms=vbx.get_available_vms())
    ctx.obj.verbose = verbose


@cli.command()
@click.option('--display', '-d', default='gui',
              type=click.Choice(['gui', 'sdl', 'headless']),
              help='default: gui')
@click.argument('name')
@pass_drift
def add(drift, name, display):
    """adds a named vm to your Drifterfile
    """
    uuid = drift.get_uuid(name)
    vminfo = drift.get_vminfo(uuid)
    # print vminfo.drift
    if vminfo.drift is None:
        cfg = {'name': name,
               'display': display,
               'provider': 'virtualbox',
               'uuid': uuid}
        vminfo.drift = cfg
        drift.drifter_raw.append(cfg)
        drift.save()
    else:
        vm_already_exists(vminfo)


@cli.command()
@click.argument('name')
@pass_drift
def remove(drift, name):
    """removes a named vm from your Drifterfile
    """
    drift.remove(name)
    drift.save()


@cli.command()
@click.option('--all', '-a', default=False, is_flag=True,
              help='List all available vms')
@pass_drift
def list(drift, all):
    """list vms in Drifterfile"""
    if all:
        the_vms = drift.available_vms
    else:
        the_vms = drift.drifter_vms

    for vm in the_vms.values():
        click.echo('<vm: "%s" - %s>' % (vm.name, vm.uuid))


@cli.command()
@pass_drift
def down(drift):
    """Downs vms, in reverse order, by sending an acipshutdown event to vms
    in Drifterfile
    """
    for vminfo in reversed(drift.drifter_vms.values()):
        if vminfo.drift is not None:
            vbx.vm_down(vminfo)


@cli.command()
@pass_drift
def up(drift):
    """Bring up vms in Drifterfile, in order
    """
    for vminfo in drift.drifter_vms.values():
        if vminfo.drift is not None:
            vbx.vm_up(vminfo)


def stanza():
    return '''# All Drift configuration is done below.

# The most common configuration options are documented and commented below.
# For a complete reference, please see the online documentation at
# http://drifter.readthedocs.org/ .

'''


class VMNotFound(Exception):
    pass


def vm_already_exists(vminfo):
    msg = 'Abort <vm: "%s" - %s> : already exists in Drifterfile'
    click.secho(msg % (vminfo.name, vminfo.uuid), fg='red')
    sys.exit(1)


def vm_not_found(vminfo):
    msg = 'Abort <vm: "%s" - %s> : not found in Drifterfile'
    click.secho(msg % (vminfo.name, vminfo.uuid), fg='red')
    sys.exit(2)


def vm_name_not_found(name, exit_code=3):
    msg = 'Abort - name "%s", not found in available VMs'
    click.secho(msg % (name), fg='red')
    if exit_code:
        sys.exit(exit_code)


def vm_uuid_not_found(name, uuid, exit_code=4):
    msg = 'Error: <vm "%s" - %s> : UUID not found in Available VMs'
    click.secho(msg % (name, uuid), fg='red')
    if exit_code:
        sys.exit(exit_code)
