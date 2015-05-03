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
}
````

A service definition must include a *name* and an *image*, it may optionally provide a *command*.

The *image* field is used to start a container, if the *command* field has been specified the container will be started using that command.
The *image* field is also used when killing a container, the adapter will search for every running container using this image and will kill one.

You can specify an optional file called *services.py* at the root of the project and use it to define services using the format defined above. 

## HTTP API

The adapter exposes a RESTful HTTP API. It can be used to perform CRUD actions on services and also to start/kill container.

Note: The examples use the httpie CLI to query the API, see: https://github.com/jakubroztocil/httpie

### Service HTTP endpoint

The following endpoints are exposed:

* [/service](#service-1) : Register a new service defintion
* [/service/\<service_name\>](#serviceservice_name) : Retrieve or update a service definition
* [/service/\<service_name\>/start](#serviceservice_namestart) : Start a new container for a service
* [/service/\<service_name\>/kill](#serviceservice_namekill) : Kill a container associated to a service

#### /service

This endpoint is used to create a new service definition.

It expects a JSON request body to be POST. The request body must look like:

````
{
	"name": "service_name",
	"image": "docker_image:tag",
	"command": "command"
}
````

The *name* and *image* fields are mandatory.

The *name* field is used to identify the service.

The *image* field specifies the image to use when starting/killing containers. The image tag must be included.

The *command* field specifies which command should be used when starting a container.

Example:

````
$ http POST :7051/service name="helloworld" image="tutum/hello-world:latest"
````

#### /service/\<service_name\>

This endpoint is used to retrieve a service definition or to update it.

It supports the following methods: PUT and GET.

When hitting the endpoint with a GET, it returns a JSON body like this:

````
{
    "image": "tutum/hello-world:latest", 
    "name": "helloworld"
}
````

When hitting the endpoint with a PUT, it expects a JSON request body that must look like:

````
{
	"image": "panamax/hello-world-php:latest",
	"command": "/run.sh"
}
````

The *image* field is mandatory.

The *image* field specifies the image to use when starting/killing containers. The image tag must be included.

The *command* field specifies which command should be used when starting a container.

Example:

````
$ http PUT :7051/service/helloworld image="panamax/hello-world-php:latest" command="/run.sh"
````

#### /service/\<service_name\>/start

This endpoint is hit with a GET and is used to start a container associated to a service.

The return code is 200 on success.

Example:

````
$ http :7051/service/helloworld/start
````

#### /service/\<service_name\>/kill

This endpoint is hit with a GET and is used to kill a running container associated to a service.

The return code is 200 on success.

Example:

````
$ http :7051/service/helloworld/kill
````
