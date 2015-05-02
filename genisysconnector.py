#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import post, run
from dockermanager import DockerManager
import errno


@post('/service/<service_name>/create')
def create_service(service_name):
    try:
        service_definition = services[service_name]
        print ("Service definition found: %s" % service_definition)
        docker.create_service_container(service_definition)
    except KeyError:
        print ("Service definition not found for service %s" % service_name)


def load_services_from_file(filename):
    services = {}
    try:
        exec(compile(open(filename, "rb").read(), filename, 'exec'),
             {},
             services)
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("Missing services definitions file. Aborting.")
            raise
        else:
            print("An error occured while trying to read \
                services definitions. Aborting.")
            raise
    return services


if __name__ == '__main__':
    services = load_services_from_file("services.py")
    docker = DockerManager('unix://var/run/docker.sock')
    run(host='localhost', port=8080)
