# This file is part of Ubuntu Continuous Integration virtual machine tools.
#
# Copyright 2014, 2015 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
import io
import os
import unittest
import yaml


from uciconfig import errors as conf_errors
from ucitests import (
    features,
    fixtures,
)
from ucivms import (
    config,
    errors,
    vms,
    ssh,
    subprocesses,
)
from ucivms.tests import (
    features as vms_features,
    fixtures as vms_fixtures,
)


def requires_known_reference_image(test):
    """Skip test if a known reference image is not provided locally.

    :note: This should be called early during setUp so the user configuration
        is still available (i.e. the test has not yet been isolated from disk).

    :param test: The TestCase requiring the image.
    """
    # We need a pre-seeded download cache from the user running the tests
    # as downloading the cloud image is too long.
    user_conf = config.VmStack(None)
    download_cache = user_conf.get('vm.download_cache')
    if download_cache is None:
        test.skipTest('vm.download_cache is not set')
    # We use some known reference
    reference_cloud_image_name = 'vivid-server-cloudimg-amd64-disk1.img'
    cloud_image_path = os.path.join(
        download_cache, reference_cloud_image_name)
    if not os.path.exists(cloud_image_path):
        test.skipTest('{} is not available'.format(cloud_image_path,))
    # Let's get the images directory set by the user. Qemu is guarded by
    # apparmor so only the user knows where this directory is. This is the only
    # place where tests can create images without triggering *very* obscure
    # 'Permission denied' errors. Even creating a temp dir below that dir
    # doesn't work.
    # /!\ This means tests should be careful when using this shared resource.
    # I.e. use unique names, cleanup.
    images_dir = user_conf.get('vm.images_dir')
    return download_cache, reference_cloud_image_name, images_dir


@features.requires(vms_features.use_sudo_for_tests_feature)
class TestDownload(unittest.TestCase):

    # FIXME: Needs parametrization against
    # vm.{cloud_image_name|cloud_tarball_name|iso_name} and
    # {download_iso|download_cloud_image|download_cloud_tarball}
    # {Lxc|Kvm}... May be we just need to test _download_in_cache() now that
    # it's implemented at Vm level and be done -- vila 2013-08-06

    def setUp(self):
        # Downloading real isos or images is too long for tests, instead, we
        # fake it by downloading a small but known to exist file: MD5SUMS
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        download_cache = os.path.join(self.uniq_dir, 'downloads')
        os.mkdir(download_cache)
        self.conf = config.VmStack('foo')
        self.conf.store._load_from_string('''
vm.iso_name=MD5SUMS
vm.cloud_image_name=MD5SUMS
vm.cloud_tarball_name=MD5SUMS
vm.release=vivid
vm.cpu_model=amd64
vm.download_cache={download_cache}
'''.format(download_cache=download_cache))
        self.addCleanup(self.conf.store.save_changes)

    def test_download_iso(self):
        vm = vms.Kvm(self.conf)
        self.assertTrue(vm.download_iso())
        # Trying to download again will find the file in the cache
        self.assertFalse(vm.download_iso())
        # Forcing the download even when the file is present
        self.assertTrue(vm.download_iso(force=True))

    def test_download_unknown_iso_fail(self):
        self.conf.set('vm.iso_name', 'I-dont-exist')
        vm = vms.Kvm(self.conf)
        self.assertRaises(errors.CommandError, vm.download_iso)

    def test_download_iso_with_unknown_cache_fail(self):
        dl_cache = os.path.join(self.uniq_dir, 'I-dont-exist')
        self.conf.set('vm.download_cache', dl_cache)
        vm = vms.Kvm(self.conf)
        self.assertRaises(errors.ConfigValueError, vm.download_iso)

    def test_download_cloud_image(self):
        vm = vms.Kvm(self.conf)
        self.assertTrue(vm.download_cloud_image())
        # Trying to download again will find the file in the cache
        self.assertFalse(vm.download_cloud_image())
        # Forcing the download even when the file is present
        self.assertTrue(vm.download_cloud_image(force=True))

    def test_download_unknown_cloud_image_fail(self):
        self.conf.set('vm.cloud_image_name', 'I-dont-exist')
        vm = vms.Kvm(self.conf)
        self.assertRaises(errors.CommandError, vm.download_cloud_image)

    def test_download_cloud_image_with_unknown_cache_fail(self):
        dl_cache = os.path.join(self.uniq_dir, 'I-dont-exist')
        self.conf.set('vm.download_cache', dl_cache)
        vm = vms.Kvm(self.conf)
        self.assertRaises(errors.ConfigValueError, vm.download_cloud_image)


