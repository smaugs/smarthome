
=============
Configuration
=============

Filesystem Structure of SmartHomeNG
===================================

After the base system is installed a closer look at the SmartHomeNG directory 
(e.g. ``/usr/local/smarthome/``) is advised to learn something about its content:

.. code-block:: bash
   :emphasize-lines: 6,8,10

   # directories
   bin            contains smarthome.py, the main application
   deprecated     contains deprecated tools, which will be removed in an upcoming release of SmartHomeNG
   dev            development files like a sample plugin
   doc            the documentation of the project resides here
   etc            should contain the basic configuration files (smarthome.yaml, plugin.yaml, logic.yaml)
   examples       contains some example files for the configuration and the visu plugin
   items          should contain one or more item configuration files.
   lib            contains the core libraries of SmartHomeNG
   logics         should contain the logic scripts
   media          contains logos of SmartHomeNG
   modules        loadable core modules. These modules extend the functionality of the core
   plugins        contains the available plugins
   requirements   you will find the requirements file here for the core and all plugins
   scenes         scene files
   tests          contains the test environment with tests and testdata
   tools          contains little programs helping to maintain SmartHomeNG
   var            its subdirectories contain various collected data
   var/cache      contains cached item values
   var/db         may contain a SQLite3 database
   var/log        contains the logfiles
   var/rrd        may contain a Round Robin Databases if rrd plugin is used (deprecated)
   
   # files
   CHANGELOG.md   changes of this project. (deprecated, should be documented in doc)
   LICENSE        GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)
   README.md      a general information
   setup.py       not functional right now
   tox.ini        used for software testing

Important for configuration are the directories ``etc``, ``items`` and ``logics``.
Those are the locations were configuration is stored and maintained.
The following discusses how these directories are populated.


directory *etc*: Config files
=============================

The configuration is done by the widespread `yaml <https://en.wikipedia.org/wiki/YAML>`_ format. 
Older versions used `configobj <http://www.voidspace.org.uk/python/articles/configobj.shtml>`_ file format which is like a well-known `ini-file <https://en.wikipedia.org/wiki/INI_file>`_ but with the ability to create multilevel sub-sections.
It is still supported in SmartHomeNG but it is deprecated now and only displayed here for informational purposes.

If ``ruamel.yaml`` is installed and the backend-plugin is configured then a service can be used to convert the old ``*.conf`` format into ``*.yaml`` format for code snippets.

There is however a service tool at ``tools/conf_to_yaml_converter.py`` that can be used to convert your whole configuration. Please have a look at :doc:`tools`.


.. _`smarthome.yaml`:

smarthome.yaml
--------------

To calculate sunrise, sunset, azimuth and elevation of the sun for a given time the coordinates of the physical location
of the SmartHomeNG installation is needed.

.. sidebar:: smarthome.conf
   :class: deprecated
   
   .. code-block:: ini
   
      # /usr/local/smarthome/etc/smarthome.conf
      lat = 51.1633        # latitude
      lon = 10.4476        # longitude
      elev = 500           # elevation
      tz = 'Europe/Berlin' # timezone, the example will be fine for most parts of central Europe

Create a new ``smarthome.yaml`` within ``etc/`` or copy the given ``smarthome.yaml.default`` 
to ``smarthome.yaml`` and edit it to your needs. It should look like the following:
      
.. code-block:: yaml
   :caption: smarthome.yaml

   lat: 51.1633         # latitude
   lon: 10.4476         # longitude
   elev: 500            # elevation
   tz: Europe/Berlin    # timezone, the example will be fine for most parts of central Europe
   default_language: de # default language for use with the backend plugin and multi-language entries in metadata

