# Genisys connector for Docker

Allows the genisys component to communicate with Docker.

## Setup

Install the requirements (assuming you got a Python >= 3.4 devel environment ready):

````
$ pip install -r requirements.txt
````

## Definitions

You must define each service you'll want to manage in a file called *services.py*.

Use the following format for each service definition:

```
myServiceName = {
	"image": "MY_DOCKER_IMAGE_NAME:TAG",
    "command": "MY_DOCKER_COMMAND",
}
```

You must specify the image and the command used to start the container.

## Run

Run it:

````
$ python genisysconnector.py
````

## Query

The component exposes multiple endpoints to manage services as Docker containers.

Start a service container:

````
$ curl http://localhost:8080/service/myServiceName/start
````

Kill a service container:

````
$ curl http://localhost:8080/service/myServiceName/kill
````
