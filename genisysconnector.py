#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import post, run
from dockermanager import DockerManager


@post('/service/<service_name>/create')
def create_service(service_name):
    try:
        service_definition = services[service_name]
        print ("Service definition found: %s" % service_definition)
        docker.create_service_container(service_definition)
    except KeyError:
        print ("Service definition not found for service %s" % service_name)

if __name__ == '__main__':
    services = {}
    exec(compile(open("services.py", "rb").read(), "services.py", 'exec'),
         {},
         services)
    docker = DockerManager('unix://var/run/docker.sock')
    run(host='localhost', port=8080)