The coordinates can be found out by using GPS of a mobile or via an adequate website (e.g. http://www.mapcoordinates.net/)
   
.. _`logic.yaml`:

logic.yaml
----------

Logics within SmartHomeNG are just Python scripts like the core, too. These scripts will be
placed in `/usr/local/smarthome/logics/`. To let SmartHomeNG know about when to start a script and which script to use then
it is needed to configure every logic script in `logic.yaml`:

.. sidebar:: logic.conf
   :class: deprecated
   
   .. code-block:: ini
   
      [MyLogic]
          filename = logic.py
          crontab = init

.. code-block:: yaml
   :caption: logic.yaml
   
   MyLogic:
       filename: logic.py
       crontab: init

With the example above SmartHomeNG would look in ``/usr/local/smarthome/logics/`` for the file
``logic.py``. The logic would be started - once - when SmartHomeNG starts.


.. _`plugin.yaml`:

plugin.yaml
-----------

Plugins extend the core functionality of SmartHomeNG. 
The ``plugins`` directory contains a subdirectory for every available plugin.
The file ``etc/plugin.yaml`` holds the configuration for every plugin to be used during runtime.

For each plugin at least the plugin object name is needed and the
attributes where to find the plugin and how to expect the classname to be.

The example below configures a plugin for the KNX bus to send and receive telegrams from and to eibd or knxd (both a software gateway to the KNX hardware bus).
In this case the object name is ``knx``, the place to look for the module is within subdirectory ``plugins/knx/`` and the class of the plugin is ``KNX``.
The object name can be any valid Python name, the class name and class path need to match those of the plugin.


.. sidebar:: plugin.conf
   :class: deprecated
   
   .. code-block:: ini
   
      [knx]
         class_name = KNX
         class_path = plugins.knx
         host = 127.0.0.1
         port = 6720
      #   send_time = 600 # update date/time every 600 seconds, default none
      #   time_ga = 1/1/1 # default none
      #   date_ga = 1/1/2 # default none

.. code-block:: yaml
   :caption: plugin.yaml
   
   knx:
       class_name: KNX
       class_path: plugins.knx
       host: 127.0.0.1
       port: 6720
       # send_time; 600 # update date/time every 600 seconds, default none
       # time_ga: 1/1/1 # default none
       # date_ga: 1/1/2 # default none

There is a `README.md` for every plugin that gives the necessary configuration information.
To continue reading follow the :doc:`plugin <plugins_all>` page.

logging.yaml
------------

The core and also every module is able to output logging information. 
The logging can be configured to be rich in detail for debugging purposes or rather smart with warning or general info.
There is a seperate document to explain how to configure :doc:`logging <logging>`.
To get started, simply copy the given ``logging.yaml.default`` 
to ``logging.yaml`` and edit it to your needs. It should look like the following:

.. literalinclude:: ../../etc/logging.yaml.default
   :caption: logging.yaml
   :language: yaml

See further details at :doc:`logging <logging>`.

.. _`item configuration files`:


directory *items*: Config files containing item definitions
===========================================================

The items represent the heart of the configuration. An item can be accessed from any logic, plugin or eval.
Any number of item configuration files may be used and any number of items may be defined (depends on your memory) in one of these files.

This directory contains yaml files with the definitions of the items SmartHomeNG can use. The yaml files can be named
the way you want.

To find out more details about items and scenes configuration continue reading the :doc:`items <items>` page.


directory *logics*: Config files containing item definitions
============================================================

This directory contains logics you write, which are used by SmartHomeNG.


SmartHomeNG start options
=========================

SmartHomeNG can be executed with the following options:

.. code-block:: bash

   usage: smarthome.py [-h] [-v | -d | -i | -l | -s | -q | -V | --start]
   optional arguments:
     -h, --help         show this help message and exit
     -v, --verbose      DEPRECATED use logging.config (verbose (debug output)
                        logging to the logfile)
     -d, --debug        stay in the foreground with verbose output
     -i, --interactive  open an interactive shell with tab completion and with
                        verbose logging to the logfile
     -l, --logics       reload all logics
     -s, --stop         stop SmartHomeNG
     -q, --quiet        DEPRECATED use logging config (reduce logging to the
                        logfile)
     -V, --version      show SmartHomeNG version
     --start            start SmartHomeNG and detach from console (default)

If you start SmartHomeNG without any option, then SmartHomeNG will return the PID if already running.

Please be noted that due to the changed nature of logging the -v and -q options are deprecated and will be removed
in a later release.

