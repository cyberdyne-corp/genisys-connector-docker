=============
Configuration
=============

Configuration file
==================

The configuration file *genisys-connector.yml* is written in `YAML format`_.

.. code-block:: yaml

    connector:
      # Server address to bind to.
      bind: 127.0.0.1

      # Application port
      port: 7051

      # Path to compute definitions
      service_file: ./services.py

    docker:
      # URL of the Docker server
      url: unix://var/run/docker.sock


Connector section
-----------------

This section is related to the connector configuration.

``bind``
^^^^^^^^

The server address to bind to.

``port``
^^^^^^^^

The port that will be used to communicate with the connector via HTTP.

.. _config-service-file:

``service_file``
^^^^^^^^^^^^^^^^

A python file that defines an optional list of services that will be loaded by the connector during startup.

See :ref:`service-definition` below for more information on the format of the file.

Docker section
--------------

This section is related to the Docker engine.

``url``
^^^^^^^^

The URL of the Docker engine.

Can be either a path to the Docker engine socket or an URL to the Docker API.

.. _service-definition:

Service definition
==================

In order to manage Docker containers for a service, the adapter provides a simple service definition format
to declare how to manage containers associated with a service.

A service definition looks like:

.. code-block:: python

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

A service definition must include a *name* and an *image*, it may optionally provide a *command*, an *environment* hash and an array of *ports*.

The *image* field is used to start a container, if the *command* field has been specified the container will be started using that command.
The image tag **must** be specified.

The *image* field is also used when stopping containers, the image is used as reference to search in running containers.

The *environment* field is used to inject environment variables into the containers associated with the service.

The *ports* field is used to expose a list of ports on the Docker host.

An optional *service_file* (see :ref:`config-service-file`) can be used to define services using the format defined above. These definitions will be loaded during the connector startup.

.. _YAML format: https://en.wikipedia.org/wiki/YAML
