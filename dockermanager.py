from docker import Client
import json


class DockerManager:

    def __init__(self, docker_url):
        self.client = Client(docker_url)

    def list_containers(self):
        containers = self.client.containers()
        return json.dumps(containers)

    def create_service_container(self, service_definition):
        container = self.client.create_container(
            image=service_definition["image"],
            command=service_definition["command"])
        self.client.start(container.get('Id'))
