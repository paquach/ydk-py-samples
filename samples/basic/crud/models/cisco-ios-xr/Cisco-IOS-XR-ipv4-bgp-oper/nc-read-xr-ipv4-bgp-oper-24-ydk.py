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
Read all data for model Cisco-IOS-XR-ipv4-bgp-oper.
Reads using a generic model and command line arguments.

usage: nc-read-xr-ipv4-bgp-oper-24-ydk.py [-h] [-v] device name

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)
  name           VRF name

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_oper \
    as xr_ipv4_bgp_oper
from datetime import timedelta
import logging

def get_rd(rd):
    rd = rd[-8:]
    rd = str(int(rd[:4], 16)) + ":" + \
         str(int(rd[-4:], 16))
    return rd
    
def get_status(path):
    status = str()
    if path.is_aggregation_suppressed:
        status += 's'
    if path.is_path_damped:
        status += 'd'
    if path.is_path_history_held:
        status += 'h'
    if path.is_path_valid:
        status += '*'
    if path.is_best_path:
        status += '>'
    if path.is_internal_path:
        status += 'i'
    if path.rib_failed:
        status += 'r'
    if path.is_path_stale:
        status += 'S'
    if path.is_path_nexthop_discarded:
        status += 'N'
    return status
    
def process_bgp(bgp, name):
    """Process data in bgp object."""
    # format string for bgp adjacency header
    bgp_table_header = ("\n   Network          Next Hop          Metric    LocPrf   "
                        "Weight  Path"
                        "\nRoute Distinguisher: {rd}")

    # format string for bgp adjacency row
    bgp_row = ("{status:<3}{network:<16} {nexthop:<20} {metric:>3} {locprf:>9} "
                "{weight:>8}  {path:<5}")
    
    bgp_header = ("BGP VRF {vrf_name}, state: {vrf_state}\n"
                  "BGP Route Distinguisher {rd}\n"
                  "VRF ID: {vrf_id}\n"
                  "BGP router identifier {routerid}, local AS number {local_as}\n"
                  "Non-stop routing is {nsr}\n"
                  "BGP table state: {tstate}\n"
                  "Table ID: {tid}    RD version: {rd_version}\n"
                  "BGP main routing table version {rt_version}\n"
                  "BGP NSR Initial initsync version {nsr_ver} ({nsr_conv})\n"
                  "BGP NSR/ISSU Sync-Group versions {sg_ver}\n"
                  "\n"
                  "Status codes: s suppressed, d damped, h history, * valid, > best\n"
                  "i - internal, r RIB-failure, S stale, N Nexthop-discard\n"
                  "Origin codes: i - IGP, e - EGP, ? - incomplete\n"
                  )
    
    if bgp.instances.instance:
        show_bgp_adj = str()
        show_bgp_table = str()
    else:
        show_bgp_adj = "No BGP instances found"
    count = 0
    
    # iterate over all instances
    for instance in bgp.instances.instance:
        # Show global configs
        # Check if vrf exists
        vrf = None
        for vrf_ in instance.instance_active.vrfs.vrf:
            if vrf_.vrf_name == name:
                vrf = vrf_
                break     
        if not vrf:
            return "VRF %s not found" % name
        
        
        vrf_name = vrf.global_process_info.vrf_name
        vrf_state = "Active" \
                    if vrf.global_process_info.vrf.vrf_is_active \
                    else "Inactive"
        rd = get_rd(vrf.information.route_distinguisher)
        vrf_id = hex(vrf.global_process_info.vrfid)
        global_process_info = vrf.global_process_info
        routerid = global_process_info.vrf.router_id
        local_as = global_process_info.global_.local_as
        gscan = global_process_info.global_.generic_scan_period
        nsr = "enabled" \
               if global_process_info.vrf.is_nsr \
               else "disabled"
        
        # Show AF information
        af = vrf.afs.af[0]
        vrf_af = af.global_af_process_info.vrf
        tstate = "Active" if vrf_af.table_is_active else "Inactive"
        tid = hex(vrf_af.table_id)
        rd_version = vrf_af.rd_version
        rt_version = vrf_af.table_version
        nsr_ver = vrf_af.nsr_conv_version
        nsr_conv = "Reached" \
                   if vrf_af.nsr_is_conv \
                   else "Not Reached"
        sg_ver = str(af.global_af_process_info.global_.syncgrp_version[0].entry) + \
                 '/' + str(af.global_af_process_info.global_.syncgrp_version[1].entry)
        
        # Show path information
        for path in af.path_table.path:
            path_information = path.path_information
            hop_ipv4_addr = path_information.next_hop.ipv4_address
            ip = path.network + '/' + str(path.prefix_length)
            metric = path_information.aigp_metric
            locprf = path.attributes_after_policy_in.common_attributes.local_preference
            weight = path_information.path_weight
            status = get_status(path_information)
            path_id = str(path.attributes_after_policy_in.common_attributes.neighbor_as)
            if path.attributes_after_policy_in.common_attributes.origin == 0:
                path_id += " i"
            elif path.attributes_after_policy_in.common_attributes.origin == 1:
                path_id += " e"
            elif path.attributes_after_policy_in.common_attributes.origin == 2:
                path_id += " ?"
            show_bgp_table += ('\n' + 
                               bgp_row.format(status = status,
                                              network=ip,
                                              nexthop=hop_ipv4_addr,
                                              metric=metric,
                                              locprf=locprf,
                                              weight=weight,
                                              path=path_id
                                              ))
        show_bgp_adj += ('\n' + 
                         bgp_header.format(vrf_name=vrf_name,
                                           vrf_state=vrf_state,
                                           rd=rd,
                                           vrf_id=vrf_id,
                                           routerid=routerid,
                                           local_as=local_as,
                                           gscan=gscan,
                                           nsr=nsr,
                                           tstate=tstate,
                                           tid=tid,
                                           rd_version=rd_version,
                                           rt_version=rt_version,
                                           nsr_ver=nsr_ver,
                                           nsr_conv=nsr_conv,
                                           sg_ver=sg_ver
                                           ))
            
    show_bgp_adj += bgp_table_header.format(rd=rd)
    show_bgp_adj += show_bgp_table
    show_bgp_adj += ("\n\n")
    return(show_bgp_adj)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    parser.add_argument("name",
                        help="VRF name")
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

    bgp = xr_ipv4_bgp_oper.Bgp()  # create object

    # read data from NETCONF device
    bgp = crud.read(provider, bgp)
    print(process_bgp(bgp, args.name))  # process object data

    provider.close()
    #print (time.time() - start)
    exit()
# End of script
