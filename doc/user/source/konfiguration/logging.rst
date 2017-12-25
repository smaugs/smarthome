..index:: Logging

#######
Logging
#######

Zur Konfiguration des Loggings mit SmartHomeNG wird seit der Version 1.2 eine Konfigurationsdatei 
im YAML Format verwendet.


Konfiguration des Loggings
==========================

Die Datei **../etc/logging.yaml** befindet sich bereits vorkonfiguriert in dem Verzeichnis.

Die Datei sieht so aus:

.. code-block:: yaml
   :caption: ../etc/logging.yaml
   
   version: 1
   disable_existing_loggers: False
   formatters:
     simple:
       format: '%(asctime)s %(levelname)-8s %(threadName)-12s %(message)s'
       datefmt: '%Y-%m-%d  %H:%M:%S'
     detail:
       format: '%(asctime)s %(levelname)-8s %(module)-12s %(threadName)-12s %(message)s -- %(filename)s:%(funcName)s:%(lineno)d'
       datefmt: '%Y-%m-%d %H:%M:%S'
   handlers:
     console:
       class: logging.StreamHandler
       formatter: simple
       stream: ext://sys.stdout
     file:
       class: logging.handlers.TimedRotatingFileHandler
       level: DEBUG
       formatter: detail
       when: midnight
       backupCount: 7
       filename: ./var/log/smarthome.log
   loggers:
     plugins.knx:
       level: DEBUG
   #  lib.scheduler:
   #    level: DEBUG
   #  plugins.cli:
   #    level: DEBUG
   root:
       level: INFO
       handlers: [file, console]


In die Konfigurationsmöglichkeiten des Phyton Loggings kann sich hier eingelesen werden:
https://docs.python.org/3.4/library/logging.html#module-logging

Die Datei **../etc/logging.yaml** hat kein SmartHomeNG spezifisches Format. Sie wird mit der 
Funktion `logging.config.dictConfig()` (Bestandteil der Python Standardbibliothek) eingelesen. 

Informationen zu dieser Python Funktion und den damit verbundenen Möglichkeiten gibt es hier: 
https://docs.python.org/3.4/library/logging.config.html#module-logging.config

Kurzdoku der Einträge in der Konfigurationsdatei
------------------------------------------------

Die einzelnen Konfigurationseinträge haben die folgende Bedeutung:

+-----------------+------------------------------------------------------------------------------------------------+
| **Abschnitte**  | Bedeutung                                                                                      |
+-----------------+------------------------------------------------------------------------------------------------+
| **formatters:** | Definiert das Ausgabeformat der einzelnen Loggingeinträge. Mehrere unterschiedliche            |
|                 | **formatter** können dazu verwendet werden um unterschiedlich aussehende Logdateien            |
|                 | zu erzeugen. In der Konfigurationsdatei **etc/logging.yaml** sind die Formatter                |
|                 | **`simple`** und **`detail`** vorkonfiguriert. Weitere Formatter können bei Bedarf             |
|                 | hinzugefügt werden.                                                                            |
+-----------------+------------------------------------------------------------------------------------------------+
| **handlers:**   | Handler definieren die Log-Behandlungsroutinen/Ausgabekanäle die verwendet werden.             |
|                 | In Python gibt es bereits mehrere vorimplementierte und mächtige Handler-Typen die             |
|                 | `hier <https://docs.python.org/3.4/library/logging.handlers.html#module-logging.handlers>`_    |
|                 | beschrieben sind. Als eigentliche Handler sind in der Konfigurationsdatei **etc/logging.yaml** |
|                 | die Handler **`console`** und **`file`** vordefiniert. Wenn Log-Einträge z.B. in eine andere   |
|                 | Datei geschrieben werden sollen, muss ein weiterer Handler definiert werden.                   |
+-----------------+------------------------------------------------------------------------------------------------+
| **loggers:**    | Hier werden die einzelnen Logger definiert und was mit diesen Einträgen passiert,              |
|                 | welche Handler und formatter verwendet werden. Das Level konfiguriert dabei die                |
|                 | Logtiefe für die einzelne Komponente. Bei den loggern ist es nun möglich einzelne              |
|                 | Plugins oder Libs im Debug protokollieren zu lassen. Dazu sind in der Konfiguration            |
|                 | bereits einige Beispiele.                                                                      |
+-----------------+------------------------------------------------------------------------------------------------+
| **root:**       | Hier ist die Konfiguration des Root-Loggers der für die ganze Anwendung gilt. Dieser           |
|                 | Root-Logger wird für alle Komponente verwendet die nicht unter loggers: konfiguriert sind.     |
+-----------------+------------------------------------------------------------------------------------------------+

Wenn man **Logger** definiert, welche die Log-Einträge über zusätzliche **Handler** ausgeben ist 
zu beachten, dass die Ausgabe zusätzlich IMMER durch den Standardhandler (**file:**) erfolgt. Dieses 
führt dazu, dass die Einträge sowohl in der Standard Log-Datei von SmartHomeNG, als auch in der 
zusätzlich definierten Log Datei erscheinen, falls der Level des Log Eintrages INFO oder höher ist.

Wenn man möchte, dass im Standard Log nur WARNINGS und ERRORS erscheinen, muss ein zusätzlicher 
Eintrag im Handler **file:** erfolgen. Der Eintrag `level: WARNING` führt dazu, dass über den 
Handler **file:** nur Ausgaben für Fehler und Warnungen erfolgen. INFO und DEBUG Ausgaben erfolgen 
dann nur noch über den zusätzlichen Handler.

Pluginentwicklung
=================

Für die Entwickler von Plugins:
Der Logger sollte nun nicht global mit logging.getLogger('') instanziert werden sondern innerhalb 
der &#95;&#95;init&#95;&#95; Methode mit:

.. code-block:: python

   self.logger = logging.getLogger(__name__)


Wobei &#95;&#95;name&#95;&#95; ein sogenanntes magic ist. Dies bedeutet, dass python 
aus &#95;&#95;name&#95;&#95; den Namen des Plugins macht. 

So wird aus plugins/cli/ der Name „plugins.cli“, aus lib/scheduler.py wird „lib.scheduler“
Daher muss dann in der Konfiguration des Loggings der Name „plugin.cli“ angegeben werden.
Verwendet man zur Instanziierung einen eigenen Namen wie z.B. 

.. code-block:: python

   self.logger = logging.getLogger('DWD')


muss in der config auch dieser Name verwendet werden. Ohne `plugin.`

.. code-block:: yaml
   :caption: ../etc/logging.yaml

   loggers:
       DWD:
           level: DEBUG
       

Auf den Logger kann dann so zugegriffen werden:

.. code-block:: python

   self.logger.debug("")
   self.logger.info("")


Beispiel:

.. code-block:: python

   def __init__(self, smarthome, update='False', ip='127.0.0.1', port=2323):
       self.logger = logging.getLogger(__name__)
       # Logger verwenden:
       self.logger.debug("Debug Message")


Best Practices
--------------

Wer eine brauchbare leicht konfigurierbare Logging Konfiguration sucht, der wird hier 
:doc:`Logging - Best Practices <logging_best_practices>` fündig.


.. toctree::
   :maxdepth: 4
   :hidden:
   :titlesonly:
   
   logging_best_practices.md
   
