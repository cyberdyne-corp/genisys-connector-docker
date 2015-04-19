from docker import Client
import json


class DockerManager:

    def __init__(self, docker_url):
        self.client = Client(docker_url)

    def list_containers(self):
        containers = self.client.containers()
        return json.dumps(containers)
