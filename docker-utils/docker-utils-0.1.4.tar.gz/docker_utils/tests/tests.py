import unittest

import docker
import mock

from compose.project import Project
from compose.project import NoSuchService
from docker_utils.cmds.bash import bash
from docker_utils.cmds.utils import NoContainer
from nose.tools import raises

project = [
    {'name': 'web', 'image': 'busybox:latest'},
    {'name': 'db', 'image': 'busybox:latest'},
]


class TestBash(unittest.TestCase):

    def setUp(self):
        mock_client = mock.create_autospec(docker.Client)
        mock_client.containers.return_value = self.mock_container('test_web_1')
        self.project = Project.from_dicts('test', project, mock_client)

    def mock_container(self, name):
        return [{
            'Name': name, 'Names': [name], 'Id': name,
            'Image': 'busybox:latest'
        }]

    def test_bash(self):
        with mock.patch('os.system') as call:
            bash(self.project, {'SERVICE': 'web'})
        call.assert_called_with('docker exec -t -i test_web_1 /bin/bash')

    @raises(NoSuchService)
    def test_no_service(self):
        bash(self.project, {'SERVICE': 'foo'})

    @raises(NoContainer)
    def test_no_container(self):
        mock_client = mock.create_autospec(docker.Client)
        mock_client.containers.return_value = self.mock_container('nope_1')
        self.project = Project.from_dicts('test', project, mock_client)
        bash(self.project, {'SERVICE': 'web'})
