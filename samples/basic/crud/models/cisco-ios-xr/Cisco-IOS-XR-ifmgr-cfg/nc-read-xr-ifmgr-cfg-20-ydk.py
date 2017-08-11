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
Read all data for model Cisco-IOS-XR-ifmgr-cfg.

Outputs is to emulate the CLI show command

usage: show-config-interfaces-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg \
    as xr_ifmgr_cfg
from datetime import timedelta
import logging

def process_interface_configurations(interface_configurations):
    spacing = 0
    show_interface_config = str()
    
    # iterate over interface configurations
    for interface_configuration in interface_configurations.interface_configuration:
        show_interface_config = show_interface_config + '\n' + \
                                (' ' * spacing) + \
                                "interface " + \
                                interface_configuration.interface_name
                                
        spacing += 1
        if interface_configuration.vrf:
            show_interface_config = show_interface_config + '\n' + \
                                    (' ' * spacing) + \
                                    "vrf " + interface_configuration.vrf
        if interface_configuration.ipv4_network.addresses.primary:
            show_interface_config = show_interface_config + '\n' + \
                                    (' ' * spacing) + \
                                    "ipv4 address " + \
                                    interface_configuration.ipv4_network.addresses.primary.address
            
            show_interface_config = show_interface_config + \
                                    " " + \
                                    interface_configuration.ipv4_network.addresses.primary.netmask
                                    
            for secondary in interface_configuration.ipv4_network.addresses.secondaries.secondary:
                show_interface_config = show_interface_config + '\n' + \
                                    (' ' * spacing) + \
                                    "ipv4 address " + \
                                    secondary.address
        if interface_configuration.ipv6_network.addresses.regular_addresses:
            for regular_address in \
                interface_configuration.ipv6_network.addresses.regular_addresses.regular_address:
                
                show_interface_config = show_interface_config + '\n' + \
                                    (' ' * spacing) + \
                                    "ipv6 address " + \
                                    regular_address.address
                
                show_interface_config = show_interface_config + \
                                    "/" + \
                                    str(regular_address.prefix_length)
                                    
        if interface_configuration.shutdown:
            show_interface_config = show_interface_config + '\n' + \
                                    (' ' * spacing) + \
                                    "shutdown"
        spacing -= 1
        show_interface_config = show_interface_config + '\n' + \
                                (' ' * spacing) + \
                                "!"
    # return formatted string
    return(show_interface_config)


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

    interface_configurations = xr_ifmgr_cfg.InterfaceConfigurations()  # create object

    # read data from NETCONF device
    interface_configurations = crud.read(provider, interface_configurations)
    print(process_interface_configurations(interface_configurations))  # process object data

    provider.close()
    exit()
# End of script
