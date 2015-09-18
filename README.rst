Genisys connector for Docker
============================

.. image:: https://badge.imagelayers.io/cyberdynesystems/genisys-connector-docker:latest.svg
   :target: https://imagelayers.io/?images=cyberdynesystems/genisys-connector-docker:latest
   :alt: imagelayers.io
.. image:: https://readthedocs.org/projects/genisys-connector-docker/badge/?version=stable
   :target: http://genisys-connector-docker.readthedocs.org/en/latest/?badge=stable
   :alt: Documentation Status


This component allows `Genisys`_ to communicate with a Docker engine.

Goals
-----

* Manage (scale up/down) resources associated to a service using containers.
* Retrieve running containers associated to a service.

Quick start
-----------

Start this component using Docker:

.. code-block:: bash

    $ docker run -p "7051:7051" cyberdynesystems/genisys-connector-docker:latest

Override the configuration file:

.. code-block:: bash

    $ docker run -p "7051:7051" -v "/path/to/config/genisys-connector.yml:/app/genisys-connector.yml" cyberdynesystems/genisys-connector-docker:latest

Documentation
-------------

`On readthedocs.org`_ or in the ``docs/source`` directory.

.. _On readthedocs.org: http://genisys-connector-docker.readthedocs.org/en/latest/
.. _Genisys: https://github.com/cyberdyne-corp/genisys