class TestMetaData(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.Kvm(self.conf)
        images_dir = os.path.join(self.uniq_dir, 'images')
        os.mkdir(images_dir)
        config_dir = os.path.join(self.uniq_dir, 'config')
        self.conf.store._load_from_string('''
vm.name=foo
vm.images_dir={images_dir}
vm.config_dir={config_dir}
'''.format(images_dir=images_dir, config_dir=config_dir))

    def test_create_meta_data(self):
        self.vm.create_meta_data()
        self.assertTrue(os.path.exists(self.vm.config_dir_path()))
        self.assertTrue(os.path.exists(self.vm._meta_data_path))
        with open(self.vm._meta_data_path) as f:
            meta_data = f.readlines()
        self.assertEqual(2, len(meta_data))
        self.assertEqual('instance-id: foo\n', meta_data[0])
        self.assertEqual('local-hostname: foo\n', meta_data[1])


class TestYaml(unittest.TestCase):

    def yaml_load(self, *args, **kwargs):
        return yaml.safe_load(*args, **kwargs)

    def yaml_dump(self, *args, **kwargs):
        return yaml.safe_dump(*args, **kwargs)

    def test_load_scalar(self):
        self.assertEqual(
            {'foo': 'bar'}, self.yaml_load(io.StringIO('{foo: bar}')))
        # Surprisingly the enclosing braces are not needed, probably a special
        # case for the highest level
        self.assertEqual({'foo': 'bar'}, self.yaml_load(
            io.StringIO('foo: bar')))

    def test_dump_scalar(self):
        self.assertEqual('{foo: bar}\n', self.yaml_dump(dict(foo='bar')))

    def test_load_list(self):
        self.assertEqual({'foo': ['a', 'b', 'c']},
                         # Single space indentation is enough
                         self.yaml_load(io.StringIO('''\
foo:
 - a
 - b
 - c
''')))

    def test_dump_list(self):
        # No more enclosing braces... yeah for consistency :-/
        self.assertEqual(
            'foo: [a, b, c]\n', self.yaml_dump(dict(foo=['a', 'b', 'c'])))

    def test_load_dict(self):
        self.assertEqual({'foo': {'bar': 'baz'}},
                         self.yaml_load(io.StringIO('{foo: {bar: baz}}')))
        multiple_lines = '''\
foo: {bar: multiple
  lines}
'''
        self.assertEqual(
            {'foo': {'bar': 'multiple lines'}},
            self.yaml_load(io.StringIO(multiple_lines)))


class TestLaunchpadAccess(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.Kvm(self.conf)
        self.ci_data = vms.CIUserData(self.conf)

    def test_cant_find_private_key(self):
        self.conf.store._load_from_string('vm.launchpad_id = I-dont-exist')
        with self.assertRaises(errors.ConfigPathNotFound) as cm:
            self.ci_data.set_launchpad_access()
        key_path = '~/.ssh/I-dont-exist@uci-vms'
        self.assertEqual(key_path, cm.exception.path)
        msg_prefix = 'You need to create the {p} keypair'.format(p=key_path)
        self.assertTrue(cm.exception.fmt.startswith(msg_prefix))

    def test_id_with_key(self):
        ssh_dir = os.path.join(self.home_dir, '.ssh')
        os.mkdir(ssh_dir)
        key_path = os.path.join(ssh_dir, 'user@uci-vms')
        with open(key_path, 'w') as f:
            f.write('key content')
        self.conf.store._load_from_string('vm.launchpad_id = user')
        self.assertEqual(None, self.ci_data.launchpad_hook)
        self.ci_data.set_launchpad_access()
        self.assertEqual('''\
#!/bin/sh
mkdir -p /home/ubuntu/.ssh
chown ubuntu:ubuntu /home/ubuntu/.ssh
chmod 0700 /home/ubuntu/.ssh
cat >/home/ubuntu/.ssh/id_rsa <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
key content
EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown ubuntu:ubuntu /home/ubuntu/.ssh/id_rsa
chmod 0400 /home/ubuntu/.ssh/id_rsa
sudo -u ubuntu bzr launchpad-login user
''',
                         self.ci_data.launchpad_hook)


class TestCIUserData(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.ci_data = vms.CIUserData(self.conf)

    def test_empty_config(self):
        self.ci_data.populate()
        # Check default values
        self.assertIs(None, self.ci_data.root_hook)
        self.assertIs(None, self.ci_data.ubuntu_hook)
        cc = self.ci_data.cloud_config
        self.assertFalse(cc['apt_update'])
        self.assertFalse(cc['apt_upgrade'])
        self.assertEqual({'expire': False}, cc['chpasswd'])
        self.assertEqual('uci-vms finished installing in ${uptime} seconds.',
                         cc['final_message'])
        self.assertTrue(cc['manage_etc_hosts'])
        self.assertEqual('ubuntu', cc['password'])
        self.assertEqual({'mode': 'poweroff'}, cc['power_state'])

    def test_password(self):
        self.conf.store._load_from_string('vm.password = tagada')
        self.ci_data.populate()
        self.assertEquals('tagada', self.ci_data.cloud_config['password'])

    def test_apt_proxy(self):
        self.conf.store._load_from_string('vm.apt_proxy = tagada')
        self.ci_data.populate()
        self.assertEquals('tagada', self.ci_data.cloud_config['apt_proxy'])

    def test_final_message_precise(self):
        self.conf.store._load_from_string('vm.release = precise')
        self.ci_data.populate()
        self.assertEqual('uci-vms finished installing in $UPTIME seconds.',
                         self.ci_data.cloud_config['final_message'])

    def test_final_message_explicit(self):
        self.conf.store._load_from_string('vm.final_message = hello there')
        self.ci_data.populate()
        self.assertEqual('hello there',
                         self.ci_data.cloud_config['final_message'])

    def test_poweroff_precise(self):
        self.conf.store._load_from_string('vm.release = precise')
        self.ci_data.populate()
        self.assertEqual(['halt'], self.ci_data.cloud_config['runcmd'])

    def test_poweroff_quantal(self):
        self.conf.store._load_from_string('vm.release = quantal')
        self.ci_data.populate()
        self.assertEqual(['halt'], self.ci_data.cloud_config['runcmd'])

    def test_poweroff_other(self):
        self.conf.store._load_from_string('vm.release = raring')
        self.ci_data.populate()
        self.assertEqual(
            {'mode': 'poweroff'}, self.ci_data.cloud_config['power_state'])
        self.assertIs(None, self.ci_data.cloud_config.get('runcmd'))

    def test_update_true(self):
        self.conf.store._load_from_string('vm.update = True')
        self.ci_data.populate()
        cc = self.ci_data.cloud_config
        self.assertTrue(cc['apt_update'])
        self.assertTrue(cc['apt_upgrade'])

    def test_packages(self):
        self.conf.store._load_from_string('vm.packages = bzr,ubuntu-desktop')
        self.ci_data.populate()
        self.assertEqual(['bzr', 'ubuntu-desktop'],
                         self.ci_data.cloud_config['packages'])

    def test_apt_sources(self):
        self.conf.store._load_from_string('''\
vm.release = raring
# Ensure options are properly expanded (and comments supported ;)
_archive_url = http://archive.ubuntu.com/ubuntu
_ppa_url = https://u:p@ppa.lp.net/user/ppa/ubuntu
vm.apt_sources = deb {_archive_url} {vm.release} partner,\
 deb {_archive_url} {vm.release} main,\
 deb {_ppa_url} {vm.release} main|ABCDEF
''')
        self.ci_data.populate()
        self.assertEqual(
            [{'source': 'deb http://archive.ubuntu.com/ubuntu raring partner'},
             {'source': 'deb http://archive.ubuntu.com/ubuntu raring main'},
             {'source':
              'deb https://u:p@ppa.lp.net/user/ppa/ubuntu raring main',
              'keyid': 'ABCDEF'}],
            self.ci_data.cloud_config['apt_sources'])

    def create_file(self, path, content=None):
        if content is None:
            content = '{}\ncontent\n'.format(path)
        with open(path, 'wb') as f:
            f.write(bytes(content, 'utf8'))

    def test_good_ssh_keys(self):
        paths = ('rsa', 'rsa.pub', 'dsa', 'dsa.pub', 'ecdsa', 'ecdsa.pub')
        for path in paths:
            self.create_file(path)
        paths_as_list = ','.join(paths)
        self.conf.store._load_from_string(
            'vm.ssh_keys = {}'.format(paths_as_list))
        self.ci_data.populate()
        self.assertEqual({'dsa_private': 'dsa\ncontent\n',
                          'dsa_public': 'dsa.pub\ncontent\n',
                          'ecdsa_private': 'ecdsa\ncontent\n',
                          'ecdsa_public': 'ecdsa.pub\ncontent\n',
                          'rsa_private': 'rsa\ncontent\n',
                          'rsa_public': 'rsa.pub\ncontent\n'},
                         self.ci_data.cloud_config['ssh_keys'])

    def test_bad_type_ssh_keys(self):
        self.conf.store._load_from_string('vm.ssh_keys = I-dont-exist')
        self.assertRaises(errors.ConfigValueError, self.ci_data.populate)

    def test_unknown_ssh_keys(self):
        self.conf.store._load_from_string('vm.ssh_keys = rsa.pub')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_good_ssh_authorized_keys(self):
        paths = ('home.pub', 'work.pub')
        for path in paths:
            self.create_file(path)
        paths_as_list = ','.join(paths)
        self.conf.store._load_from_string(
            'vm.ssh_authorized_keys = {}'.format(paths_as_list))
        self.ci_data.populate()
        self.assertEqual(['home.pub\ncontent\n', 'work.pub\ncontent\n'],
                         self.ci_data.cloud_config['ssh_authorized_keys'])

    def test_unknown_ssh_authorized_keys(self):
        self.conf.store._load_from_string('vm.ssh_authorized_keys = rsa.pub')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_unknown_root_script(self):
        self.conf.store._load_from_string('vm.root_script = I-dont-exist')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_unknown_ubuntu_script(self):
        self.conf.store._load_from_string('vm.ubuntu_script = I-dont-exist')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_expansion_error_in_script(self):
        root_script_content = '''#!/bin/sh
echo Hello {I_dont_exist}
'''
        with open('root_script.sh', 'w') as f:
            f.write(root_script_content)
        self.conf.store._load_from_string('''\
vm.root_script = root_script.sh
''')
        with self.assertRaises(conf_errors.ExpandingUnknownOption) as cm:
            self.ci_data.populate()
        self.assertEqual(root_script_content, cm.exception.string)

    def test_unknown_uploaded_scripts(self):
        self.conf.store._load_from_string(
            '''vm.uploaded_scripts = I-dont-exist ''')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_root_script(self):
        with open('root_script.sh', 'w') as f:
            f.write('''#!/bin/sh
echo Hello {user}
''')
        self.conf.store._load_from_string('''\
vm.root_script = root_script.sh
user=root
''')
        self.ci_data.populate()
        # The additional newline after the script is expected
        self.assertEqual('''\
#!/bin/sh
cat >/tmp/root-uci-vms_post_install <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
#!/bin/sh
echo Hello root

EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown root:root /tmp/root-uci-vms_post_install
chmod 0700 /tmp/root-uci-vms_post_install
''', self.ci_data.root_hook)
        self.assertEqual(['/tmp/root-uci-vms_post_install'],
                         self.ci_data.cloud_config['runcmd'])

    def test_ubuntu_script(self):
        with open('ubuntu_script.sh', 'w') as f:
            f.write('''#!/bin/sh
echo Hello {user}
''')
        self.conf.store._load_from_string('''\
vm.ubuntu_script = ubuntu_script.sh
user = ubuntu
''')
        self.ci_data.populate()
        # The additional newline after the script is expected
        self.assertEqual('''\
#!/bin/sh
echo Hello ubuntu
''', self.ci_data.ubuntu_hook)

    def test_uploaded_scripts(self):
        paths = ('foo', 'bar')
        for path in paths:
            self.create_file(path)
        paths_as_list = ','.join(paths)
        self.conf.store._load_from_string(
            'vm.uploaded_scripts = {}'.format(paths_as_list))
        self.ci_data.populate()
        self.assertEqual('''\
#!/bin/sh
cat >~ubuntu/uci-vms_uploads <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
mkdir -p ~ubuntu/bin
cd ~ubuntu/bin
cat >foo <<'EOFfoo'
foo
content

EOFfoo
chmod 0755 foo
cat >bar <<'EOFbar'
bar
content

EOFbar
chmod 0755 bar
EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown ubuntu:ubuntu ~ubuntu/uci-vms_uploads
chmod 0700 ~ubuntu/uci-vms_uploads
''',
                         self.ci_data.uploaded_scripts_hook)
        self.assertEqual([['su', '-l', '-c', '~ubuntu/uci-vms_uploads',
                           'ubuntu']],
                         self.ci_data.cloud_config['runcmd'])


class TestCreateUserData(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.Kvm(self.conf)

    def test_empty_config(self):
        config_dir = os.path.join(self.uniq_dir, 'config')
        # The config is *almost* empty, we need to set config_dir though as the
        # user-data needs to be stored there.
        self.conf.store._load_from_string('vm.config_dir=' + config_dir)
        self.vm.create_user_data()
        self.assertTrue(os.path.exists(self.vm.config_dir_path()))
        self.assertTrue(os.path.exists(self.vm._user_data_path))
        with open(self.vm._user_data_path) as f:
            user_data = f.readlines()
        # We care about the two first lines only here, checking the format (or
        # cloud-init is confused)
        self.assertEqual('#cloud-config-archive\n', user_data[0])
        self.assertEqual("- {content: '#cloud-config\n", user_data[1])


class TestSeedData(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.VM(self.conf)
        images_dir = os.path.join(self.uniq_dir, 'images')
        os.mkdir(images_dir)
        config_dir = os.path.join(self.uniq_dir, 'config')
        self.conf.store._load_from_string('''
vm.name=foo
vm.release=raring
vm.config_dir={config_dir}
vm.images_dir={images_dir}
'''.format(config_dir=config_dir, images_dir=images_dir))

    def test_create_meta_data(self):
        self.vm.create_meta_data()
        self.assertTrue(os.path.exists(self.vm._meta_data_path))

    def test_create_user_data(self):
        self.vm.create_user_data()
        self.assertTrue(os.path.exists(self.vm._user_data_path))


@features.requires(vms_features.use_sudo_for_tests_feature)
@features.requires(vms_features.qemu_img_feature)
class TestSeedImage(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.Kvm(self.conf)
        images_dir = os.path.join(self.uniq_dir, 'images')
        os.mkdir(images_dir)
        config_dir = os.path.join(self.uniq_dir, 'config')
        self.conf.store._load_from_string('''
vm.name=foo
vm.release=raring
vm.config_dir={config_dir}
vm.images_dir={images_dir}
'''.format(config_dir=config_dir, images_dir=images_dir))

    def test_create_seed_image(self):
        self.assertTrue(self.vm._seed_path is None)
        self.vm.create_seed_image()
        self.assertFalse(self.vm._seed_path is None)
        self.assertTrue(os.path.exists(self.vm._seed_path))


@features.requires(vms_features.use_sudo_for_tests_feature)
@features.requires(vms_features.qemu_img_feature)
class TestImageFromCloud(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.Kvm(self.conf)
        images_dir = os.path.join(self.uniq_dir, 'images')
        os.mkdir(images_dir)
        download_cache_dir = os.path.join(self.uniq_dir, 'download')
        os.mkdir(download_cache_dir)
        self.conf.store._load_from_string('''
vm.name=foo
vm.release=raring
vm.images_dir={images_dir}
vm.download_cache={download_cache_dir}
vm.cloud_image_name=fake.img
vm.disk_size=1M
'''.format(images_dir=images_dir, download_cache_dir=download_cache_dir))

    def test_create_disk_image(self):
        cloud_image_path = os.path.join(self.conf.get('vm.download_cache'),
                                        self.conf.get('vm.cloud_image_name'))
        # We need a fake cloud image that can be converted
        subprocesses.run(
            ['sudo', 'qemu-img', 'create',
             cloud_image_path, self.conf.get('vm.disk_size')])
        self.assertTrue(self.vm._disk_image_path is None)
        self.vm.create_disk_image()
        self.assertFalse(self.vm._disk_image_path is None)
        self.assertTrue(os.path.exists(self.vm._disk_image_path))


@features.requires(vms_features.use_sudo_for_tests_feature)
class TestImageWithBacking(unittest.TestCase):

    def setUp(self):
        (download_cache_dir,
         reference_cloud_image_name,
         images_dir) = requires_known_reference_image(self)
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
vm.release=vivid
vm.images_dir={images_dir}
vm.download_cache={download_cache}
vm.disk_size=3G
[test-image-from-cloud]
vm.name=test-image-from-cloud
vm.cloud_image_name={cloud_image_name}
[test-image-backing]
vm.name=test-image-backing
vm.backing=test-image-from-cloud.qcow2
'''.format(images_dir=images_dir, download_cache=download_cache_dir,
           cloud_image_name=reference_cloud_image_name))
        conf.store.save()
        # To bypass creating a real vm, we start from the cloud image that is a
        # real and bootable one, so we just convert it. That also makes it
        # available in vm.images_dir
        temp_vm = vms.Kvm(config.VmStack('test-image-from-cloud'))
        temp_vm.create_disk_image()
        self.addCleanup(subprocesses.run,
                        ['sudo', 'rm', '-f', temp_vm._disk_image_path])

    def test_create_image_with_backing(self):
        vm = vms.Kvm(config.VmStack('test-image-backing'))
        self.assertTrue(vm._disk_image_path is None)
        vm.create_disk_image()
        self.addCleanup(subprocesses.run,
                        ['sudo', 'rm', '-f', vm._disk_image_path])
        self.assertFalse(vm._disk_image_path is None)
        self.assertTrue(os.path.exists(vm._disk_image_path))


class TestKvmStates(unittest.TestCase):

    def assertStates(self, expected, lines):
        self.assertEqual(expected, vms.kvm_states(lines))

    def test_empty(self):
        self.assertStates({}, [])

    def test_garbage(self):
        with self.assertRaises(ValueError):
            self.assertStates(None, [''])

    def test_known_states(self):
        # From a real life sample
        self.assertStates({'foo': 'shut off', 'bar': 'running'},
                          ['-     foo                            shut off',
                           '19    bar                            running'])


class TestLxcInfo(unittest.TestCase):

    def assertInfo(self, expected, lines):
        self.assertEqual(expected, vms.lxc_info('foo', lines))

    def test_empty(self):
        self.assertRaises(IndexError, self.assertInfo, {}, [])

    # FIXME: Meh, can't work anymore, lxc_info needs a complete rewrite may be
    # even using the python interface now that we've switched to py3. But using
    # the python interface also means we can't use 'sudo' anymore so that would
    # require using unprivileged containers first -- vila 2015-06-26
    def xtest_garbage(self):
        self.assertRaises(ValueError, self.assertInfo, None, [''])

    def test_stopped_with_pid(self):
        # From a real life sample
        self.assertInfo({'state': 'STOPPED', 'pid': '-1'},
                        ['State:   STOPPED',
                         'pid:        -1'])

    def test_stopped_without_pid(self):
        # From a real life sample
        self.assertInfo({'state': 'STOPPED', 'pid': '-1'},
                        ['State:   STOPPED'])

    def test_running(self):
        # From a real life sample
        self.assertInfo({'state': 'RUNNING', 'pid': '30937'},
                        ['State:   RUNNING',
                         'pid:     30937'])


@features.requires(vms_features.use_sudo_for_tests_feature)
class TestInstallWithSeed(unittest.TestCase):

    def setUp(self):
        (download_cache,
         reference_cloud_image_name,
         images_dir) = requires_known_reference_image(self)
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        # We need to allow other users to read this dir
        os.chmod(self.uniq_dir, 0o755)
        # We also need to sudo rm it as root created some files there
        self.addCleanup(
            subprocesses.run,
            ['sudo', 'rm', '-fr',
             os.path.join(self.uniq_dir, 'home', '.virtinst')])
        self.conf = config.VmStack('selftest-seed')
        self.vm = vms.Kvm(self.conf)
        config_dir = os.path.join(self.uniq_dir, 'config')
        self.conf.store._load_from_string('''
vm.name=selftest-seed
vm.update=False # Shorten install time
vm.cpus=2,
vm.release=vivid
vm.config_dir={config_dir}
vm.images_dir={images_dir}
vm.download_cache={download_cache}
vm.cloud_image_name={cloud_image_name}
vm.disk_size=8G
'''.format(config_dir=config_dir, images_dir=images_dir,
           download_cache=download_cache,
           cloud_image_name=reference_cloud_image_name))

    def test_install_with_seed(self):
        self.addCleanup(self.vm.undefine)
        self.vm.install()
        self.assertEqual('shut off', self.vm.state())
        # As a side-effect, the console and the interface file are created
        # MISSINGTEST: This applies to Kvm only, lxc needs the same,
        # parametrization will be ideal but it's ok for now -- vila 2014-01-18
        self.assertTrue(os.path.exists(self.vm.console_path()))
        self.assertTrue(os.path.exists(self.vm.iface_path('eth0')))


@features.requires(vms_features.use_sudo_for_tests_feature)
class TestInstallWithBacking(unittest.TestCase):

    def setUp(self):
        (download_cache_dir,
         reference_cloud_image_name,
         images_dir) = requires_known_reference_image(self)
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        # We need to allow other users to read this dir
        os.chmod(self.uniq_dir, 0o755)
        # We also need to sudo rm it after the test as root created some files
        # there
        self.addCleanup(
            subprocesses.run,
            ['sudo', 'rm', '-fr',
             os.path.join(self.uniq_dir, 'home', '.virtinst')])
        config_dir = os.path.join(self.uniq_dir, 'config')
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
vm.release=vivid
vm.config_dir={config_dir}
vm.images_dir={images_dir}
vm.download_cache={download_cache_dir}
vm.disk_size=3G
vm.update=False # Shorten install time
[selftest-from-cloud]
vm.name=selftest-from-cloud
vm.cloud_image_name={reference_cloud_image_name}
[selftest-backing]
vm.name=selftest-backing
vm.backing=selftest-from-cloud.qcow2
'''.format(config_dir=config_dir, images_dir=images_dir,
           download_cache_dir=download_cache_dir,
           reference_cloud_image_name=reference_cloud_image_name))
        conf.store.save()
        conf.store.unload()
        # Fake a previous install by just re-using the reference cloud image
        temp_vm = vms.Kvm(config.VmStack('selftest-from-cloud'))
        temp_vm.create_disk_image()
        self.addCleanup(subprocesses.run,
                        ['sudo', 'rm', '-f', temp_vm._disk_image_path])

    def test_install_with_backing(self):
        vm = vms.Kvm(config.VmStack('selftest-backing'))
        self.addCleanup(vm.undefine)
        vm.install()
        self.assertEqual('shut off', vm.state())
        # As a side-effect, the console and the interface files are created
        # MISSINGTEST: This applies to Kvm only, lxc needs the same,
        # parametrization will be ideal but it's ok for now -- vila 2014-01-18
        self.assertTrue(os.path.exists(vm.console_path()))
        self.assertTrue(os.path.exists(vm.iface_path('eth0')))


class TestKeyGen(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack(None)
        self.vm = vms.VM(self.conf)
        self.config_dir = os.path.join(self.uniq_dir, 'config')

    def load_config(self, more):
        content = '''\
vm.config_dir={config_dir}
vm.name=foo
'''.format(config_dir=self.config_dir)
        self.conf.store._load_from_string(content + more)

    def override_ssh_keygen(self):
        self.keygen_called = False

        def fake_key_gen(*args, **kwargs):
            self.keygen_called = True

        fixtures.patch(self, ssh, 'keygen', fake_key_gen)

    def test_do_nothing_if_key_exists(self):
        self.load_config('vm.ssh_keys=rsa')
        path = self.conf.get('vm.ssh_keys')[0]
        self.override_ssh_keygen()
        with open(path, 'w') as f:
            f.write('something')
        self.vm.ssh_keygen()
        self.assertFalse(self.keygen_called)

    def test_recreate_key_if_force(self):
        self.load_config('vm.ssh_keys=rsa')
        self.override_ssh_keygen()
        path = self.conf.get('vm.ssh_keys')[0]
        with open(path, 'w') as f:
            f.write('something')
        self.vm.ssh_keygen(force=True)
        self.assertTrue(self.keygen_called)

    def assertKeygen(self, ssh_type, upper_type=None):
        if upper_type is None:
            upper_type = ssh_type.upper()
        self.load_config('vm.ssh_keys={vm.config_dir}/' + ssh_type)
        self.vm.ssh_keygen()
        private_path = 'config/{}'.format(ssh_type)
        self.assertTrue(os.path.exists(private_path))
        public_path = 'config/{}.pub'.format(ssh_type)
        self.assertTrue(os.path.exists(public_path))

    def test_dsa(self):
        self.assertKeygen('dsa')

    def test_rsa(self):
        self.assertKeygen('rsa')

    @features.requires(vms_features.ssh_feature)
    def test_ecdsa(self):
        vms_features.ssh_feature.requires_ecdsa(self)
        self.assertKeygen('ecdsa', 'EC')


class TestSSH(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        self.conf = config.VmStack(None)
        self.vm = vms.VM(self.conf)
        self.config_dir = os.path.join(self.uniq_dir, 'config')

    def load_config(self, more):
        content = '''\
vm.config_dir={config_dir}
vm.name=foo
'''.format(config_dir=self.config_dir)
        self.conf.store._load_from_string(content + more)

    def test_defaults(self):
        self.load_config('')
        ssh_cmd = self.vm.get_ssh_command('whoami', ip='localhost')
        self.assertEqual(['ssh', 'ubuntu@localhost', 'whoami'], ssh_cmd)

    def test_user_only_is_ignored(self):
        self.load_config('vm.user = foo')
        ssh_cmd = self.vm.get_ssh_command('whoami', ip='localhost')
        self.assertEqual(['ssh', 'ubuntu@localhost', 'whoami'], ssh_cmd)

    def test_bind_home(self):
        self.load_config('vm.bind_home = True\nvm.user = foo\n')
        ssh_cmd = self.vm.get_ssh_command('whoami', ip='localhost')
        self.assertEqual(['ssh', 'foo@localhost', 'whoami'], ssh_cmd)


@features.requires(vms_features.use_sudo_for_tests_feature)
class TestEmptyConsole(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_fixtures.isolate_from_disk(self)
        # To isolate tests from each other, created vms needs a unique name. To
        # keep those names legal and still user-readable we use the class name
        # and the test method name
        self.vm_name = '{}-{}'.format(self.__class__.__name__,
                                      self._testMethodName)
        config_dir = os.path.join(self.uniq_dir, 'config')
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
vm.config_dir={config_dir}
[{vm_name}]
vm.name = {vm_name}
vm.class = lxc
'''.format(config_dir=config_dir, vm_name=self.vm_name))
        conf.store.save()
        conf.store.unload()

    def test_no_console(self):
        vm = vms.Lxc(config.VmStack(self.vm_name))
        self.assertFalse(os.path.exists(vm.console_path()))
        vm.empty_console()
        self.assertTrue(os.path.exists(vm.console_path()))

    def test_existing_console_is_emptied(self):
        vm = vms.Lxc(config.VmStack(self.vm_name))
        self.assertFalse(os.path.exists(vm.console_path()))
        vm.empty_console()
        self.assertTrue(os.path.exists(vm.console_path()))
        # Let's put some random stuff in that console file
        with open(vm.console_path(), 'w') as f:
            f.write('stuff')
        with open(vm.console_path()) as f:
            actual_content = f.read()
        self.assertEqual('stuff', actual_content)
        vm.empty_console()
        self.assertTrue(os.path.exists(vm.console_path()))
        with open(vm.console_path()) as f:
            final_content = f.read()
        self.assertEqual('', final_content)

    def test_root_owned_existing_console(self):
        vm = vms.Lxc(config.VmStack(self.vm_name))
        self.assertFalse(os.path.exists(vm.console_path()))
        vm.empty_console()
        self.assertTrue(os.path.exists(vm.console_path()))
        subprocesses.run(['sudo', 'chown', 'root:root', vm.console_path()])
        vm.empty_console()
        with open(vm.console_path()) as f:
            actual_content = f.read()
        self.assertEqual('', actual_content)


@features.requires(vms_features.use_sudo_for_tests_feature)
class TestEphemeralLXC(unittest.TestCase):

    def setUp(self):
        super().setUp()
        vms_features.requires_existing_vm(self, 'uci-vms-tests-trusty')
        vms_fixtures.isolate_from_disk(self)
        # To isolate tests from each other, created vms needs a unique name. To
        # keep those names legal and still user-readable we use the class name
        # and the test method name
        self.vm_name = '{}-{}'.format(self.__class__.__name__,
                                      self._testMethodName)
        config_dir = os.path.join(self.uniq_dir, 'config')
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
vm.ssh_opts=-oUserKnownHostsFile=/dev/null,-oStrictHostKeyChecking=no
vm.config_dir={config_dir}
# /!\ Should match the one defined by the user
[uci-vms-tests-trusty]
vm.name = uci-vms-tests-trusty
vm.class = lxc
vm.release = trusty
[{vm_name}]
vm.name = {vm_name}
vm.class = ephemeral-lxc
vm.backing = uci-vms-tests-trusty
vm.release = trusty
'''.format(config_dir=config_dir, vm_name=self.vm_name))
        conf.store.save()
        conf.store.unload()

    def test_start(self):
        vm = vms.EphemeralLxc(config.VmStack(self.vm_name))
        self.addCleanup(vm.stop)
        vm.start()
        self.assertEqual('RUNNING', vm.state())

    def test_stop(self):
        vm = vms.EphemeralLxc(config.VmStack(self.vm_name))
        vm.start()
        vm.stop()
        self.assertEqual('UNKNOWN', vm.state())


# MISSING TESTS:
# vm.start() for lxc and kvm
# class TestRetry(unittest.TestCase):
#
#    def test_no_timeouts_run_once(self):
#        pass
#
#    def test_fail_exhausts_timeouts(self):
#        pass
#
#    def test_fail_once_then_succeed(self):
#        pass
