#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2011-2013   Marcus Popp                        marcus@popp.mx
# Copyright 2016-       Martin Sinn                         m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

import logging
import os

import lib.config
from lib.constants import PLUGIN_PARSE_LOGIC

logger = logging.getLogger(__name__)


class Logics():

    def __init__(self, smarthome, userlogicconf, envlogicconf):
        logger.info('Start Logics')
        self._sh = smarthome
        self._workers = []
        self._logics = {}
        self._bytecode = {}
        self.alive = True
        _config = {}
        _config.update(self._read_logics(envlogicconf, smarthome._env_dir))
        _config.update(self._read_logics(userlogicconf, smarthome._logic_dir))

        for name in _config:
            logger.debug("Logic: {}".format(name))
            logic = Logic(self._sh, name, _config[name])
            if hasattr(logic, 'bytecode'):
                self._logics[name] = logic
                self._sh.scheduler.add(name, logic, logic.prio, logic.crontab, logic.cycle)
            else:
                continue
            # plugin hook
            for plugin in self._sh._plugins:
                if hasattr(plugin, PLUGIN_PARSE_LOGIC):
                    update = plugin.parse_logic(logic)
                    if update:
                        logic.add_method_trigger(update)
            # item hook
            if hasattr(logic, 'watch_item'):
                if isinstance(logic.watch_item, str):
                    logic.watch_item = [logic.watch_item]
                for entry in logic.watch_item:
                    for item in self._sh.match_items(entry):
                        item.add_logic_trigger(logic)

    def _read_logics(self, filename, directory):
        logger.debug("Reading Logics from {}.*".format(filename))
        config = lib.config.parse_basename(filename, configtype='logics')
        if config != {}:
            for name in config:
                if 'filename' in config[name]:
                    config[name]['filename'] = directory + config[name]['filename']
        return config

    def __iter__(self):
        for logic in self._logics:
            yield logic

    def __getitem__(self, name):
        if name in self._logics:
            return self._logics[name]


class Logic():

    def __init__(self, smarthome, name, attributes):
        self._sh = smarthome
        self.name = name
        self.enabled = True if 'enabled' not in attributes else bool(attributes['enabled'])
        self.crontab = None
        self.cycle = None
        self.prio = 3
        self.last = None
        self.conf = attributes
        self.__methods_to_trigger = []
        if attributes != 'None':
            for attribute in attributes:
                vars(self)[attribute] = attributes[attribute]
            self.prio = int(self.prio)
            self.generate_bytecode()
        else:
            logger.error("Logic {} is not configured correctly (configuration has no attibutes)".format(self.name))
        

    def id(self):
        return self.name

    def __str__(self):
        return self.name

    def __call__(self, caller='Logic', source=None, value=None, dest=None, dt=None):
        if self.enabled:
            self._sh.scheduler.trigger(self.name, self, prio=self.prio, by=caller, source=source, dest=dest, value=value, dt=dt)

    def enable(self):
        self.enabled =True

    def disable(self):
        self.enabled = False

    def trigger(self, by='Logic', source=None, value=None, dest=None, dt=None):
        if self.enabled:
            self._sh.scheduler.trigger(self.name, self, prio=self.prio, by=by, source=source, dest=dest, value=value, dt=dt)

    def generate_bytecode(self):
        if hasattr(self, 'filename'):
            if not os.access(self.filename, os.R_OK):
                logger.warning("{}: Could not access logic file ({}) => ignoring.".format(self.name, self.filename))
                return
            try:
                code = open(self.filename, encoding='UTF-8').read()
                code = code.lstrip('\ufeff')  # remove BOM
                self.bytecode = compile(code, self.filename, 'exec')
            except Exception as e:
                logger.exception("Exception: {}".format(e))
        else:
            logger.warning("{}: No filename specified => ignoring.".format(self.name))

    def add_method_trigger(self, method):
        self.__methods_to_trigger.append(method)

    def get_method_triggers(self):
        return self.__methods_to_trigger

