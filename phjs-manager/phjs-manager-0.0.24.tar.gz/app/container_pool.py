from docker_adapter import DockerAdapter
from string import Template


class ContainerPool:
    """Class for managing pool of containers"""
    ports_pool = []

    def __init__(self, socket_path, image_path, run_command, start_port):
        self.adapter = DockerAdapter(socket_path)
        self.image_path = image_path
        self.run_command = Template(run_command)
        self.start_port = start_port

    def instantiate_node(self):
        print(0)
        current_port = len(self.ports_pool) + self.start_port
        print(1)
        self.ports_pool.append(current_port)
        print(2)
        command = self.run_command.substitute(exposed_port = current_port)
        print(3)
        self.adapter.run_container(self.image_path, command, current_port)
        print(4)

    def get_node_list(self):
        return self.adapter.get_nodes()

