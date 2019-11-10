#!/usr/bin/env python2
#################################################################################
#
# Copyright (c) 2019 Zhaoqi Xiong
# All rights reserved.
#
#
# @NETFPGA_LICENSE_HEADER_START@
#
# Licensed to NetFPGA C.I.C. (NetFPGA) under one or more contributor
# license agreements.  See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.  NetFPGA licenses this
# file to you under the NetFPGA Hardware-Software License, Version 1.0 (the
# "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at:
#
#   http://www.netfpga-cic.org
#
# Unless required by applicable law or agreed to in writing, Work distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
# @NETFPGA_LICENSE_HEADER_END@
#
#################################################################################  

import argparse
import os
import sys
import grpc


# Import P4Runtime lib from parent utils dir
# Probably there's a better way of doing this.
sys.path.append(
                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '../../utils/'))
import p4runtime_lib.bmv2
from p4runtime_lib.switch import ShutdownAllSwitchConnections
import p4runtime_lib.helper




def get_actionpara(action):
    para = {}
    if action == 0:
        para = {}
    elif action == 2:
        para = {"dstAddr": "00:00:00:02:02:00", "port": 2}
    elif action == 3:
        para = {"dstAddr": "00:00:00:03:03:00", "port": 3}
    elif action == 4:
        para = {"dstAddr": "00:00:00:04:04:00", "port": 4}
    
    return para


def writeclass1x(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
                                                table_name="MyIngress.class1_exactx",
                                                match_fields={ "meta.distancex": a
                                                
                                                },
                                                action_name= "MyIngress.set_distancex",
                                                action_params= {"square": a_square,
                                               })
    switch.WriteTableEntry(table_entry)
    print("Installed action rule on %s" % switch.name)


def writeclass1y(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
                                                table_name="MyIngress.class1_exacty",
                                                match_fields={"meta.distancey": a
                                                
                                                },
                                                action_name="MyIngress.set_distancey",
                                                action_params={"square": a_square,}
                                                )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule on %s" % switch.name)


def writeclass2x(p4info_helper, switch,  a, a_square):
    table_entry = p4info_helper.buildTableEntry(
                                                table_name="MyIngress.class2_exactx",
                                                match_fields={"meta.distancex": a
                                                
                                                },
                                                action_name= "MyIngress.set_distancex",
                                                action_params = {"square": a_square,}
                                                )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule on %s" % switch.name)


def writeclass2y(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
                                                table_name="MyIngress.class2_exacty",
                                                match_fields={"meta.distancey": a
                                                
                                                },
                                                action_name="MyIngress.set_distancey",
                                                action_params = {"square": a_square,}
                                                )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule on %s" % switch.name)
                  


def writeaction(p4info_helper, switch,value,port):
    para = get_actionpara(port)
    table_entry = p4info_helper.buildTableEntry(
                                              table_name="MyIngress.ipv4_exact",
                                              match_fields={
                                              "meta.classification": value },
                                              action_name= "MyIngress.ipv4_forward",
                                              action_params = para
                                              )

    switch.WriteTableEntry(table_entry)
    print("Installed select rule on %s" % switch.name)
                  


                  
                  

def printGrpcError(e):
    print("gRPC Error:", e.details(), )
    status_code = e.code()
    print("(%s)" % status_code.name, )
    traceback = sys.exc_info()[2]
    print("[%s:%d]" % (traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))




def main(p4info_file_path, bmv2_file_path):
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)
                  
    try:
                  
        s1 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
                                                   name='s1',
                                                   address='127.0.0.1:50051',
                                                   device_id=0,
                                                   proto_dump_file='logs/s1-p4runtime-requests.txt')

        s1.MasterArbitrationUpdate()
                  
        s1.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                     bmv2_json_file_path=bmv2_file_path)
        print("Installed P4 Program using SetForwardingPipelineConfig on s1")

        a = [256,65535]
        for i in range(0,65535):
            writeclass1x(p4info_helper, s1, i, i**2)
            writeclass1y(p4info_helper, s1, i, i**2)
            writeclass2x(p4info_helper, s1, i, i**2)
            writeclass2y(p4info_helper, s1, i, i**2)
        # writeclass1x(p4info_helper,s1, a, 65535)
        # writeclass1y(p4info_helper,s1, a, 65535)
        # writeclass2x(p4info_helper,s1, a, 65535)
        # writeclass2y(p4info_helper,s1,a, 65535)
        # writeclass2y(p4info_helper,s1, a, 65535)
        writeaction(p4info_helper,s1,1,2)
        writeaction(p4info_helper,s1,2,3)
       #writedropaction(p4info_helper,s1,0)

                  
                  
    except KeyboardInterrupt:
        print("Shutting down.")

    except grpc.RpcError as e:
        printGrpcError(e)
                  
    ShutdownAllSwitchConnections()
                  
                  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/kmeans.p4info')

    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/kmeans.json')

    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print("\np4info file not found: %s\nHave you run 'make'?" % args.p4info)
        parser.exit(1)

    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print("\nBMv2 JSON file not found: %s\nHave you run 'make'?" % args.bmv2_json)
        parser.exit(1)

    main(args.p4info, args.bmv2_json)