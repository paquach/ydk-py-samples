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
Read all data for model Cisco-IOS-XR-ipv4-ospf-cfg.

Outputs is to emulate the CLI show command

usage: show-config-ospf-ipv4-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_ospf_cfg \
    as xr_ipv4_ospf_cfg
from datetime import timedelta
import logging

def process_ospf(ospf):
    """Process data in ospf object."""
    spacing = 0
    if ospf.processes.process:
        show_ospf_config = str()
    else:
        show_ospf_config = ""
    
    for process in ospf.processes.process:
        show_ospf_config = show_ospf_config + '\n' + (' ' * spacing) + \
                           "router ospf " + process.process_name
        if process.distribute:
            show_ospf_config = show_ospf_config + '\n' + (' ' * spacing) + \
                           "distribute link-state"
        for area in process.default_vrf.area_addresses.area_area_id:
            spacing += 1
            show_ospf_config = show_ospf_config + '\n' + (' ' * spacing) + \
                               'area ' + str(area.area_id)
            for name in area.name_scopes.name_scope:
                spacing += 1
                show_ospf_config = show_ospf_config + '\n' + (' ' * spacing) + \
                                   'interface ' + name.interface_name
                show_ospf_config = show_ospf_config + '\n' + \
                                   (' ' * spacing) + '!' 
                spacing -= 1
            show_ospf_config = show_ospf_config + '\n' + \
                               (' ' * spacing) + '!'
            spacing -= 1
        show_ospf_config = show_ospf_config + '\n' + \
                           (' ' * spacing) + '!'
        
    
                
    # return formatted string
    return(show_ospf_config)


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

    ospf = xr_ipv4_ospf_cfg.Ospf()  # create object

    # read data from NETCONF device
    ospf = crud.read(provider, ospf)
    print(process_ospf(ospf))  # process object data

    provider.close()
    exit()
# End of script
