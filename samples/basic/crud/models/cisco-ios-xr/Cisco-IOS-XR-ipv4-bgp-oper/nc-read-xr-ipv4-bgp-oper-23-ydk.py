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

usage: nc-read-xr-ipv4-bgp-oper-23-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_oper \
    as xr_ipv4_bgp_oper
import logging

def get_name(enum):
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

def int_to_time(time_int):
    return "%02d:%02d:%02d" % (time_int/60/60, (time_int/60)%60, time_int%60)
    
def get_status(next_hop_af):
    '''
        Use the binary representation of the status
        to find the actual status of device 
    '''
    status = str()
    binary = bin(next_hop_af.nexthop_gateway_info[0].nexthop_status)
    binary = '00' + binary[2:]
    stat_list = [binary[i:i+2] for i in range(0, len(binary), 2)]
    stat_list = list(reversed(stat_list))
    
    if stat_list[0] == '01':
        status += "[R]"
    elif stat_list[0] == '10':
        status += "[UR]"
    if stat_list[1] == '01':
        status += "[C]"
    elif stat_list[1] == '10':
        status += "[NC]"
    if stat_list[2] == '01':
        status += "[L]"
    elif stat_list[2] == '10':
        status += "[NL]"
    if stat_list[3][1] == '1':
        status += "[PR]"
    elif stat_list[3][0] == '1':
        status += "[I]" 
    return status
    
def get_rib_event(enum):
    return {
        0 : "(Cri)",
        1 : "(Non-Cri)",
        2 : "(Reg)"
    }.get(enum, "Error")
    
    
