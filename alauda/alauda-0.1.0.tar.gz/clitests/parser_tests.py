import unittest
import mock

from alaudacli import cmd_parser, cmd_processor, util, auth


class UtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_image_name_tag(self):
        name, tag = util.parse_image_name_tag('index/user/repo:tag')
        self.assertEqual('index/user/repo', name)
        self.assertEqual('tag', tag)

    def test_parse_image_name_no_tag(self):
        name, tag = util.parse_image_name_tag('index/user/repo')
        self.assertEqual('index/user/repo', name)
        self.assertEqual('latest', tag)

    def test_parse_target_state(self):
        state = util.parse_target_state(True)
        self.assertEqual('STOPPED', state)
        state = util.parse_target_state(False)
        self.assertEqual('STARTED', state)

    def test_parse_instance_ports(self):
        ports = util.parse_instance_ports(['80/tcp', '22/tcp'])
        self.assertEqual([{'container_port': 80, 'protocol': 'tcp'}, {'container_port': 22, 'protocol': 'tcp'}], ports)

    def test_parse_envvars(self):
        envvars = util.parse_envvars(['FOO=foo', 'BAR=bar'])
        self.assertEqual({'FOO': 'foo', 'BAR': 'bar'}, envvars)

    def test_build_headers(self):
        headers = auth.build_headers('toooooken')
        self.assertEqual({'Authorization': 'Token toooooken', 'Content-type': 'application/json'}, headers)


class ProcessCmdTest(unittest.TestCase):
    def setUp(self):
        pass

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_login(self, mock_commands):
        argv = ['login', '-u', 'user', '-p', 'password', '-c', 'io']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.login.assert_called_with('user', 'password', 'io', None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_logout(self, mock_commands):
        argv = ['logout']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.logout.assert_called()

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_create(self, mock_commands):
        argv = ['service', 'create', 'index.alauda.io/alauda/hello-world:latest',
                'hello', '--do-not-start', '-t', '2', '-s', 'XS', '-r', '/run.sh',
                '-e', 'FOO=bar', '-p', '5000/tcp']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_create.assert_called_with(image='index.alauda.io/alauda/hello-world:latest',
                                                        name='hello', do_not_start=True, target_num_instances=2, instance_size='XS',
                                                        run_command='/run.sh', env=['FOO=bar'], ports=['5000/tcp'])

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_update(self, mock_commands):
        argv = ['service', 'update', 'hello', '-t', '2']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_update.assert_called_with('hello', target_num_instances=2)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_get(self, mock_commands):
        argv = ['service', 'get', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_get.assert_called_with('hello')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_start(self, mock_commands):
        argv = ['service', 'start', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_start.assert_called_with('hello')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_stop(self, mock_commands):
        argv = ['service', 'stop', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_stop.assert_called_with('hello')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_delete(self, mock_commands):
        argv = ['service', 'delete', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_delete.assert_called_with('hello')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_list(self, mock_commands):
        argv = ['service', 'list']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_list.assert_called_()
