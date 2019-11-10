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
import numpy as np

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
        table_name="MyIngress.class1_p1",
        match_fields={"hdr.tcp.srcPort": a

                      },
        action_name="MyIngress.set_p1",
        action_params={"square": a_square,
                       })
    switch.WriteTableEntry(table_entry)
    print("Installed action rule about class1 p1")


def writeclass1y(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.class1_p2",
        match_fields={"hdr.tcp.dstPort": a

                      },
        action_name="MyIngress.set_p2",
        action_params={"square": a_square, }
    )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule about class1 p2")


def writeclass2x(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.class2_p1",
        match_fields={"hdr.tcp.srcPort": a

                      },
        action_name="MyIngress.set_p1",
        action_params={"square": a_square, }
    )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule about class2 p1")


def writeclass2y(p4info_helper, switch, a, a_square):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.class2_p2",
        match_fields={"hdr.tcp.dstPort": a

                      },
        action_name="MyIngress.set_p2",
        action_params={"square": a_square, }
    )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule about class2 p2")


def writepro1(p4info_helper, switch, a, b, probility):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.class1_pro",
        match_fields={"meta.x": a,
                      "meta.y": b

                      },
        action_name="MyIngress.set_select1",
        action_params={"probility": probility, }
    )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule about class1 pro")


def writepro2(p4info_helper, switch, a, b, probility):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.class2_pro",
        match_fields={"meta.x": a,
                      "meta.y": b

                      },
        action_name="MyIngress.set_select2",
        action_params={"probility": probility, }
    )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule about class2 pro")


def writeaction(p4info_helper, switch, value, port):
    para = get_actionpara(port)
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.ipv4_exact",
        match_fields={
            "meta.classification": value},
        action_name="MyIngress.ipv4_forward",
        action_params=para
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

        for i in range(5000,39000):
            p11 = int(1 / np.sqrt(2 * np.pi * 0.001 ** 2) * np.exp(-((i - 5001) ** 2) / (2 * 0.001 ** 2)) * 10 ** 5)
            p12 = int(1 / np.sqrt(2 * np.pi * 0.001 ** 2) * np.exp(-((i - 5001) ** 2) / (2 * 0.001 ** 2)) * 10 ** 5)
            p21 = int(
                1 / np.sqrt(2 * np.pi * 0.001 ** 2) * np.exp(-((i - 11211) ** 2) / (2 * 0.001 ** 2)) * 10 ** 5)
            p22 = int(
                1 / np.sqrt(2 * np.pi * 0.001 ** 2) * np.exp(-((i - 38094) ** 2) / (2 * 0.001 ** 2)) * 10 ** 5)
            if (p11 > 65535):
                p11 = 65535
            if (p12 > 65535):
                p12 = 65535
            if (p21 > 65535):
                p21 = 65535
            if (p22 > 65535):
                p22 = 65535
            writeclass1x(p4info_helper, s1, i, p11)
            writeclass1y(p4info_helper, s1, i, p12)
            writeclass2x(p4info_helper, s1, i, p21)
            writeclass2y(p4info_helper, s1, i, p22)

        writeaction(p4info_helper, s1, 1, 2)
        writeaction(p4info_helper, s1, 2, 3)

        for i in range(0, 65530, 255):
            for j in range(0, 65530, 255):
                a = [i, i + 255]
                b = [j, j + 255]
                probility = i * j
                writepro1(p4info_helper, s1, a, b, probility)
                writepro2(p4info_helper, s1, a, b, probility)

        # writepro1(p4info_helper, s1, [0, 0],[0,0], 0)
        # writepro1(p4info_helper, s1, [65535,65535], [65535,65535], 1)
        # writepro2(p4info_helper, s1, [0, 0],[0,0], 0)
        # writepro2(p4info_helper, s1, [65535,65535], [65535,65535], 1)

    except KeyboardInterrupt:
        print("Shutting down.")

    except grpc.RpcError as e:
        printGrpcError(e)

    ShutdownAllSwitchConnections()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/bayes.p4info')

    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/bayes.json')

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
