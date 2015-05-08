import sys
from modulefinder import ModuleFinder
import glob
import json
import os
import shutil
from tempfile import mkdtemp, NamedTemporaryFile
import subprocess
from uuid import uuid4

import click
from lxml import etree

from ags.admin.server import ServerAdmin
from ags.admin.services.gp import GPServerDefinition
from ags.exceptions import ServerError, HTTPError
from ags.gp import GPTask


PUBLISH_TOOL_PATH = '/arcgis/rest/services/System/PublishingTools/GPServer/Publish%20Service%20Definition'
SD_ROOT_DIRECTORY = 'v101'
SCRIPT_DIRECTORY = os.path.abspath(os.path.split(__file__)[0])

MANIFEST_TEMPLATE = """
<SVCManifest xmlns:typens='http://www.esri.com/schemas/ArcGIS/10.1' xmlns:xs='http://www.w3.org/2001/XMLSchema' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:type='typens:SVCManifest'>
    <ID></ID>
    <Name></Name>
    <ByReference>true</ByReference>
    <Type>esriServiceDefinitionType_New</Type>
    <State>esriSDState_Staged</State>
    <ServerType>esriSVCServerType_FullServer</ServerType>
    <KeepExistingData>false</KeepExistingData>
    <KeepExistingMapCache>false</KeepExistingMapCache>
    <Resources xsi:type='typens:ArrayOfSVCResource'>
        <SVCResource xsi:type='typens:SVCResource'>
            <ID></ID>
            <Name></Name>
            <InPackagePath></InPackagePath>
        </SVCResource>
    </Resources>
</SVCManifest>
"""


def find_local_modules(filename):
    """Returns file path to local modules used by the script specified by filename"""

    base_dir = os.path.dirname(filename)
    sys.path.insert(0, base_dir)
    finder = ModuleFinder()
    finder.run_script(filename)
    return [module.__file__ for name, module in finder.modules.iteritems()
            if module.__file__ and module.__file__.count(base_dir)]


def create_text_node(document, tag_name, content):
    """Creates an element node with a text node containing the given content."""

    element = document.createElement(tag_name)
    element.appendChild(document.createTextNode(content))
    return element


def create_manifest(path, toolbox, service_name):
    """Creates a manifest.xml file in the specified path"""

    f = open(os.path.join(path, 'manifest.xml'), 'w')
    tree = etree.fromstring(MANIFEST_TEMPLATE)
    tree.xpath('/SVCManifest/ID')[0].text = '{%s}' % str(uuid4())
    tree.xpath('/SVCManifest/Name')[0].text = service_name
    tree.xpath('/SVCManifest/Resources/SVCResource/ID')[0].text = '{%s}' % str(uuid4())
    tree.xpath('/SVCManifest/Resources/SVCResource/Name')[0].text = toolbox
    tree.xpath('/SVCManifest/Resources/SVCResource/InPackagePath')[0].text = os.path.join(SD_ROOT_DIRECTORY, toolbox)
    f.write(etree.tostring(tree))
    f.close()


def create_service_configuration(path, service_name, description='', folder_name='', auto_start=True, async=True,
                                 message_type='None', max_instances=None, max_usage_time=None):
    """
    Creates serviceconfiguration.json in the specified path.

    :param message_type: must be one of None, Warning, Info, Error
    """

    definition = GPServerDefinition(
        service_name=service_name,
        description=description
    )
    for attr in ('toolbox', 'jobs_directory', 'jobs_virtual_directory', 'output_dir', 'virtual_output_dir'):
        setattr(definition.properties, attr, '')

    data = definition.get_data()
    data['configuredState'] = 'STARTED' if auto_start else 'STOPPED'

    data['properties']['executionType'] = 'asynchronous' if async else 'synchronous'
    data['properties']['showMessages'] = message_type
    if max_instances is not None:
        data['maxInstancesPerNode'] = max_instances
    if max_usage_time is not None:
        data['maxUsageTime'] = max_usage_time

    f = open(os.path.join(path, 'serviceconfiguration.json'), 'w')
    f.write(json.dumps({
        'folderName': folder_name,
        'service': data
    }))
    f.close()


