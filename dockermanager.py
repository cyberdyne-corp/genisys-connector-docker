from docker import Client


class DockerManager:

    def __init__(self, docker_url):
        self.client = Client(docker_url)

    def create_service_container(self, service_definition):
        try:
            command = service_definition["command"]
        except KeyError:
            command = None
        container = self.client.create_container(
            image=service_definition["image"],
            command=command)
        self.client.start(container.get('Id'))

    def stop_service_container(self, service_definition):
        containers = self.client.containers()
        for container in containers:
            if container["Image"] == service_definition["image"]:
                self.client.kill(container["Id"])
