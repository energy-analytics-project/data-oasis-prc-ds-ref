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
# 40_inse.py : parse resources from an xml file and insert into database
# -----------------------------------------------------------------------------

from edl.resources import db
from edl.resources import log
from edl.resources import state
import datetime as dt
import json
import logging
import os
import pprint
import sqlite3
import sys
import xml.dom.minidom as md
import shutil

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
def config():
    """
    config = {
            "source_dir"    : location of the xml files
            "working_dir"   : location of the database
            "state_file"    : fqpath to file that lists the inserted xml files
            "mem_mount"     : in memory file system
            }
    """
    cwd                     = os.path.abspath(os.path.curdir)
    sql_dir                 = os.path.join(cwd, "sql")
    db_dir                  = os.path.join(cwd, "db")
    state_file              = os.path.join(db_dir, "state.txt")
    config = {
            "source_dir"    : sql_dir,
            "working_dir"   : db_dir,
            "state_file"    : state_file,
            "mem_mount"     : "/mnt/ramdisk",
            }
    return config


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def run(logger, manifest, config):
    resource_name   = manifest['name']
    sql_dir         = config['source_dir']
    db_dir          = config['working_dir']
    state_file      = config['state_file']
    mem_mount       = config['mem_mount']
    new_files = state.new_files(resource_name, state_file, sql_dir, '.sql')
    log.info(logger, {
        "name"      : __name__,
        "method"    : "run",
        "resource"  : resource_name,
        "mem_mount" : str(mem_mount),
        "sql_dir"   : sql_dir,
        "db_dir"    : db_dir,
        "state_file": state_file,
        "new_files_count" : len(new_files),
        "message"   : "started processing sql files",
        })
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    if mem_mount is not None:
        mem_db_dir = os.path.join(mem_mount, resource_name)
        shutil.copytree(db_dir, mem_db_dir)
        try:
            state.update(db.insert(logger, resource_name, sql_dir, mem_db_dir, new_files), state_file)
        except:
            pass
        finally:
            temp_dir_name = "%s.temp" % db_dir
            shutil.move(mem_db_dir, temp_dir_name)
            shutil.rmtree(db_dir)
            os.rename(temp_dir_name, db_dir)
            log.info(logger, {
                "name"      : __name__,
                "method"    : "run",
                "resource"  : resource_name,
                "mem_mount" : mem_mount,
                "sql_dir"   : sql_dir,
                "db_dir"    : db_dir,
                "state_file": state_file,
                "new_files_count" : len(new_files),
                "message"   : "finished processing sql files",
                })
    else:
        state.update(db.insert(logger, resource_name, sql_dir, db_dir, new_files), state_file)
        log.info(logger, {
            "name"      : __name__,
            "method"    : "run",
            "resource"  : resource_name,
            "sql_dir"   : sql_dir,
            "db_dir"    : db_dir,
            "state_file": state_file,
            "new_files_count" : len(new_files),
            "message"   : "finished processing sql files",
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
        "src"       : "40_inse.py"
        })
    with open('manifest.json', 'r') as json_file:
        m = json.load(json_file)
        run(logger, m, config())