def copy_files(target_path, toolbox_path, file_patterns=None):
    """Finds all files that match file_patterns or local dependencies of toolbox and copies into target_path"""

    path, toolbox = os.path.split(toolbox_path)
    path = path or '.'
    os.chdir(path)

    #Copy all local dependencies detected from toolbox, including the toolbox itself
    for module_filename in find_local_modules(toolbox_path):
        directory, filename = os.path.split(module_filename)
        directory = directory or os.getcwd()
        target_dir = os.path.join(target_path, os.path.relpath(directory))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy(module_filename, os.path.join(target_dir, filename))

    if file_patterns:
        paths_to_copy = set()
        for pattern in (p for p in file_patterns.split(',') if p):
            for path in glob.glob(pattern.strip()):
                paths_to_copy.add(path)

        for path in paths_to_copy:
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(target_path, path))
            else:
                directory, filename = os.path.split(path)
                target_dir = os.path.join(target_path, os.path.relpath(directory)) if directory else target_path
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                shutil.copy(path, os.path.join(target_dir, filename))


def create_sd(toolbox_path, service_name, description='', service_folder='', file_patterns=None, **service_config):
    """Creates the service definition file and returns a NamedTemporaryFile object"""

    path, toolbox = os.path.split(toolbox_path)
    temp_dir = mkdtemp()
    try:
        target_dir = os.path.join(temp_dir, SD_ROOT_DIRECTORY)
        os.makedirs(target_dir)

        #Write manifest file
        create_manifest(temp_dir, toolbox, service_name)

        #Write service configuration file
        create_service_configuration(temp_dir, service_name, description, service_folder, **service_config)

        #Copy dependencies and other files that match file_patterns
        copy_files(os.path.join(temp_dir, SD_ROOT_DIRECTORY), toolbox_path, file_patterns)

        #Create archive
        os.chdir(temp_dir)
        sd_filename = toolbox.replace('.pyt', '.sd')
        print("--------------- CREATING SERVICE DEFINITION FILE USING 7ZIP -----------------------")
        subprocess.call('7z a -t7z -ms=off {0} *'.format(sd_filename))
        print("--------------- DONE CREATING SERVICE DEFINITION FILE USING 7ZIP ------------------")

        #Copy to temporary file and return
        temp_file = NamedTemporaryFile(suffix='.sd')
        f = open(os.path.join(temp_dir, sd_filename), 'rb')
        shutil.copyfileobj(f, temp_file)
        f.close()
        temp_file.seek(0)
        return temp_file
    finally:
        try:
            shutil.rmtree(temp_dir)
        except OSError:
            pass


def deploy_sd(sd_file, service_name, hostname, admin_user, admin_pwd, overwrite=False):
    """Deploys the given .sd file to an ArcGIS server."""

    server_admin = ServerAdmin(hostname, admin_user, admin_pwd)
    folder, service = os.path.split(service_name)
    if server_admin.service_exists(service_name, 'GPServer'):
        if not overwrite:
            raise Exception('The service {0} already exists, and overwrite is set to false'.format(service_name))
        server_admin.delete_service(service, 'GPServer', folder)

    print('Uploading to server')
    upload_item = server_admin.upload_item(sd_file, service_name)
    print('Publishing service')

    t = GPTask('http://{0}{1}'.format(hostname, PUBLISH_TOOL_PATH), {'in_sdp_id': upload_item.id},
               token=server_admin.token)
    t.submit_job(True)
    if t.status != t.SUCCEEDED:
        raise Exception('Toolbox deployment failed:\n{0}'.format('\n'.join([str(m) for m in t.messages])))

    svc_info = server_admin.get_service(service, 'GPServer', folder)
    print('Toolbox is published to: {0}'.format(svc_info.properties['toolbox']))
    print('Service is now published to: {0}/arcgis/rest/services/{1}/GPServer'.format(hostname, service_name))


