# Genisys connector for Docker

Allows the genisys component to communicate with Docker.

## Setup

Install bottle (assuming you got a Python >= 3.4 devel environment ready):

````
$ pip install bottle docker-py
````

## Run

Run it:

````
$ python genisysconnector.py
````

## Query

The component exposes a `/resources` endpoint to manage Docker containers.

Query the running containers:

````
$ curl http://localhost:8080/resources
````