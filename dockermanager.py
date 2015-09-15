"""Docker management module.
Exposes a class to manage Docker containers using the Python SDK.
"""

from docker import Client, utils


class DockerManager:
    """The DockerManager provides a way to manage a Docker engine."""

    def __init__(self, docker_url):
        """docker_url is the URL to the docker engine. It can either be the URL
        to the docker engine API or a path to the Docker socket.
        """
        self.client = Client(docker_url)

    def count_containers_by_image(self, container_image):
        """Iterates through all running containers to count the number
        of running containers associated with a container image name.
        Returns the number of running container.
        """
        containers = self.client.containers()
        service_container_count = 0
        for container in containers:
            if container['Image'] == container_image:
                service_container_count += 1
        return service_container_count

    def stop_container_by_image(self, container_image):
        """Iterates through all running containers to stop the first
        container that match a container image name.
        """
        containers = self.client.containers()
        for container in containers:
            if container['Image'] == container_image:
                self.client.kill(container['Id'])
                break

    def create_container(self, service_definition):
        """Creates a new container based on a service definition object."""
        container = self.client.create_container(
            image=service_definition['image'],
            command=service_definition['command'],
            ports=service_definition['ports'],
            environment=service_definition['environment'],
            host_config=utils.create_host_config(publish_all_ports=True))
        self.client.start(container.get('Id'))

    def ensure_containers_for_service(self,
                                      service_definition,
                                      container_number):
        """Ensures that a number of container are running for a service.
        Based on the *container_number* parameter it will stop/create
        containers to match this value.
        """
        service_container_count = self.count_containers_by_image(
            service_definition['image'])
        while service_container_count != container_number:
            if service_container_count > container_number:
                self.stop_container_by_image(service_definition['image'])
                service_container_count -= 1
            elif service_container_count < container_number:
                self.create_container(service_definition)
                service_container_count += 1
