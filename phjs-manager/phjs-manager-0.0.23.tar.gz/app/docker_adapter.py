from docker import Client
from docker.utils import utils


class DockerAdapter:
    """Adapter for docker api"""
    def __init__(self, base_url):
        self.dockerClient = Client(base_url=base_url)

    def run_container(self, image_path, run_command, port_bind):
        self.dockerClient.create_container(
            image=image_path,
            command=run_command, detach=True,
            host_config=utils.create_host_config(
                network_mode="host"
            )
        )

    def get_nodes(self):
        return self.dockerClient.containers()
