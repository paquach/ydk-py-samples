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
Create configuration for model Cisco-IOS-XR-ipv4-bgp-cfg.

usage: bgp-ipv4-cfg-CE1-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_datatypes \
    as xr_ipv4_bgp_datatypes
from ydk.types import Empty
import logging


def config_bgp(bgp):
    """Add config data to bgp object."""
    # global configuration
    instance = bgp.Instance()
    instance.instance_name = "default"
    instance_as = instance.InstanceAs()
    instance_as.as_ = 0
    four_byte_as = instance_as.FourByteAs()
    four_byte_as.as_ = 200
    four_byte_as.bgp_running = Empty()
    four_byte_as.default_vrf.global_.router_id = "10.1.1.2"                          
    # global address family
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast      
    connected_routes = global_af.ConnectedRoutes()                                  
    static_routes = global_af.StaticRoutes()                                         
    global_af.connected_routes = connected_routes
    global_af.static_routes = static_routes
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)
    # global address family for vpnv4
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.vp_nv4_unicast    
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)
	# global address family for ipv6
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv6_unicast      
    connected_routes = global_af.ConnectedRoutes()                                   
    static_routes = global_af.StaticRoutes()                                         
    global_af.connected_routes = connected_routes
    global_af.static_routes = static_routes
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)
    # global address family for vpnv6
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.vp_nv6_unicast    
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)
    # global address family for l2vpn
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.l2vpnevpn        
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)

    # configure neighbor 2001::6
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "2001::6"
    neighbor.remote_as.as_xx = 0
    neighbor.remote_as.as_yy = 100
    # address family ipv4
    neighbor_af = neighbor.neighbor_afs.NeighborAf()
    neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    neighbor_af.route_policy_in = "pass-all"
    neighbor_af.route_policy_out = "pass-all"
    neighbor_af.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af)
    # address family ipv6
    neighbor_af2 = neighbor.neighbor_afs.NeighborAf()
    neighbor_af2.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv6_unicast
    neighbor_af2.route_policy_in = "pass-all"
    neighbor_af2.route_policy_out = "pass-all"
    neighbor_af2.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af2)
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)
    
    # configure neighbor 10.1.1.1
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "10.1.1.1"
    neighbor.remote_as.as_xx = 0
    neighbor.remote_as.as_yy = 100
    # address family ipv4
    neighbor_af = neighbor.neighbor_afs.NeighborAf()
    neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    neighbor_af.route_policy_in = "pass-all"
    neighbor_af.route_policy_out = "pass-all"
    neighbor_af.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af)
    # address family vpnv4
    neighbor_af2 = neighbor.neighbor_afs.NeighborAf()
    neighbor_af2.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.vp_nv4_unicast
    neighbor_af2.route_policy_in = "pass-all"
    neighbor_af2.route_policy_out = "pass-all"
    neighbor_af2.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af2)
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)




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
    config_bgp(bgp)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, bgp)

    provider.close()
    exit()
# End of script
