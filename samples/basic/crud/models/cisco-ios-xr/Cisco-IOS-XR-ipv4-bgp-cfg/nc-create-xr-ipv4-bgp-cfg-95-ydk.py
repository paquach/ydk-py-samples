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

usage: bgp-ipv4-cfg-RR-ydk [-h] [-v] device

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
    four_byte_as.as_ = 100
    four_byte_as.bgp_running = Empty()
    four_byte_as.default_vrf.global_.router_id = "200.1.1.2"
    # global address family
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)
	# global address family for vpnv4
    global_af2 = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af2.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.vp_nv4_unicast
    global_af2.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af2)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)

    # configure rr-client neighbor group
    neighbor_groups = four_byte_as.default_vrf.bgp_entity.neighbor_groups
    neighbor_group = neighbor_groups.NeighborGroup()
    neighbor_group.neighbor_group_name = "rr-client"
    neighbor_group.create = Empty()
    # remote AS
    neighbor_group.remote_as.as_xx = 0
    neighbor_group.remote_as.as_yy = 100
    neighbor_groups.neighbor_group.append(neighbor_group)
    # ipv4 unicast
    neighbor_group_af = neighbor_group.neighbor_group_afs.NeighborGroupAf()
    neighbor_group_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
    neighbor_group_af.route_reflector_client = True
    neighbor_group_af.activate = Empty()
    neighbor_group_afs = neighbor_group.neighbor_group_afs
    neighbor_group_afs.neighbor_group_af.append(neighbor_group_af)
	# vpnv4 unicast
    neighbor_group_af2 = neighbor_group.neighbor_group_afs.NeighborGroupAf()
    neighbor_group_af2.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.vp_nv4_unicast
    neighbor_group_af2.route_reflector_client = True
    neighbor_group_af2.activate = Empty()
    neighbor_group_afs2 = neighbor_group.neighbor_group_afs
    neighbor_group_afs2.neighbor_group_af.append(neighbor_group_af2)

    # configure neighbor 80.1.1.1
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "80.1.1.1"
    neighbor.neighbor_group_add_member = "rr-client"
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)

	# configure neighbor 200.1.1.1
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "200.1.1.1"
    neighbor.neighbor_group_add_member = "rr-client"
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