def process_bgp(bgp):
    """Process data in bgp object."""
    # format string for bgp adjacency header
    bgp_table_header = ("\nNext Hop         Status              Metric "
                   "Tbl-ID       Notf LastRIBEvent      RefCount")

    # format string for bgp adjacency row
    bgp_row = ("{next_hop:<16} {status:<19} {metric:<6} {tblid:<12} "
                "{notf:<4} {ribtime:<8}{ribevent:<9} {refcount:<8}")
    
    bgp_header = ("Total Nexthop Processing\n"
                  "  Time Spent: {tot_time} seconds\n"
                  "\n"
                  "Maximum Nexthop Processing\n"
                  "  Received: {rcvd_time} \n"
                  "  Bestpaths Deleted: {del_bp}\n"
                  "  Bestpaths Changed: {chg_bp}\n"
                  "  Time Spent: {bp_time} seconds\n"
                  "\n"
                  "Last Notification Processing\n"
                  "  Received: {rcvd_ln}\n"
                  "  Time Spent: {ln_time} seconds"
                  )
                  
    af_info = ("\n"
               "Gateway Address Family: {af}\n"
               "Table ID: {tid}\n"
               "Nexthop Count: {nh_count}\n"
               "Critical Trigger Delay: {ctd} ms\n"
               "Non-critical Trigger Delay: {nctd} ms\n"
               "\n"
               "Nexthop Version: {nh_ver}, RIB version: {rib_ver}\n"
               "EPE Table Version: {epet_ver}, EPE Label version: {epel_ver}\n"
               "EPE Downloaded Version: {eped_ver}, EPE Standby version: {epes_ver}\n"
               "\n"
               "Status Codes: R/UR Reachable/Unreachable\n"
               "              C/NC Connected/Not-connected\n"
               "              L/NL Local/Non-local\n"
               "              PR   Pending Registration\n"
               "              I    Invalid (Policy drop)\n"
               )
    
    if bgp.instances.instance:
        show_bgp_adj = str()
        show_row = str()
    else:
        show_bgp_adj = "No BGP instances found"
    count = 0
    
    # iterate over all instances
    # time is in ms
    for instance in bgp.instances.instance:
        default_vrf = instance.instance_active.default_vrf
        tot_time = default_vrf.next_hop_vrf.total_processing_time/1000.0
        rcvd_time = int_to_time(default_vrf.next_hop_vrf.max_proc_notification_time)
        del_bp = default_vrf.next_hop_vrf.max_notification_bestpath_deletes
        chg_bp = default_vrf.next_hop_vrf.max_notification_bestpath_changes
        bp_time = default_vrf.next_hop_vrf.maximum_processing_time/1000.0
        rcvd_ln = int_to_time(default_vrf.next_hop_vrf.last_notificationication_time)
        ln_time = default_vrf.next_hop_vrf.last_notification_processing_time/1000.0
        show_bgp_adj += ('\n' + 
                         bgp_header.format(tot_time=tot_time,
                                           rcvd_time=rcvd_time,
                                           del_bp=del_bp,
                                           chg_bp=chg_bp,
                                           bp_time=bp_time,
                                           rcvd_ln=rcvd_ln,
                                           ln_time=ln_time
                                           ))
        
        # Show af information
        for af in default_vrf.afs.af:
            for next_hop_address_family in af.next_hop_address_families.next_hop_address_family:
                af = get_name(next_hop_address_family.next_hop_af_name.value)
                tid = hex(next_hop_address_family.next_hop_af_vrf_af.nh_table_id)
                nh_count = next_hop_address_family.next_hop_af_vrf_af.total_nexthops
                ctd = next_hop_address_family.next_hop_af_vrf_af.critical_trigger_delay
                nctd = next_hop_address_family.next_hop_af_vrf_af.non_critical_trigger_delay
                nh_ver = next_hop_address_family.next_hop_af_vrf_af.nh_nexthop_version
                rib_ver = next_hop_address_family.next_hop_af_vrf_af.nh_rib_version
                epet_ver = next_hop_address_family.next_hop_af_vrf_af.epe_table_version
                epel_ver = next_hop_address_family.next_hop_af_vrf_af.epe_label_version
                eped_ver = next_hop_address_family.next_hop_af_vrf_af.epe_downloaded_version
                epes_ver = next_hop_address_family.next_hop_af_vrf_af.epe_standby_version
                
                show_bgp_adj += ('\n' + 
                                 af_info.format(af=af,
                                                tid=tid,
                                                nh_count=nh_count,
                                                ctd=ctd,
                                                nctd=nctd,
                                                nh_ver=nh_ver,
                                                rib_ver=rib_ver,
                                                epet_ver=epet_ver,
                                                epel_ver=epel_ver,
                                                eped_ver=eped_ver,
                                                epes_ver=epes_ver
                                                ))
                  
                # Show next hop information
                for next_hop_af in next_hop_address_family.next_hop_afs.next_hop_af:
                    next_hop = next_hop_af.next_hop_address
                    status = get_status(next_hop_af)
                    metric = next_hop_af.nexthop_gateway_info[0].nexthop_metric
                    tblid = hex(next_hop_af.nexthop_gateway_info[0].nexthop_tableid)
                    notf = str(next_hop_af.nexthop_gateway_info[0].critical_events) + \
                           '/' + str(next_hop_af.nexthop_gateway_info[0].non_critical_events)
                    ribtime = int_to_time(next_hop_af.nexthop_gateway_info[0].last_event_since)
                    ribevent = get_rib_event(next_hop_af.nexthop_gateway_info[0].last_event_type.value)
                    refcount = str(next_hop_af.nexthop_reference_count) + \
                               "/" + str(next_hop_af.nh_reference_count_total)  
                    
                    show_row += ('\n' + 
                                 bgp_row.format(next_hop=next_hop,
                                                status=status,
                                                metric=metric,
                                                tblid=tblid,
                                                notf=notf,
                                                ribtime=ribtime,
                                                ribevent=ribevent,
                                                refcount=refcount
                                                ))
                show_bgp_adj += bgp_table_header
                show_bgp_adj += show_row
            break
                
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

    bgp = xr_ipv4_bgp_oper.Bgp()  # create object

    # read data from NETCONF device
    bgp = crud.read(provider, bgp)
    print(process_bgp(bgp))  # process object data

    provider.close()
  #  print (time.time() - start)
    exit()
# End of script
