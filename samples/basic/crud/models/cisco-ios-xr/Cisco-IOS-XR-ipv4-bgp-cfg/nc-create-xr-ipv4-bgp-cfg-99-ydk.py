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

usage: bgp-ipv4-cfg-PE1-ydk.py [-h] [-v] device

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
import sys
#sys.path[1:1] = ['/nobackup/paquach/moonshine-dev/xrut/modules']

#import xrut
#routers = xrut.routers

#print routers

def config_bgp(bgp):
    """Add config data to bgp object."""
    # global configuration
    instance = bgp.Instance()
    instance.instance_name = "default"
    instance_as = instance.InstanceAs()
    instance_as.as_ = 0
    four_byte_as = instance_as.FourByteAs()
    four_byte_as.as_ = 100
    four_byte_as.bgp_running = Empty()
    four_byte_as.default_vrf.global_.router_id = "10.1.1.1"                         
    # global address family
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast    
    connected_routes = global_af.ConnectedRoutes()
    connected_routes.route_policy_name = "passall"                        
    global_af.connected_routes = connected_routes
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)
	# global address family for vpnv4
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.vp_nv4_unicast 
    global_af.vrf_all.label_mode.label_allocation_mode = "per-ce"
    global_af.vrf_all.enable = Empty()
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)
    # global address family for ipv6
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv6_unicast   
    connected_routes = global_af.ConnectedRoutes()
    connected_routes.route_policy_name = "passall"                               
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
    global_af.vrf_all.label_mode.label_allocation_mode = "per-ce"
    global_af.vrf_all.enable = Empty()
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
    # global address family for link state link state
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.lsls         
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)
    
     # configure neighbor group ce
    neighbor_groups = four_byte_as.default_vrf.bgp_entity.neighbor_groups
    neighbor_group = neighbor_groups.NeighborGroup()
    neighbor_group.neighbor_group_name = "ce"
    neighbor_group.create = Empty()
    # remote AS
    neighbor_group.remote_as.as_xx = 0
    neighbor_group.remote_as.as_yy = 200
    neighbor_groups.neighbor_group.append(neighbor_group)
    # ipv4 unicast
    neighbor_group_af = neighbor_group.neighbor_group_afs.NeighborGroupAf()
    neighbor_group_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    neighbor_group_af.route_policy_in = "passall"
    neighbor_group_af.route_policy_out = "passall"
    neighbor_group_af.activate = Empty()
    neighbor_group_afs = neighbor_group.neighbor_group_afs
    neighbor_group_afs.neighbor_group_af.append(neighbor_group_af)
        
    # configure neighbor 3001::5
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "3001::5"
    neighbor.remote_as.as_xx = 0
    neighbor.remote_as.as_yy = 100
    # address family ipv4
    neighbor_af = neighbor.neighbor_afs.NeighborAf()
    neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    neighbor_af.route_policy_in = "passall"
    neighbor_af.route_policy_out = "passall"
    neighbor_af.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af)
    # address family ipv6 
    neighbor_af2 = neighbor.neighbor_afs.NeighborAf()
    neighbor_af2.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv6_unicast
    neighbor_af2.route_policy_in = "passall"
    neighbor_af2.route_policy_out = "passall"
    neighbor_af2.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af2)
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)

    # configure neighbor 200.1.1.2
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "200.1.1.2"
    neighbor.remote_as.as_xx = 0
    neighbor.remote_as.as_yy = 100
    # address family ipv4
    neighbor_af = neighbor.neighbor_afs.NeighborAf()
    neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    neighbor_af.route_policy_in = "passall"
    neighbor_af.route_policy_out = "passall"
    neighbor_af.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af)
    # address family vpnv4
    neighbor_af2 = neighbor.neighbor_afs.NeighborAf()
    neighbor_af2.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.vp_nv4_unicast
    neighbor_af2.route_policy_in = "passall"
    neighbor_af2.route_policy_out = "passall"
    neighbor_af2.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af2)
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)
    # address family link-state
    neighbor_af = neighbor.neighbor_afs.NeighborAf()
    neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.lsls
    neighbor_af.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af)
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)

    # configure neighbor 2001::208:28:2:1
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "2001::208:28:2:1"
    neighbor.remote_as.as_xx = 0
    neighbor.remote_as.as_yy = 1
    neighbor.update_source_interface = "Loopback0"
    # address family ipv4
    neighbor_af = neighbor.neighbor_afs.NeighborAf()
    neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv6_unicast
    neighbor_af.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af)
    # address family link-state
    neighbor_af = neighbor.neighbor_afs.NeighborAf()
    neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.lsls
    neighbor_af.activate = Empty()
    neighbor.neighbor_afs.neighbor_af.append(neighbor_af)
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)
    
    # VRF 1 
    vrf = four_byte_as.vrfs.Vrf()
    vrf.vrf_name = "1"
    # vrf global
    vrf.vrf_global.route_distinguisher.type = xr_ipv4_bgp_cfg.BgpRouteDistinguisherEnum.four_byte_as
    vrf.vrf_global.route_distinguisher.as_xx = 0
    vrf.vrf_global.route_distinguisher.as_ = 1
    vrf.vrf_global.route_distinguisher.as_index = 1
    vrf.vrf_global.exists = Empty()
    # vrf global af
    vrf_global_af = vrf.vrf_global.vrf_global_afs.VrfGlobalAf()
    vrf_global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    static_routes = vrf_global_af.StaticRoutes()
    vrf_global_af.static_routes = static_routes
    vrf_global_af.enable = Empty()
    vrf.vrf_global.vrf_global_afs.vrf_global_af.append(vrf_global_af)
    # vrf neighbor
    vrf_neighbor = vrf.vrf_neighbors.VrfNeighbor()
    vrf_neighbor.neighbor_address = "10.1.1.2"
    vrf_neighbor.neighbor_group_add_member = "ce"
    # vrf neighbor af
    vrf_neighbor_af = vrf_neighbor.vrf_neighbor_afs.VrfNeighborAf()
    vrf_neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    vrf_neighbor_af.activate = Empty()
    vrf_neighbor.vrf_neighbor_afs.vrf_neighbor_af.append(vrf_neighbor_af)
    vrf.vrf_neighbors.vrf_neighbor.append(vrf_neighbor)
    four_byte_as.vrfs.vrf.append(vrf)

    # VRF 2 
    vrf = four_byte_as.vrfs.Vrf()
    vrf.vrf_name = "2"
    # vrf global
    vrf.vrf_global.route_distinguisher.type = xr_ipv4_bgp_cfg.BgpRouteDistinguisherEnum.four_byte_as
    vrf.vrf_global.route_distinguisher.as_xx = 0
    vrf.vrf_global.route_distinguisher.as_ = 2
    vrf.vrf_global.route_distinguisher.as_index = 2
    vrf.vrf_global.exists = Empty()
    # vrf global af
    vrf_global_af = vrf.vrf_global.vrf_global_afs.VrfGlobalAf()
    vrf_global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    static_routes = vrf_global_af.StaticRoutes()
    vrf_global_af.static_routes = static_routes
    vrf_global_af.enable = Empty()
    vrf.vrf_global.vrf_global_afs.vrf_global_af.append(vrf_global_af)
    # vrf global af ipv6
    vrf_global_af = vrf.vrf_global.vrf_global_afs.VrfGlobalAf()
    vrf_global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv6_unicast
    static_routes = vrf_global_af.StaticRoutes()
    vrf_global_af.static_routes = static_routes
    vrf_global_af.enable = Empty()
    vrf.vrf_global.vrf_global_afs.vrf_global_af.append(vrf_global_af)
    # vrf neighbor
    vrf_neighbor = vrf.vrf_neighbors.VrfNeighbor()
    vrf_neighbor.neighbor_address = "2001::5"
    vrf_neighbor.remote_as.as_xx = 0
    vrf_neighbor.remote_as.as_yy = 200
    # vrf neighbor af
    vrf_neighbor_af = vrf_neighbor.vrf_neighbor_afs.VrfNeighborAf()
    vrf_neighbor_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv6_unicast
    vrf_neighbor_af.route_policy_in = "passall"
    vrf_neighbor_af.route_policy_out = "passall"
    vrf_neighbor_af.activate = Empty()
    vrf_neighbor.vrf_neighbor_afs.vrf_neighbor_af.append(vrf_neighbor_af)
    vrf.vrf_neighbors.vrf_neighbor.append(vrf_neighbor)
    four_byte_as.vrfs.vrf.append(vrf)
    
    # VRF 3   
    vrf = four_byte_as.vrfs.Vrf()
    vrf.vrf_name = "3"
    # vrf global
    vrf.vrf_global.route_distinguisher.type = xr_ipv4_bgp_cfg.BgpRouteDistinguisherEnum.four_byte_as
    vrf.vrf_global.route_distinguisher.as_xx = 0
    vrf.vrf_global.route_distinguisher.as_ = 3
    vrf.vrf_global.route_distinguisher.as_index = 3
    vrf.vrf_global.exists = Empty()
    # vrf global af
    vrf_global_af = vrf.vrf_global.vrf_global_afs.VrfGlobalAf()
    vrf_global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    vrf_global_af.table_policy = "allow-only-pfxlen-32"
    vrf_global_af.enable = Empty()
    vrf.vrf_global.vrf_global_afs.vrf_global_af.append(vrf_global_af)
    # vrf neighbor
    vrf_neighbor = vrf.vrf_neighbors.VrfNeighbor()
    vrf_neighbor.neighbor_address = "30.1.1.2"
    vrf_neighbor.neighbor_group_add_member = "ce"
    # vrf neighbor af
    vrf.vrf_neighbors.vrf_neighbor.append(vrf_neighbor)
    four_byte_as.vrfs.vrf.append(vrf)
    
    # VRF 4  
    vrf = four_byte_as.vrfs.Vrf()
    vrf.vrf_name = "4"
    # vrf global
    vrf.vrf_global.route_distinguisher.type = xr_ipv4_bgp_cfg.BgpRouteDistinguisherEnum.four_byte_as
    vrf.vrf_global.route_distinguisher.as_xx = 0
    vrf.vrf_global.route_distinguisher.as_ = 4
    vrf.vrf_global.route_distinguisher.as_index = 4
    vrf.vrf_global.exists = Empty()
    # vrf global af
    vrf_global_af = vrf.vrf_global.vrf_global_afs.VrfGlobalAf()
    vrf_global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    vrf_global_af.table_policy = "allow-only-pfxlen-32"
    vrf_global_af.enable = Empty()
    vrf.vrf_global.vrf_global_afs.vrf_global_af.append(vrf_global_af)
    # vrf neighbor
    vrf_neighbor = vrf.vrf_neighbors.VrfNeighbor()
    vrf_neighbor.neighbor_address = "40.1.1.2"
    vrf_neighbor.neighbor_group_add_member = "ce"
    # vrf neighbor af
    vrf.vrf_neighbors.vrf_neighbor.append(vrf_neighbor)
    four_byte_as.vrfs.vrf.append(vrf)
    
    
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
