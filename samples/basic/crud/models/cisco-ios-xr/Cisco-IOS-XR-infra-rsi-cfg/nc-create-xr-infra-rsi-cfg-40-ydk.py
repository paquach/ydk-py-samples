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
Create configuration for model Cisco-IOS-XR-infra-rsi-cfg.
Creates using a generic model and command line arguments.

usage: nc-create-xr-infra-rsi-cfg-40-ydk.py [-h] [-v] device name af saf direction as

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)
  name           VRF name
  af             Address Family Name (ipv4/ipv6)
  saf            sub address family (unicast/multicast)
  direction      route (import/export)
  as             AS Number (as_:as_index)
  

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_cfg \
    as xr_ipv4_bgp_cfg
from ydk.types import Empty
import logging


def af_enum(af):
    af = af.lower()
    if af == "ipv4":
        return xr_infra_rsi_cfg.VrfAddressFamilyEnum.ipv4
    elif af == "ipv6":
        return xr_infra_rsi_cfg.VrfAddressFamilyEnum.ipv6
    else:
        print "Invalid AF name"
        exit(1)
    
def saf_enum(saf):
    saf = saf.lower()
    if saf == "unicast":
        return xr_infra_rsi_cfg.VrfSubAddressFamilyEnum.unicast
    elif saf == "multicast":
        return xr_infra_rsi_cfg.VrfSubAddressFamilyEnum.multicast
    else: 
        print "Invalid SAF"
        exit(1)
       

def config_vrfs(vrfs, name, af, saf, direction, as_):
    """Add config data to vrfs object."""
    vrf = vrfs.Vrf()
    vrf.vrf_name = name
    vrf.create = Empty()

    # Get af information
    af_name_enum = af_enum(af)
    saf_name_enum = saf_enum(saf)
    as_list = as_.split(':')
    if len(as_list) < 2:
        print "Incorrect AS format"
        exit(1)
    
    # address family
    af = vrf.afs.Af()
    af.af_name = af_name_enum
    af.saf_name = saf_name_enum
    af.topology_name = "default"
    af.create = Empty()

    # import route targets    
    if direction.lower() == "import":
        route_target = af.bgp.import_route_targets.route_targets.RouteTarget()
        route_target.type = xr_ipv4_bgp_cfg.BgpVrfRouteTargetEnum.as_
        as_or_four_byte_as = route_target.AsOrFourByteAs()
        as_or_four_byte_as.as_xx = 0
        as_or_four_byte_as.as_ = int(as_list[0])
        as_or_four_byte_as.as_index = int(as_list[1])
        as_or_four_byte_as.stitching_rt = 0
        route_target.as_or_four_byte_as.append(as_or_four_byte_as)
        af.bgp.import_route_targets.route_targets.route_target.append(route_target)
    
    # export route targets
    elif direction.lower() == "export":
        route_target = af.bgp.export_route_targets.route_targets.RouteTarget()
        route_target.type = xr_ipv4_bgp_cfg.BgpVrfRouteTargetEnum.as_
        as_or_four_byte_as = route_target.AsOrFourByteAs()
        as_or_four_byte_as.as_xx = 0
        as_or_four_byte_as.as_ = int(as_list[0])
        as_or_four_byte_as.as_index = int(as_list[1])
        as_or_four_byte_as.stitching_rt = 0
        route_target.as_or_four_byte_as.append(as_or_four_byte_as)
        af.bgp.export_route_targets.route_targets.route_target.append(route_target)
     
    else:
        print "invalid direction"
        exit(1)

    # append address family and vrf
    vrf.afs.af.append(af)
    vrfs.vrf.append(vrf)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    parser.add_argument("name",
                        help="VRF name")
    parser.add_argument("af",
                        help="AF name (ipv4/ipv6)")  
    parser.add_argument("saf",
                        help="sub AF name (unicast/multicast)")
    parser.add_argument("direction",
                        help="route (import/export)")   
    parser.add_argument("as_",
                        help="AS (as_:as_index)")                        
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
    config_vrfs(vrfs, args.name, args.af, args.saf, args.direction, args.as_)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, vrfs)

    provider.close()
    exit()
# End of script
