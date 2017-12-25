:tocdepth: 6

###########
SmartHomeNG
###########

Anwenderdokumentation
=====================

SmartHomeNG ist ein System das als Metagateway zwischen verschiedenen "Dingen" fungiert und 
dient der Verbindung unterschiedlicher Geräte-Schnittstellen. Die Standard-Schnittstelle eines 
Gerätes wird durch das Metagateway so um viele zusätzliche Schnittstellen erweitert. So ist es 
möglich dass die Klingel mit der Musikanlage und TV spricht, und dessen Wiedergabe unterbricht 
oder bei Abwesenheit eine Nachricht per Email verschickt.

Viele haben in die Konfiguration Ihres Smarthome.py Systems viel Arbeit gesteckt und wollen 
das jetzt nicht aufgeben und wieder etwas komplett neues machen. So wurde ein Fork smarthomeNG 
erstellt um die Fortentwicklungen im System wieder zusammenzuführen und eine Basis für 
Weiterentwicklungen zu stellen.

Diese Dokumentation reflektiert das aktuelle Release |release|.


Die Entwickler-Dokumentation (für Entwickler von Plugins und den Core von SmartHomeNG), sowie
die READMEs der Plugins sind in Englisch gehalten.
 
Die hier entstehende Anwenderdokumentation ist auf Deutsch. Später wird sie zweisprachig Deutsch/Englisch
zur Verfügung stehen. Sie wird sich aus Inhalten speisen, die zurzeit im `SmartHomeNG Wiki <https://github.com/smarthomeNG/smarthome/wiki>`_
zur Verfügung stehen.

Hilfe zu SmartHomeNG gibt es im `Supportforum im KNX-User-Forum <https://knx-user-forum.de/forum/supportforen/smarthome-py>`_ 
oder im `Chat auf gitter.im <https://gitter.im/smarthomeNG/smarthome>`_ .

.. note::

   **Anmerkungen** und **Änderungswünsche** zu dieser Anwenderdokumentation bitte auf  
   `dieser Wiki Seite <https://github.com/smarthomeNG/smarthome/wiki/Anwender-Dokumentation---Kommentare>`_ hinterlassen.



.. toctree::
   :maxdepth: 5
   :hidden:
   :titlesonly:
   
   einleitung.md
   installation/installation.rst
   konfiguration/konfiguration.rst
   plugins_all.rst
   logiken/logiken.rst
   visualisierung/visualisierung.rst
   backend/backend.rst
   tools/tools.rst
   fehlersuche
   faq
   entwickler_doku
   release
   genindex
