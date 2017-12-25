#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2017-     Martin Sinn                           m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG.
#  https://github.com/smarthomeNG/smarthome
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
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import os
import subprocess

# Update auf 1.3d wg. neuer item features on_update, on_change
# Update auf 1.3e wg. neuer logic features for visu_websocket
# Update auf 1.3f wg. Vorbereitung Release Candidate

# Update auf 1.4a wg. Kennzeichnung des Stands als "nach dem v1.4 Release"
# Update auf 1.4b wg. Kennzeichnung des Stands als "nach dem v1.4.1 Release"

shNG_version = '1.4b'

# ---------------------------------------------------------------------------------
FileBASE = None

def _get_git_data(sub='', printout=False):
    global FileBASE
    if FileBASE is None:
        FileBASE = os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-2])
    BASE = FileBASE
    if sub != '':
        BASE = os.path.join(FileBASE,sub)
    commit = '0'
    branch = 'manual'
    describe = ''
    commit_short = ''
    if BASE is not None:
        try:
            os.chdir(BASE)
            branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.STDOUT).decode().strip('\n')
            commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.STDOUT).decode().strip('\n')
            commit_short = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], stderr=subprocess.STDOUT).decode().strip('\n')
            describe = subprocess.check_output(['git', 'describe', '--all'], stderr=subprocess.STDOUT).decode().strip('\n')
        except Exception as e:
            pass
    if printout:
        print()
        print("_get_git_data: BASE={}".format(BASE)) 
        print("- describe: {}".format(describe))
        print("- commit_short : {}".format(commit_short))
        print("- commit .: {}".format(commit))
        print("- branch .: {}".format(branch))
        print()
    return commit, commit_short, branch, describe 

# ---------------------------------------------------------------------------------

def get_shng_main_version():
    return shNG_version

def get_shng_version():
    commit, commit_short, branch, describe = _get_git_data()
    VERSION = get_shng_main_version()
    if branch == 'master':
        VERSION += '.'+branch+' ('+commit_short+')'
    else:
        VERSION += '.'+commit_short+'.'+branch
    return VERSION

def get_shng_description():
    commit, commit_short, branch, describe = _get_git_data()
    return describe

def get_plugins_version():
    commit, commit_short, branch, describe = _get_git_data('plugins')
    VERSION = get_shng_main_version()
    if branch == 'master':
        VERSION += '.'+branch+' ('+commit_short+')'
    else:
        VERSION += '.'+commit_short+'.'+branch
    return VERSION

def get_plugins_description():
    commit, commit_short, branch, describe = _get_git_data('plugins')
    return describe

def get_shng_docversion():
    commit, commit_short, branch, describe = _get_git_data()
    VERSION = get_shng_main_version()
    if branch != 'master':
        VERSION += ' '+branch
    return VERSION

if __name__ == '__main__':
    print()
    commit, commit_short, branch, describe = _get_git_data()
    print("get_shng_git         :", commit+'.'+branch)
    commit, commit_short, branch, describe = _get_git_data('plugins')
    print("get_plugins_git      :", commit+'.'+branch)
    print()
    print("get_shng_main_version:", get_shng_main_version())
    print("get_shng_version     :", get_shng_version())
    print(" - description       :", get_shng_description())
    print("get_plugins_version  :", get_plugins_version())
    print(" - description       :", get_plugins_description())
    print()

