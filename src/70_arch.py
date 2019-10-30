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
# 70_arch.py : archive distribution to s3
# -----------------------------------------------------------------------------

from edl.resources import log
from edl.cli import feed as clifeed
from edl.resources import state
import json
import logging
import sys
import shutil
import os

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
def config():
    """
    config = {
                "wasabi_bwlimit"        : [rclone] Bandwidth limit in kBytes/s, or use suffix b|k|M|G or a full timetable.
                "digitalocean_bwlimit"  : [rclone] Bandwidth limit in kBytes/s, or use suffix b|k|M|G or a full timetable.
            }
    """
    config = {
            "wasabi_bwlimit"        : "500K",
            "digitalocean_bwlimit"  : "500K"            
            }
    return config


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def run(logger, manifest, config):
    resource_name           = manifest['name']
    wasabi_bandwidth_limit  = config['wasabi_bwlimit']
    digitalocean_bandwidth_limit = config['digitalocean_bwlimit']
    log.info(logger, {
        "name"      : __name__,
        "method"    : "run",
        "resource"  : resource_name,
        "message"   : "archiving...",
        })
    ed_path = os.path.dirname(os.path.dirname(os.path.abspath(os.curdir)))
    for output in clifeed.archive_to_s3(logger, resource_name, ed_path, "wasabi", wasabi_bandwidth_limit):
        log.info(logger, {
            "name"      : __name__,
            "method"    : "run",
            "resource"  : resource_name,
            "service"   : "wasabi",
            "stdout"   : str(output),
            })
    for output in clifeed.archive_to_s3(logger, resource_name, ed_path, "digitalocean", digitalocean_bandwidth_limit):
        log.info(logger, {
            "name"      : __name__,
            "method"    : "run",
            "resource"  : resource_name,
            "service"   : "digitalocean",
            "stdout"   : str(output),
            })
    shutil.rmtree(os.path.join(os.curdir, 'dist'))

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
        "src"       : "70_arch.py"
        })
    with open('manifest.json', 'r') as json_file:
        m = json.load(json_file)
        run(logger, m, config())
