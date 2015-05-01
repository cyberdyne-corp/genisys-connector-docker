#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import get, run
from dockermanager import DockerManager


@get('/resources')
def list():
    containers = docker.list_containers()
    return containers

if __name__ == '__main__':
    config = {}
    execfile("services.py", config)
    docker = DockerManager('unix://var/run/docker.sock')
    run(host='localhost', port=8080)
