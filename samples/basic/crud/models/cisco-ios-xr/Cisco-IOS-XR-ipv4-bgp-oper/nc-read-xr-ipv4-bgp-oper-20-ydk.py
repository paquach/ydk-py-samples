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

usage: nc-read-xr-ipv4-bgp-oper-20-ydk.py [-h] [-v] device

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
from datetime import timedelta
import logging
import time
start_time = time.time()
def get_nbr_state(enum):
    #interpret enum
    return {
        0 : "DontCare",
        1 : "Idle",
        2 : "Connect",
        3 : "Active",
        4 : "OpenSent",
        5 : "OpenConfirm",
        6 : "Established",
        7 : "Closing",
        8 : "ClosingSync"
    }.get(enum, "Error")
    
def get_nsr_state(enum):
    return {
        0 : "None",
        1 : "OPER_DOWN",
        2 : "TCP Sync in progress",
        3 : "TCP Sync Phase 2",
        4 : "BGP Sync in progress",
        5 : "Neighbor Ready"
    }.get(enum, "Error")


def process_bgp(bgp):
    """Process data in bgp object."""
    # format string for bgp adjacency header
    bgp_header = ("BGP Sessions:\n"
                   "Neighbor         Vrf                  Spk    AS   "
                   "InQ  OutQ  NBRState     NSRState")

    # format string for bgp adjacency row
    bgp_row = ("{neighbor:<16} {vrf:<20} {spk:>3} {bgp_as:>5} "
                "{inq:>5} {outq:>5}  {nbr_state:<12} {nsr_state:<8}")
    # format string for bgp adjacency trailer
    bgp_trailer = "Total Neighbor count: {count}"
    
    if bgp.instances.instance:
        show_bgp_adj = str()
    else:
        show_bgp_adj = "No BGP instances found"
    count = 0
    
    # iterate over all instances
    for instance in bgp.instances.instance:
        show_bgp_adj += bgp_header
        # iterate over all neighbors
        for neighbor in instance.instance_active.default_vrf.neighbors.neighbor:
            count += 1
            # iterate over all adjacencies
            vrf = neighbor.vrf_name
            spk = neighbor.speaker_id
            bgp_as = neighbor.remote_as
            inq = neighbor.messages_queued_in
            outq = neighbor.messages_queued_out
            nbr_state = get_nbr_state(neighbor.connection_state.value)
            nsr_state = get_nsr_state(neighbor.nsr_state.value)
            
            show_bgp_adj += ("\n" +
                              bgp_row.format(neighbor=neighbor.neighbor_address,
                                              vrf=vrf,
                                              spk=spk,
                                              bgp_as=bgp_as,
                                              inq=inq,
                                              outq=outq,
                                              nbr_state=nbr_state,
                                              nsr_state=nsr_state))
                                              
        for vrf in instance.instance_active.vrfs.vrf:
            for neighbor in vrf.neighbors.neighbor:
                count += 1
                # iterate over all adjacencies
                vrf = neighbor.vrf_name
                spk = neighbor.speaker_id
                bgp_as = neighbor.remote_as
                inq = neighbor.messages_queued_in
                outq = neighbor.messages_queued_out
                nbr_state = get_nbr_state(neighbor.connection_state.value)
                nsr_state = get_nsr_state(neighbor.nsr_state.value)

                show_bgp_adj += ("\n" +
                                  bgp_row.format(neighbor=neighbor.neighbor_address,
                                                  vrf=vrf,
                                                  spk=spk,
                                                  bgp_as=bgp_as,
                                                  inq=inq,
                                                  outq=outq,
                                                  nbr_state=nbr_state,
                                                  nsr_state=nsr_state))
                                                  
    show_bgp_adj += ("\n\n" + 
                     bgp_trailer.format(count=count))
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
    exit()
# End of script
