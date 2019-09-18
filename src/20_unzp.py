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
# 20_unzp.py : unzip zip files in ZIP_DIR to XML_DIR in preparation for
#              xml parsing and further injestion
# -----------------------------------------------------------------------------

from edl.resources import log
from edl.resources import state
from edl.resources import zp
import json
import logging
import os
import sys
import zipfile as zf

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
def config():
    """
    config = {
            "source_dir"    : location of zip files
            "working_dir"   : location to unzip xml files to
            "state_file"    : fqpath to a file that lists unzipped files
            }
    """
    cwd                     = os.path.abspath(os.path.curdir)
    zip_dir                 = os.path.join(cwd, "zip")
    xml_dir                 = os.path.join(cwd, "xml")
    state_file              = os.path.join(xml_dir, "state.txt")
    config = {
            "source_dir"    : zip_dir,
            "working_dir"   : xml_dir,
            "state_file"    : state_file
            }
    return config



# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def run(logger, manifest, config):
    resource_name   = manifest['name']
    xml_dir         = config['working_dir']
    zip_dir         = config['source_dir']
    state_file      = config['state_file']
    resource_url    = manifest['url']
    new_files = state.new_files(resource_name, state_file, zip_dir, '.zip')
    log.debug(logger, {
        "name"      : __name__,
        "method"    : "run",
        "resource"  : resource_name,
        "url"       : resource_url,
        "xml_dir"   : xml_dir,
        "zip_dir"   : zip_dir,
        "state_file": state_file,
        "new_files_count" : len(new_files),
        })
    state.update(
            zp.unzip(
                resource_name,
                new_files,
                zip_dir,
                xml_dir),
            state_file)


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
        "src"       : "20_unzp.py"
        })
    with open('manifest.json', 'r') as json_file:
        m = json.load(json_file)
        run(logger, m, config())
