=====
Setup
=====

Docker
======

A public Docker image is available and can be used to start the component:

.. code-block:: bash

    $ docker run -p "7051:7051" cyberdynesystems/genisys-connector-docker:latest

Do not forget to map the port 7051 of the container to a specific port on the Docker host.

Overriding the configuration
----------------------------

You can map your own configuration file in the container file system:

.. code-block:: bash

    $ docker run -p "7051:7051" -v "/path/to/config/genisys-connector.yml:/app/genisys-connector.yml" cyberdynesystems/genisys-connector-docker:latest

From sources
============

Requirements
------------

Ensure you have *python* >= 3.4 and *git* installed on your system.

Installation
------------

Clone this repository and install the dependencies using **pip**:

.. code-block:: bash

    $ git clone https://github.com/cyberdyne-corp/genisys-connector-docker && cd genisys-connector-docker
    $ pip install -r requirements.txt


Start
-----

Start the connector:

.. code-block:: bash

    $ python main.py
