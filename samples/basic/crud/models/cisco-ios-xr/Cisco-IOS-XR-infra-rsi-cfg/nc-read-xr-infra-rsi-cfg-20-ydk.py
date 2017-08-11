#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Read all data for model Cisco-IOS-XR-ipv4-vrfs-oper.

Outputs is to emulate the CLI show command

usage: show-config-global-vrf-ydk.py [-h] [-v] device

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_infra_rsi_cfg \
    as xr_infra_rsi_cfg
from datetime import timedelta
import logging

def process_vrfs(vrfs):
    spacing = 0
    """Process data in vrfs object."""
    if vrfs:
        show_vrfs_config = str()
    else:
        return ""
    # iterate on vrfs
    for vrf in vrfs.vrf:
        show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + \
                           "vrf " + vrf.vrf_name
        
        # iterate on AFs
        spacing += 1
        for af in vrf.afs.af:
            show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + \
                               "address-family " + af.af_name.name + \
                               " " + af.saf_name.name
            
            #iterate on import route target
            spacing += 1
            if af.bgp.import_route_targets.route_targets.route_target:
                show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + \
                                   "import route-target " 
                spacing += 1
                for route_target in af.bgp.import_route_targets.route_targets.route_target:
                    for as_or_four_byte_as in route_target.as_or_four_byte_as:
                        show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + \
                                           str(as_or_four_byte_as.as_) + ":" + \
                                           str(as_or_four_byte_as.as_index)
                spacing -= 1
                show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + "!"
            spacing -= 1
            
            
            #iterate on export route target
            spacing += 1
            if af.bgp.export_route_targets.route_targets.route_target:
                show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + \
                                   "export route-target " 
                spacing += 1
                for route_target in af.bgp.export_route_targets.route_targets.route_target:
                    for as_or_four_byte_as in route_target.as_or_four_byte_as:
                        show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + \
                                           str(as_or_four_byte_as.as_) + ":" + \
                                           str(as_or_four_byte_as.as_index)
                spacing -= 1
                show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + "!"
            spacing -= 1
            
        show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + "!"
        spacing -= 1
        show_vrfs_config = show_vrfs_config + '\n' + (' ' * spacing) + "!"
    return(show_vrfs_config)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF provider
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)
    # create CRUD service
    crud = CRUDService()

    vrfs = xr_infra_rsi_cfg.Vrfs()  # create object

    # read data from NETCONF device
    vrfs = crud.read(provider, vrfs)
    print(process_vrfs(vrfs))  # process object data

    provider.close()
    exit()
# End of script
