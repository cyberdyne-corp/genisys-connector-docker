========
HTTP API
========

The connector exposes a HTTP API. It can be used to perform CRUD actions on services and also to trigger remote procedure calls to manage containers.

NOTE: The examples use the `httpie CLI`_ to query the API.

Service HTTP endpoint
=====================

The following endpoints are exposed:

* :ref:`service-endpoint`: List service definitions or register a new service definition
* :ref:`service-name-endpoint`: Retrieve or update a service definition
* :ref:`service-scale-endpoint`: Ensure a number of containers are running for a service
* :ref:`service-status-endpoint`: Return the number of running resources for a service

.. _service-endpoint:

``/service``
------------

This endpoint is used to list service definitions or to create a new service definition.

It supports the following methods: POST and GET.

When hitting the endpoint with a GET, it returns a JSON body like this:

.. code-block:: javascript

  {
    "myServiceA" = {
  	  "name": "myServiceA"
  	  "image": "docker_image:tag",
  	  "command": "command",
  	  "environment": {
  		  "ENV_VARIABLE_A": "value",
  		  "ENV_VARIABLE_B": "value",
  	  },
  	  "ports": ['8080']
    },
    "myServiceB" = {
  	  "name": "myServiceB"
  	  "image": "docker_image:tag",
  	  "ports": ['5000', '5001'],
  	  "command": null,
  	  "environment": null,
    }
  }

When hitting the endpoint with a POST, it expects a JSON request body that must look like:

.. code-block:: javascript

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

The *name* and *image* fields are mandatory.

The *name* field is used to identify the service.

The *image* field specifies the reference of the container image used when creating/stopping containers. The image tag must be included.

The *command* field specifies which command should be used when starting a container.

The *environment* field is used to inject environment variables into the containers associated with the service.

The *ports* field is used to expose a list of ports on the Docker host.

Example:

.. code-block:: bash

  $ http POST :7051/service name="helloworld" image="tutum/hello-world:latest" ports:='["8080", "8081"]' environment:='{"VAR_A":"value", "VAR_B": "value"}'

.. _service-name-endpoint:

``/service/<service_name>``
---------------------------

This endpoint is used to retrieve a service definition or to update it.

It supports the following methods: PUT and GET.

When hitting the endpoint with a GET, it returns a JSON body like this:

.. code-block:: javascript

    {
      "image": "tutum/hello-world:latest",
      "name": "helloworld"
      "command": null,
      "environment": null,
      "ports": null,
    }

When hitting the endpoint with a PUT, it expects a JSON request body that must look like:

.. code-block:: javascript

  {
    "image": "tutum/hello-world:latest",
    "command": "/run.sh",
    "environment": {
  	  "VAR_A": "value"
    },
    "ports": ['8080'],
  }

The *image* field is mandatory.

The *image* field specifies the image to use when starting/killing containers. The image tag must be included.

The *command* field specifies which command should be used when starting a container.

The *environment* field is used to inject environment variables into the containers associated with the service.

The *ports* field is used to expose a list of ports on the Docker host.

Example:

.. code-block:: bash

  $ http PUT :7051/service/helloworld image="panamax/hello-world-php:latest" command="/run.sh" ports:='["8080", "8082"]' environment:='{"VAR_A":"value", "VAR_B": "value"}'

.. _service-scale-endpoint:

``/service/<service_name>/scale``
---------------------------------

This endpoint is used to ensure that a specific number of containers associated to a service are running.

It expects a JSON request body to be POST.

The request body must look like:

.. code-block:: javascript

  {
    "number": number_of_containers,
  }

The *number* field is mandatory.

Example:

.. code-block:: bash

  $ http POST :7051/service/helloworld/scale number=3


.. _service-status-endpoint:

``/service/<service_name>/status``
----------------------------------

This endpoint returns the number of running resources for a service managed by this connector.

When hitting the endpoint with a GET, it returns a JSON body like this:

.. code-block:: javascript

  {
    "running_resources": number_of_running_resources,
  }

.. _httpie CLI: https://github.com/jakubroztocil/httpie
