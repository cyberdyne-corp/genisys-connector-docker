#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import post, get, put, run, abort, request
from dockermanager import DockerManager
import errno


@post('/service')
def create_service_definition():
    data = request.json
    if not data:
        abort(400, 'No data received')
    try:
        service_name = data["name"]
        services[service_name] = {}
        services[service_name]["name"] = service_name
        services[service_name]["image"] = data["image"]
    except KeyError:
        abort(400, 'Missing parameters.')
    try:
        services[service_name]["command"] = data["command"]
    except KeyError:
        pass


@get('/service')
def retrieve_service_definitions():
    return services


@put('/service/<service_name>')
def update_service_definition(service_name):
    data = request.json
    if not data:
        abort(400, 'No data received')
    try:
        services[service_name] = {}
        services[service_name]["name"] = service_name
        services[service_name]["image"] = data["image"]
    except KeyError:
        abort(400, 'Missing parameter.')
    try:
        services[service_name]["command"] = data["command"]
    except KeyError:
        pass


@get('/service/<service_name>')
def retrieve_service_definition(service_name):
    try:
        service_definition = services[service_name]
        return service_definition
    except KeyError:
        abort(501, "Undefined service: %s." % service_name)


@post('/service/<service_name>/scale')
def scale_service(service_name):
    data = request.json
    if not data:
        abort(400, 'No data received')
    try:
        scale_number = int(data["number"])
    except KeyError:
        abort(400, 'Missing parameter.')
    except ValueError:
        abort(400, 'Invalid value for number parameter.')
    try:
        service_definition = services[service_name]
        docker.ensure_containers_for_service(service_definition, scale_number)
    except KeyError:
        abort(501, "Undefined service: %s." % service_name)


def load_services_from_file(filename):
    services = {}
    try:
        exec(compile(open(filename, "rb").read(), filename, 'exec'),
             {},
             services)
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("No services definitions file provided.")
        else:
            print("An error occured while trying to read \
                services definitions file. Aborting.")
            raise
    return services


if __name__ == '__main__':
    services = load_services_from_file("services.py")
    docker = DockerManager('unix://var/run/docker.sock')
    run(host='localhost', port=7051)
