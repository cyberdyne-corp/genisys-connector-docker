# Genisys connector for Docker

Allows the genisys component to communicate with Docker.

Can manage services as containers.

## Setup

Install the requirements (assuming you got a Python >= 3.4 devel environment ready):

````
$ pip install -r requirements.txt
````

## Run

Start the adapter:

````
$ python genisysconnector.py
````

## Service definition

In order to manage Docker containers for a service, the adapter provides a simple service definition format
to declare how to manage containers associated with a service.

A service definition looks like:

````
myService = {
	"name": "myService"
	"image": "docker_image:tag",
  "command": "command",
	"environment": {
		"ENV_VARIABLE_A": "value",
		"ENV_VARIABLE_B": "value",
	},
	"ports": ['8080']
}
````

A service definition must include a *name* and an *image*, it may optionally provide a *command*, an *environment* hash and an array of *ports*.

The *image* field is used to start a container, if the *command* field has been specified the container will be started using that command.
The *image* field is also used when stopping containers, the image is used as reference to search in running containers.

The *environment* field is used to inject environment variables into the containers associated with the service.

The *ports* field is used to expose a list of ports on the Docker host.

You can specify an optional file called *services.py* at the root of the project and use it to define services using the format defined above.

## HTTP API

The adapter exposes a HTTP API. It can be used to perform CRUD actions on services and also to trigger remote procedure calls to manage containers.

Note: The examples use the httpie CLI to query the API, see: https://github.com/jakubroztocil/httpie

### Service HTTP endpoint

The following endpoints are exposed:

* [/service](#service-1) : List service definitions or register a new service definition
* [/service/\<service_name\>](#serviceservice_name) : Retrieve or update a service definition
* [/service/\<service_name\>/scale](#serviceservice_namescale) : Ensure a number of containers are running for a service

#### /service

This endpoint is used to list service definitions or to create a new service definition.

It supports the following methods: POST and GET.

When hitting the endpoint with a GET, it returns a JSON body like this:

````
{
	myServiceA = {
		"name": "myServiceA"
		"image": "docker_image:tag",
	  "command": "command",
		"environment": {
			"ENV_VARIABLE_A": "value",
			"ENV_VARIABLE_B": "value",
		},
		"ports": ['8080']
	},
	myServiceB = {
		"name": "myServiceB"
		"image": "docker_image:tag",
		"ports": ['5000', '5001'],
		"command": null,
		"environment": null,
	}
}
````

When hitting the endpoint with a POST, it expects a JSON request body that must look like:

````
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
````

The *name* and *image* fields are mandatory.

The *name* field is used to identify the service.

The *image* field specifies the reference of the container image used when creating/stopping containers. The image tag must be included.

The *command* field specifies which command should be used when starting a container.

The *environment* field is used to inject environment variables into the containers associated with the service.

The *ports* field is used to expose a list of ports on the Docker host.

Example:

````
$ http POST :7051/service name="helloworld" image="tutum/hello-world:latest" ports:='["8080", "8081"]' environment:='{"VAR_A":"value", "VAR_B": "value"}'
````

#### /service/\<service_name\>

This endpoint is used to retrieve a service definition or to update it.

It supports the following methods: PUT and GET.

When hitting the endpoint with a GET, it returns a JSON body like this:

````
{
    "image": "tutum/hello-world:latest",
    "name": "helloworld"
		"command": null,
		"environment": null,
		"ports": null,
}
````

When hitting the endpoint with a PUT, it expects a JSON request body that must look like:

````
{
	"image": "tutum/hello-world:latest",
	"command": "/run.sh",
	"environment": {
		"VAR_A": "value"
	},
	"ports": ['8080'],
}
````

The *image* field is mandatory.

The *image* field specifies the image to use when starting/killing containers. The image tag must be included.

The *command* field specifies which command should be used when starting a container.

The *environment* field is used to inject environment variables into the containers associated with the service.

The *ports* field is used to expose a list of ports on the Docker host.

Example:

````
$ http PUT :7051/service/helloworld image="panamax/hello-world-php:latest" command="/run.sh" ports:='["8080", "8082"]' environment:='{"VAR_A":"value", "VAR_B": "value"}'
````

#### /service/\<service_name\>/scale

This endpoint is used to ensure that a specific number of containers associated to a service are running.

It expects a JSON request body to be POST. The request body must look like:

````
{
	"number": number_of_containers,
}
````

The *number* field is mandatory.

Example:

````
$ http POST :7051/service/helloworld/scale number=3
````
