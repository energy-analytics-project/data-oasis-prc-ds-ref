#! /usr/bin/env python3
# edl : common library for the energy-dashboard tool-chain
# Copyright (C) 2019  Todd Greenwood-Geer (Enviro Software Solutions, LLC)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# -----------------------------------------------------------------------------
# 50_save.py : save state files
# -----------------------------------------------------------------------------

from edl.resources import log
from edl.resources import state
from edl.resources import save
import logging
import os
import sys
import json

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
def config():
    """
    config = {
            "source_dir"    : location of the databases
            "working_dir"   : location of the state file
            "state_file"    : fqpath to file that lists the created database files
            }
    """
    cwd                     = os.path.abspath(os.path.curdir)
    db_dir                  = os.path.join(cwd, "db")
    save_dir                = os.path.join(cwd, "save")
    state_file              = os.path.join(save_dir, "state.txt")
    config = {
            "source_dir"    : db_dir,
            "working_dir"   : save_dir,
            "state_file"    : state_file,
            }
    return config


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def run(logger, manifest, config):
    resource_name   = manifest['name']
    db_dir          = config['source_dir']
    save_dir        = config['working_dir']
    state_file      = config['state_file']

    log.info(logger, {
        "name"      : __name__,
        "method"    : "run",
        "resource"  : resource_name,
        "db_dir"    : db_dir,
        "save_dir"  : db_dir,
        "state_file": state_file,
        "message"   : "started saving state",
        })

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        log.info(logger, {
            "name"      : __name__,
            "method"    : "run",
            "resource"  : resource_name,
            "db_dir"    : db_dir,
            "save_dir"  : db_dir,
            "state_file": state_file,
            "message"   : "created save dir",
            })

    save.git_add_and_commit(logger, resource_name)

    log.info(logger, {
        "name"      : __name__,
        "method"    : "run",
        "resource"  : resource_name,
        "db_dir"    : db_dir,
        "save_dir"  : db_dir,
        "state_file": state_file,
        "message"   : "finished saving state",
        })

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        loglevel = sys.argv[1]
    else:
        loglevel = "INFO"
    log.configure_logging()
    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)
    log.debug(logger, {
        "name"      : __name__,
        "method"    : "main",
        "src"       : "50_save.py"
        })
    with open('manifest.json', 'r') as json_file:
        m = json.load(json_file)
        run(logger, m, config())
