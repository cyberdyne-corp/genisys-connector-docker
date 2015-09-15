#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Entry point for the connector.
It will start an a web server to expose a HTTP API based on the configuration
defined in the configuration file.
"""

from bottle import post, get, put, run, abort, request
from utils import load_services_from_file, load_configuration
from dockermanager import DockerManager


@get('/service')
def retrieve_service_definitions():
    """Exposes the /service endpoint accessible via a GET method.
    Used to retrieve the service definitions as JSON.
    """
    return services


@post('/service')
def create_service_definition():
    """Exposes the /service endpoint accessible via a POST method.
    Used to create a new service definition.

    It expects a JSON body that looks like:

    {
        "name": "service_name",
        "image": "docker_image:tag",
        "command": "command",
        "environment": {
                "ENV_VARIABLE_A": "value",
                "ENV_VARIABLE_B": "value",
            },
            "ports": ['port_number']
        }
    }

    The *name* and *image* fields are mandatory.

    The *name* field is used to identify the service.

    The *image* field specifies the reference of the container image used
    when creating/stopping containers. The image tag **must** be included.

    The *command* field specifies which command should be used when
    starting a container.

    The *environment* field is used to inject environment variables into
    the containers associated with the service.

    The *ports* field is used to expose a list of ports on the Docker host.
    """
    data = request.json
    if not data:
        abort(400, 'No data received')
    try:
        service_name = data['name']
        services[service_name] = {}
        services[service_name]['name'] = service_name
        services[service_name]['image'] = data['image']
    except KeyError:
        abort(400, 'Missing parameters.')
    services[service_name]['command'] = data.get('command', None)
    services[service_name]['environment'] = data.get('environment', None)
    services[service_name]['ports'] = data.get('ports', None)


@get('/service/<service_name>')
def retrieve_service_definition(service_name):
    """Exposes the /service/<service_name> endpoint accessible via a GET method.
    Used to retrieve the definition of a specific service as JSON.
    """
    try:
        service_definition = services[service_name]
        return service_definition
    except KeyError:
        abort(501, 'Undefined service: %s.' % service_name)


@put('/service/<service_name>')
def update_service_definition(service_name):
    """Exposes the /service/<service_name> endpoint accessible via a PUT method.
    Used to update the definition of an existing service.

    It expects a JSON body that looks like:
    {
        "image": "tutum/hello-world:latest",
        "command": "/run.sh",
        "environment": {
            "VAR_A": "value"
        },
        "ports": ['8080'],
    }
    The image field is mandatory.
    """
    data = request.json
    if not data:
        abort(400, 'No data received')
    try:
        services[service_name] = {}
        services[service_name]['name'] = service_name
        services[service_name]['image'] = data['image']
    except KeyError:
        abort(400, 'Missing parameter.')
    services[service_name]['command'] = data.get('command', None)
    services[service_name]['environment'] = data.get('environment', None)
    services[service_name]['ports'] = data.get('ports', None)


@post('/service/<service_name>/scale')
def scale_service(service_name):
    """Exposes the /service/<service_name>/scale endpoint accessible via
    a POST method.
    Used to scale the number of resources associated to a service.

    It expects a JSON body that looks like:
    {
        "number": number_of_containers,
    }
    """
    data = request.json
    if not data:
        abort(400, 'No data received')
    try:
        scale_number = int(data['number'])
    except KeyError:
        abort(400, 'Missing parameter.')
    except ValueError:
        abort(400, 'Invalid value for number parameter.')
    try:
        service_definition = services[service_name]
        docker.ensure_containers_for_service(service_definition, scale_number)
    except KeyError:
        abort(501, 'Undefined service: %s.' % service_name)


@get('/service/<service_name>/status')
def service_status(service_name):
    """Exposes the /service/<service_name>/status endpoint accessible via
    a GET method.
    Used to retrieve the number of running resources for a service as JSON.
    """
    try:
        service_definition = services[service_name]
        running_resources = docker.count_containers_by_image(
            service_definition['image'])
        response = {}
        response['running_resources'] = running_resources
        return response
    except KeyError:
        abort(501, 'Undefined service: %s.' % service_name)


if __name__ == '__main__':
    """Main method.
    Retrieve the configuration from the configuration file.
    It also retrieves the services from a service definition file.
    Finally, it creates a DockerManager instance and start the web server.
    """
    config = load_configuration('genisys-connector.yml')
    services = load_services_from_file(config['connector']['service_file'])
    docker = DockerManager(config['docker']['url'])
    run(host=config['connector']['bind'],
        port=config['connector']['port'])
