from docker import Client


class DockerManager:

    def __init__(self, docker_url):
        self.client = Client(docker_url)

    def list_containers(self):
        return self.client.containers()
