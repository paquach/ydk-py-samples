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
Read all data for model Cisco-IOS-XR-ipv4-bgp-cfg.

Outputs is to emulate the CLI show command

usage: show-config-bgp-ipv4-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_cfg \
    as xr_ipv4_bgp_cfg
from datetime import timedelta
import logging

def get_name(enum):
    #interpret enum
    return {
        0 : "IPv4 unicast",
        1 : "IPv4 multicast",
        2 : "IPv4 labeled-unicast",
        3 : "IPv4 tunnel",
        4 : "VPNv4 unicast",
        5 : "IPv6 unicast",
        6 : "IPv6 multicast",
        7 : "IPv6 labeled-unicast",
        8 : "VPNv6 unicast",
        9 : "IPv4 MDT",
        10 : "L2VPN VPLS-VPWS",
        11 : "IPv4 rt-filter",
        12 : "IPv4 MVPN",
        13 : "IPv6 MVPN",
        14 : "L2VPN EVPN",
        15 : "Link-state link-state"
    }.get(enum, "Error")

def process_bgp(bgp):
    """Process data in bgp object."""
    spacing = 0

    if bgp.instance:
        show_bgp_adj = str()
    else:
        show_bgp_adj = "No BGP instances found"
   
   # iterate over all instances
    for instance in bgp.instance:
        for instance_as in instance.instance_as:
            for four_byte_as in instance_as.four_byte_as:
                show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                               "bgp router " + str(four_byte_as.as_)
                show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                "bgp router-id " + \
                                str(four_byte_as.default_vrf.global_.router_id)
                
                # iterate over all global af
                for global_af in four_byte_as.default_vrf.global_.global_afs.global_af:
                    spacing += 1
                    show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                   "address family " + get_name(global_af.af_name.value)
                   
                    # check for interior configs
                    spacing += 1
                    if global_af.connected_routes:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "redistribute connected "
                        if global_af.connected_routes.route_policy_name:
                            show_bgp_adj = show_bgp_adj + "route policy " + \
                                           global_af.connected_routes.route_policy_name
                    if global_af.static_routes:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "redistribute static "
                        if global_af.static_routes.route_policy_name:
                            show_bgp_adj = show_bgp_adj + "route policy " + \
                                           global_af.static_routes.route_policy_name
                        
                    if global_af.vrf_all.label_mode.label_allocation_mode:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "vrf all"
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                       "label mode " + \
                                       str(global_af.vrf_all.label_mode.label_allocation_mode)
                        show_bgp_adj = show_bgp_adj + '\n' + \
                                       (' ' * spacing) + '!'
                    spacing -= 1
                    show_bgp_adj = show_bgp_adj + '\n' + \
                                   (' ' * spacing) + '!'
                    spacing -= 1  
                
                # iterate over neighbor groups
                for neighbor_group in four_byte_as.default_vrf.bgp_entity.neighbor_groups.neighbor_group:
                    spacing += 1 
                    show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                   "neighbor-group " + neighbor_group.neighbor_group_name
                    spacing += 1 
                    if neighbor_group.remote_as:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "remote-as " + str(neighbor_group.remote_as.as_xx) + \
                                        ":" + str(neighbor_group.remote_as.as_yy)
                    if neighbor_group.update_source_interface:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "update-source " + neighbor_group.update_source_interface
                    
                    # show the neighbor group AF information
                    for neighbor_group_af in neighbor_group.neighbor_group_afs.neighbor_group_af:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "address-family " + get_name(neighbor_group_af.af_name.value)
                        if neighbor_group_af.route_reflector_client:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                           "route-reflector-client"
                        if neighbor_group_af.route_policy_in:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                           "route-policy " + neighbor_group_af.route_policy_in + \
                                           " in"
                        if neighbor_group_af.route_policy_out:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                           "route-policy " + neighbor_group_af.route_policy_out + \
                                           " out"
                        show_bgp_adj = show_bgp_adj + '\n' + \
                                       (' ' * spacing) + '!'
                    spacing -= 1
                    show_bgp_adj = show_bgp_adj + '\n' + \
                                   (' ' * spacing) + '!'
                    spacing -= 1
            
                # iterate over neighbors
                for neighbor in four_byte_as.default_vrf.bgp_entity.neighbors.neighbor:
                    spacing += 1 
                    show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                   "neighbor " + neighbor.neighbor_address
                    spacing += 1 
                    if not(neighbor.remote_as.as_xx == None):
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "remote-as " + str(neighbor.remote_as.as_xx) + \
                                        ":" + str(neighbor.remote_as.as_yy)
                    if neighbor.update_source_interface:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "update-source " + neighbor.update_source_interface
                    if neighbor.neighbor_group_add_member:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "use neighbor-group " + neighbor.neighbor_group_add_member
                    
                    # check for neighbor AF
                    for neighbor_af in neighbor.neighbor_afs.neighbor_af:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "address-family " + get_name(neighbor_af.af_name.value)
                        if neighbor_af.route_policy_in:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                           "route-policy " + neighbor_af.route_policy_in + \
                                           " in"
                        if neighbor_af.route_policy_out:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                           "route-policy " + neighbor_af.route_policy_out + \
                                           " out"
                        show_bgp_adj = show_bgp_adj + '\n' + \
                                       (' ' * spacing) + '!'
                    spacing -= 1
                    show_bgp_adj = show_bgp_adj + '\n' + \
                                   (' ' * spacing) + '!'
                    spacing -= 1
                
                # iterate over bgp vrf
                for vrf in four_byte_as.vrfs.vrf:
                    spacing += 1
                    show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                   "vrf " + vrf.vrf_name
                    spacing += 1 
                    if vrf.vrf_global.route_distinguisher:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "rd " + str(vrf.vrf_global.route_distinguisher.as_xx) + \
                                        "." + str(vrf.vrf_global.route_distinguisher.as_)  + \
                                        ":" + str(vrf.vrf_global.route_distinguisher.as_index)
                    
                    # check for vrf AF
                    for vrf_global_af in vrf.vrf_global.vrf_global_afs.vrf_global_af:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "address-family " + get_name(vrf_global_af.af_name.value)
                        spacing += 1
                        if vrf_global_af.connected_routes:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                           "redistribute connected "
                            if vrf_global_af.connected_routes.route_policy_name:
                                show_bgp_adj = show_bgp_adj + "route policy " + \
                                               vrf_global_af.connected_routes.route_policy_name
                        if vrf_global_af.static_routes:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                           "redistribute static "
                            if vrf_global_af.static_routes.route_policy_name:
                                show_bgp_adj = show_bgp_adj + "route policy " + \
                                               vrf_global_af.static_routes.route_policy_name
                        if vrf_global_af.table_policy:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                           "table-policy " + vrf_global_af.table_policy
                        spacing -= 1
                        show_bgp_adj = show_bgp_adj + '\n' + \
                                       (' ' * spacing) + '!'
                    
                    # Check for vrf neighbors
                    for vrf_neighbor in vrf.vrf_neighbors.vrf_neighbor:
                        show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                       "neighbor " + vrf_neighbor.neighbor_address
                        spacing += 1
                        if vrf_neighbor.neighbor_group_add_member:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                           "use neighbor-group " + vrf_neighbor.neighbor_group_add_member
                        if not (vrf_neighbor.remote_as.as_xx == None):
                                show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                               "remote-as " + str(vrf_neighbor.remote_as.as_xx) + \
                                                ":" + str(vrf_neighbor.remote_as.as_yy)
                                                
                        # check for bgp vrf neighbor's AF
                        for vrf_neighbor_af in vrf_neighbor.vrf_neighbor_afs.vrf_neighbor_af:
                            show_bgp_adj = show_bgp_adj + '\n' + (' ' * spacing) + \
                                           "address-family " + get_name(vrf_neighbor_af.af_name.value)
                            spacing += 1
                            if vrf_neighbor_af.route_policy_in:
                                show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                               "route-policy " + vrf_neighbor_af.route_policy_in + \
                                               " in"
                            if vrf_neighbor_af.route_policy_out:
                                show_bgp_adj = show_bgp_adj + '\n' + (' ' * (spacing+1)) + \
                                               "route-policy " + vrf_neighbor_af.route_policy_out + \
                                               " out"
                            spacing -= 1
                            show_bgp_adj = show_bgp_adj + '\n' + \
                                           (' ' * spacing) + '!'
                        spacing -= 1
                        show_bgp_adj = show_bgp_adj + '\n' + \
                                       (' ' * spacing) + '!'
                    
                    spacing -= 1
                    show_bgp_adj = show_bgp_adj + '\n' + \
                                   (' ' * spacing) + '!'
                    spacing -= 1
                show_bgp_adj = show_bgp_adj + '\n' + \
                               (' ' * spacing) + '!'
    # return formatted string
    return(show_bgp_adj)


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

    bgp = xr_ipv4_bgp_cfg.Bgp()  # create object

    # read data from NETCONF device
    bgp = crud.read(provider, bgp)
    print(process_bgp(bgp))  # process object data

    provider.close()
    exit()
# End of script
