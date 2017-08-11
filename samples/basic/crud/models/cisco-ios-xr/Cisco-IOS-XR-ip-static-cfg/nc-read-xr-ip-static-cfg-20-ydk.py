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
Read all data for model Cisco-IOS-XR-ip-static-cfg.

Outputs is to emulate the CLI show command

usage: show-config-static-route-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ip_static_cfg \
    as xr_ip_static_cfg
from datetime import timedelta
import logging

def process_router_static(router_static):
    spacing = 0
    """Process data in router_static object."""
    if router_static:
        show_router_static_config = str()
    else:
        show_router_static_config = "No static instances found"

    # ipv4 unicast routes
    spacing += 1
    if router_static.default_vrf.address_family.vrfipv4.vrf_unicast.vrf_prefixes.vrf_prefix:
        show_router_static_config = show_router_static_config + '\n' + \
                                    (' ' * spacing) + "address-family ipv4 unicast"
        spacing += 1
        for vrf in router_static.default_vrf.address_family.vrfipv4.vrf_unicast.vrf_prefixes.vrf_prefix:

            for interface in vrf.vrf_route.vrf_next_hop_table.vrf_next_hop_interface_name: 
                route_string = (' ' * spacing) + \
                                vrf.prefix + '/' + \
                                str(vrf.prefix_length) + \
                                ' ' + interface.interface_name
                show_router_static_config = show_router_static_config + '\n' + \
                                            route_string
        spacing -= 1
        show_router_static_config = show_router_static_config + \
                                    '\n' + (' ' * spacing) + '!'
       
    # ipv6 unicast routes    
    if router_static.default_vrf.address_family.vrfipv6.vrf_unicast.vrf_prefixes.vrf_prefix:
        show_router_static_config = show_router_static_config + '\n' + \
                                    (' ' * spacing) + "address-family ipv6 unicast"
        spacing += 1
        for vrf in router_static.default_vrf.address_family.vrfipv6.vrf_unicast.vrf_prefixes.vrf_prefix:
            
            for interface in vrf.vrf_route.vrf_next_hop_table.vrf_next_hop_interface_name: 
                route_string = (' ' * spacing) + \
                                vrf.prefix + '/' + \
                                str(vrf.prefix_length) + \
                                ' ' + interface.interface_name
                show_router_static_config = show_router_static_config + '\n' + \
                                            route_string
        spacing -= 1
        show_router_static_config = show_router_static_config + \
                                    '\n' + (' ' * spacing) +'!'
        
    spacing -= 1
    show_router_static_config = show_router_static_config + \
                                (' ' * spacing) +'\n!'
    # return formatted string
    if show_router_static_config.replace("!", "").strip() == "":
        return ""
    show_router_static_config = "router static" + show_router_static_config
    return(show_router_static_config)


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

    router_static = xr_ip_static_cfg.RouterStatic()  # create object

    # read data from NETCONF device
    router_static = crud.read(provider, router_static)
    print(process_router_static(router_static))  # process object data

    provider.close()
    exit()
# End of script
