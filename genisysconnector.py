#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import post, get, put, run, abort, request
from utils import load_services_from_file, load_configuration
from dockermanager import DockerManager


@get('/service')
def retrieve_service_definitions():
    return services


@post('/service')
def create_service_definition():
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
    try:
        service_definition = services[service_name]
        return service_definition
    except KeyError:
        abort(501, 'Undefined service: %s.' % service_name)


@put('/service/<service_name>')
def update_service_definition(service_name):
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
    config = load_configuration('genisys-connector.yml')
    services = load_services_from_file(config['connector']['service_file'])
    docker = DockerManager(config['docker']['url'])
    run(host=config['connector']['bind'],
        port=config['connector']['port'])
