

# SmartHomeNG
[![Build Status on TravisCI](https://travis-ci.org/smarthomeNG/smarthome.svg?branch=develop)](https://travis-ci.org/smarthomeNG/smarthome)
[![Join the chat at https://gitter.im/smarthomeNG/smarthome](https://badges.gitter.im/smarthomeNG/smarthome.svg)](https://gitter.im/smarthomeNG/smarthome?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This file contains basic information about the basic directories of SmartHomeNG.

Developer documentation (english) can be found on [www.smarthomeNG.de](https://www.smarthomeNG.de)

Additional information / documentation can be found in the [SmartHomeNG Wiki](https://github.com/smarthomeNG/smarthome/wiki). The Wiki ist in german for the greatest part.

| directory | description|
| ---     | :--- |
|bin 	  | the main python file is based here |
|dev 	  | if you plan to create a plugin then this is the folder you want to have a closer look at |
|etc 	  | the three basic configuration files smarthome.conf, plugin.conf and logic.conf are located here, you will edit these files to reflect your basic settings|
|examples |	some examples of items, etc. this is only for informational purpose |
|items 	  | put here your own files for your items |
|lib 	  | some more core python modules are in this directory. You won't need to change anything here
|logics   |	here your logic files are put
|modules  | here are all loadable core-modules located (one subdirectory for every module)
|plugins  | here are all plugins located (one subdirectory for every plugin)
|scenes   | the scenes are stored here
|tools    | there are some tools which help you for creating an initial configuration 
|var 	  | everything that is changed by smarthome is put here, e.g. logfiles, cache, sqlite database etc.

## Some more detailed info on the configuration files

### etc/smarthome.conf (deprecated) / etc/smarthome.yaml
Upon installation you will need to create this file and specify your location.

```
# smarthome.conf (deprecated)
# look e.g. at http://www.mapcoordinates.net/de
lat = 52.52
lon = 13.40
elev = 36
tz = 'Europe/Berlin'
```

```yaml
# smarthome.yaml
# look e.g. at http://www.mapcoordinates.net/de
lat: '52.52'
lon: '13.40'
elev: 36
tz: Europe/Berlin
```

### etc/plugin.conf (deprecated) / etc/plugin.yaml
Upon installation you will need to create this file and configure the plugins and their attributes. 
An example is shown below

```
[knx]
   class_name = KNX
   class_path = plugins.knx
   host = 127.0.0.1
   port = 6720
#   send_time = 600 # update date/time every 600 seconds, default none
#   time_ga = 1/1/1 # default none
#   date_ga = 1/1/2 # default none
[ow]
    class_name = OneWire
    class_path = plugins.onewire
[visu]
    class_name = WebSocket
    class_path = plugins.visu_websocket
[smartvisu]
    class_name = SmartVisu
    class_path = plugins.visu_smartvisu
    smartvisu_dir = /var/www/html/smartVISU
[cli]
    class_name = CLI
    class_path = plugins.cli
    ip = 0.0.0.0
    update = True
[sql]
    class_name = SQL
    class_path = plugins.sqlite
```

```yaml
knx:
    class_name: KNX
    class_path: plugins.knx
    host: 127.0.0.1
    port: 6720

# send_time = 600 # update date/time every 600 seconds, default none
# time_ga = 1/1/1 # default none
# date_ga = 1/1/2 # default none
ow:
    class_name: OneWire
    class_path: plugins.onewire

visu:
    class_name: WebSocket
    class_path: plugins.visu_websocket

smartvisu:
    class_name: SmartVisu
    class_path: plugins.visu_smartvisu
    smartvisu_dir: /var/www/html/smartVISU

cli:
    class_name: CLI
    class_path: plugins.cli
    ip: 0.0.0.0
    update: 'True'

sql:
    class_name: SQL
    class_path: plugins.sqlite
```

### etc/logic.conf (deprecated) / etc/logic.yaml
In the logic.conf you specify your logics and when they will be run. An example is shown below

```
# etc/logic.conf (deprecated)
[AtSunset]
    filename = sunset.py
    crontab = sunset
```

```yaml
# etc/logic.yaml
AtSunset:
    filename: sunset.py
    crontab: sunset
```

### items/
This directory contains one or more item configuration files. The filename does not matter, except it has to end with '.conf'.

```
# items/global.conf (deprecated)
[global]
    [[sun]]
        type = bool
        attribute = foo
```

```yaml
# items/global.yaml
global:
    sun:
        type: bool
        attribute: foo
```

### logics/
This directory contains your logic files. Simple or sophisitcated python scripts. You could address your smarthome item by `sh.item.path`.
If you want to read an item call `sh.item.path()` or to set an item `sh.item.path(Value)`.

```
# logics/sunset.py
if sh.global.sun():       # if sh.global.sun() == True:
    sh.gloabl.sun(False)  # set it to False
```