@click.group()
def deploy():
    """Manage deployment operations for an ArcGIS python toolbox."""


@deploy.command()
@click.argument('toolbox_path', metavar='<toolbox_path>', type=click.Path(True, dir_okay=False))
@click.argument('service_name', metavar='<service_name>')
@click.argument('outfile', metavar='<outfile_name>', type=click.File(mode='wb', lazy=False))
@click.option('--files', metavar='<files>',
              help='Wildcard patterns of additional files to include (relative to toolbox).  Example: *.csv,some_data.*')
@click.option('--hg', metavar='<hg>', is_flag=True, help='Include Mercurial (hg) repository information?')
@click.option('--sync', default=False, is_flag=True,
              help='Execute tool synchronously instead of asynchronously (default)')
@click.option('--messages', 'message_type', type=click.Choice(('None', 'Info', 'Error', 'Warning')), default='None',
              help='Level of messaging for service')
def package(toolbox_path, service_name, outfile, sync, message_type, files, hg):
    """
    Package a python toolbox into a service definition file (*.sd).
    Local python modules this toolbox references are included automatically.
    Requires 7Zip to be installed and on the system PATH.

    WARNING: this will overwrite the file <outfile_name> if it already exists.

    \b
    Aguments:
    <toolbox_path>:         Filename of python toolbox (*.pyt) to deploy
    <service_name>:         Name of service, including folder(s).  Example: SomeFolder/MyTool
    <outfile>:              Name of the service definition file to create
    """

    if hg:
        files = '{0},.hg/hgrc,.hg/branch'.format(files or "")

    sd = create_sd(toolbox_path, service_name, file_patterns=files, async=not sync, message_type=message_type)
    shutil.copyfileobj(sd, outfile)
    sd.close()



@deploy.command()
@click.argument('toolbox_path', metavar='<toolbox_path>', type=click.Path(True, dir_okay=False))
@click.argument('service_name', metavar='<service_name>')
@click.argument('server', metavar='<server:port>')
@click.argument('user', metavar='<user>')
@click.option('--password', metavar='<password>', prompt='ArcGIS Administrator Password', hide_input=True,
              help='ArcGIS administrator password.  You will be prompted for this if you do not provide it')
@click.option('--files', metavar='<files>',
              help='Wildcard patterns of additional files to include (relative to toolbox).  Example: *.csv,some_data.*')
@click.option('--hg', metavar='<hg>', is_flag=True, help='Include Mercurial (hg) repository information?')
@click.option('--sync', default=False, is_flag=True,
              help='Execute tool synchronously instead of asynchronously (default)')
@click.option('--messages', 'message_type', type=click.Choice(('None', 'Info', 'Error', 'Warning')), default='None',
              help='Level of messaging for service')
@click.option('--overwrite', 'overwrite', default=False, is_flag=True,
              help='Delete and replace the service, if it already exists?')

def publish(toolbox_path, service_name, server, user, password, sync, message_type, files, hg, overwrite):
    """
    Publish a python toolbox to an ArcGIS server.
    Local python modules this toolbox references are included automatically.
    Requires 7Zip to be installed and on the system PATH.

    \b
    Aguments:
    <toolbox_path>:         Filename of python toolbox (*.pyt) to deploy
    <service_name>:         Name of service, including folder(s).  Example: SomeFolder/MyTool
    <server:port>:               Hostname and port number of ArcGIS server
    <user>:                 ArcGIS server administrator user name
    """

    if hg:
        files = '{0},.hg/hgrc,.hg/branch'.format(files or "")

    sd = create_sd(toolbox_path, service_name, file_patterns=files, async=not sync, message_type=message_type)

    try:
        deploy_sd(sd, service_name, server, user, password, overwrite=overwrite)
    except ServerError as ex:
        raise click.ClickException(ex.message)


if __name__ == '__main__':
    deploy()