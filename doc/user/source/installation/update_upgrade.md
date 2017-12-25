# Update von einer älteren Version

Es kann verschiedene Szenarien geben von denen aus man ein Update machen möchte. Es gibt unterschiedliche Ansätze wenn es sich um eine Virtuelle Maschine handelt oder wenn ein Raspberry Pi upgedated werden soll. Es gibt hier leider nicht **die** Methode. Leider gibt es derzeit auch keine Systemübergreifende Backup Methode. Es ist also ein wenig ein Stückwerk.


## Gedanken zu Distributionsupgrade

Bei Linux Betriebsystemversionen gibt es tiefgreifende Änderungen, was die Systemdienste betrifft. Gab es bei älteren Systemen wie Debian 7 (Wheezy) oder Ubuntu 14.x noch die init-Skripte, so ist bei neuen Systemen wie Debian 8 (Jessie) oder Ubuntu 15 ein neuer Ansatz gefunden worden: **systemd**
Die Art und Weise wie Systemunterbauten für SmartHomeNG laufen haben sich also grundlegend angepaßt. Als __alter Linuxhase__ ist das sicher mit einem Distributionsupgrade schnell erledigt aber dann kommen noch solche Dinge wie Umstellung von **eibd** auf **knxd** dazu.
Es kann also sinnvoll sein ein frisch installiertes System auf Basis SmartHomeNG einem aktualisierten System vorzuzuiehen. In diesem Fall müssen nur die Konfigurationen vom SmartHomeNG angepaßt und die smartVISU Dateien rüberkopiert werden. Zusätzlich sind noch die Dateien der SQLite zu migrieren.

Grundsätzlich empfiehlt sich, vor dem Update von SmarthomeNG auf eine aktuelle Linux-Distribution upzudaten. Einige Funktionen (z.B. das Backend) könnten sonst evtl. nicht funktionieren. Für ein Update von Raspian Wheezy auf Jessie findet sich [hier](https://www.elektronik-kompendium.de/sites/raspberry-pi/2005051.htm) eine gute Anleitung. Zusätzlich müssen noch die [in der Komplettanleitung](https://github.com/smarthomeNG/smarthome/wiki/Komplettanleitung#smarthomeng-installieren) unter Vorbedingungen angegebenen Programme und auf der selben Seite weiter unten beschriebenen Python-Pakete (ephem, pyyaml, ...) installiert werden.

## Update von SmarthomeNG ab V1.1 und höher

Wenn man SmarthomeNG laut der [Komplettanleitung](https://github.com/smarthomeNG/smarthome/wiki/Komplettanleitung) (mithilfe "git clone [...]") installiert hat, in das Verzeichnis "smarthome" wechseln und anschliessend

```
git pull
```

eingeben. Daraufhin sollte der Update-Vorgang starten. 

Nachdem SmartHomeNG aktualisiert wurde, müssen noch die als Submodule eingebundenen **Plugins aktualisiert** werden. Dazu das folgende Kommando eingeben:

```
git submodule update --init
```



Zum Abschluss SmarthomeNG dann starten. Um zu prüfen, ob sich vielleicht Fehler oder Änderungen in den Plugins ergeben haben, sollte man dies im Debugmodus von der Kommandozeile aus machen:

```
python3 bin/smarthome.py -d
```

Jetzt heißt es genau zu schauen, was an **Warning** oder **Error** gemeldet wird. Logfiles findet man auch im Verzeichnis  ``../var/log`` (in der Standardinstallation unter ``/usr/local/smarthome/var/log``). Von da aus kann man sie mit einem Editor in Ruhe anschauen und auf Fehler durchsuchen.
Alternativ kann man ab SmartHomeNG Version 1.2 auch im Backend schauen. Dort werden die Logfiles aufgelistet.

Wenn dann die Konfiguration stimmt, kann man natürlich den automatischen Neustart von SmartHomeNG wieder einschalten. In der Komplettanleitung ist beschrieben, welche Schritte dafür bei Verwendung von systemd durchgeführt werden müssen.

Möchte man vom alten *.conf [Format der Konfigurationsdateien](https://github.com/smarthomeNG/smarthome/wiki/Configuration-Files) (die wohl absehbar auch nicht weiter unterstützt werden) auf das neue *.yaml Format umschwenken, so kann der im Verzeichnis ``../tools`` bereitgestellte Konverter ``conf_to_yaml_converter.py`` genutzt werden um das automatisch zu tun.

Nacharbeiten empfehlen sich auf jeden Fall für Item Attribute deren Werte als String erwartet werden, die aufgrund ihrer Struktur aber als float eingelesen werden. Ein prominentes Beispiel sind Onewire Adressen.

**PS:**
Wer sich ein wenig mit GitHub beschäftigen möchte, dem sei [diese Seite](https://rogerdudler.github.io/git-guide/index.de.html) empfohlen.

## Anpassen der Repositories

Wenn man Smarthome noch mit git aus dem alten Repository installiert hat (z.B. wie in einer der Komplettanleitungen beschrieben), verweisen die Pfade noch dorthin. Man kann aber recht einfach auf das neue Repository von SmartHomeNG umstellen. Dazu zunächst ins Unterverzeichnis vom smarthome wechseln (kann auf Raspi auch anders sein, z.B. /usr/smarthome) auf den Stand prüfen:

```
cd /usr/local/smarthome
git remote -v
```
Als Anzeige erscheint im Falle des alten Repositories:

```
origin  https://github.com/mknx/smarthome (fetch)
origin  https://github.com/mknx/smarthome (push)
```

Jetzt werden die URLs neu gesetzt (die zweite Zeile gegebenenfalls entsprechend der vorhergehenden Ausgabe von git remote -v anpassen):

```
git remote set-url origin --add https://github.com/smarthomeNG/smarthome
git remote set-url --delete origin  https://github.com/mknx/smarthome
git remote -v
```

Als Rückmeldung bekommt man nun:

```
origin  https://github.com/smarthomeNG/smarthome (fetch)
origin  https://github.com/smarthomeNG/smarthome (push)
```
Jetzt kann man mit `git pull` den neue Stand herunterladen. Das Ergebnis sieht in etwa so aus:

```
remote: Counting objects: 12, done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 12 (delta 2), reused 1 (delta 1), pack-reused 0
Unpacking objects: 100% (12/12), done.
From https://github.com/smarthomeNG/smarthome
   57c1163..8534021  develop    -> origin/develop
Updating 57c1163..8534021
```

### Fehlerquellen

Es ist besser, das bisherige Verzeichnis ``/usr/local/smarthome`` zunächst z.B. in ``/usr/local/smarthome.old`` umzubenennen und ein neues Verzeichnis ``/usr/local/smarthome`` für SmarthomeNG anzulegen. Es sind nur wenige Ordner, die dann einfach in die neue Version kopiert werden müssen (etc, items, logics...), sonst hat git später Probleme mit Updates.

Es kann sein, dass in der alten Version der automatische Start von smarthome.py anders erfolgt ist, wie jetzt in der Komplettanleitung beschrieben. Dann muss man die alte Startsystematik noch entfernen.