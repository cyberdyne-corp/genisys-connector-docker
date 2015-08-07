from docker import Client, utils


class DockerManager:

    def __init__(self, docker_url):
        self.client = Client(docker_url)

    def count_containers_by_image(self, container_image):
        containers = self.client.containers()
        service_container_count = 0
        for container in containers:
            if container["Image"] == container_image:
                service_container_count += 1
        return service_container_count

    def stop_container_by_image(self, container_image):
        containers = self.client.containers()
        for container in containers:
            if container["Image"] == container_image:
                self.client.kill(container["Id"])
                break

    def create_container(self, service_definition):
        try:
            command = service_definition["command"]
        except KeyError:
            command = None

        container = self.client.create_container(
            image=service_definition["image"],
            command=command,
            ports=service_definition["ports"],
            environment=service_definition["environment"],
            host_config=utils.create_host_config(publish_all_ports=True))
        self.client.start(container.get('Id'))

    def ensure_containers_for_service(self,
                                      service_definition,
                                      container_number):
        service_container_count = self.count_containers_by_image(
            service_definition["image"])
        while service_container_count != container_number:
            if service_container_count > container_number:
                self.stop_container_by_image(service_definition["image"])
                service_container_count -= 1
            elif service_container_count < container_number:
                self.create_container(service_definition)
                service_container_count += 1
