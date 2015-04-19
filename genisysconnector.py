#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run
from dockermanager import DockerManager


@route('/resources', method='GET')
def list():
    containers = docker.list_containers()
    return containers

docker = DockerManager('unix://var/run/docker.sock')
run(host='localhost', port=8080)
