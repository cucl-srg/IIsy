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
import json
import re
import sys
from time import sleep
import grpc
import time

inputfile = './tree.txt'
actionfile = './action.txt'

# Import P4Runtime lib from parent utils dir
# Probably there's a better way of doing this.
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../utils/'))
import p4runtime_lib.bmv2
from p4runtime_lib.switch import ShutdownAllSwitchConnections
import p4runtime_lib.helper


def find_action(textfile):
    action = []
    f = open(textfile)
    for line in f:
        n = re.findall(r"class", line)
        if n:
            fea = re.findall(r"\d", line)
            action.append(int(fea[1]))
    f.close()
    return action


def find_feature(textfile):
    f = open(textfile)
    line = f.readline()
    proto = re.findall('\d+', line)
    line = f.readline()
    src = re.findall('\d+', line)
    line = f.readline()
    dst = re.findall('\d+', line)
    f.close
    proto = [int(i) for i in proto]
    src = [int(i) for i in src]
    dst = [int(i) for i in dst]
    return proto, src, dst

def find_classification(textfile, proto, src, dst):
    fea = []
    sign = []
    num = []
    f = open(textfile, 'r')
    for line in f:
        n = re.findall(r"when", line)
        if n:
            fea.append(re.findall(r"(proto|src|dst)", line))
            sign.append(re.findall(r"(<=|>)", line))
            num.append(re.findall(r"\d+\.?\d*", line))
    f.close()

    protocol = []
    srouce = []
    dstination = []
    classfication = []

    for i in range(len(fea)):
        feature1 = [k for k in range(len(proto) + 1)]
        feature2 = [k for k in range(len(src) + 1)]
        feature3 = [k for k in range(len(dst) + 1)]
        for j, feature in enumerate(fea[i]):
            if feature == 'proto':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = proto.index(thres)
                if sig == '<=':
                    while id < len(proto):
                        if id + 1 in feature1:
                            feature1.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature1:
                            feature1.remove(id)
                        id = id - 1
            elif feature == 'src':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = src.index(thres)
                if sig == '<=':
                    while id < len(src):
                        if id + 1 in feature2:
                            feature2.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature2:
                            feature2.remove(id)
                        id = id - 1
            else:
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = dst.index(thres)
                if sig == '<=':
                    while id < len(dst):
                        if id + 1 in feature3:
                            feature3.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature3:
                            feature3.remove(id)
                        id = id - 1
        protocol.append(feature1)
        srouce.append(feature2)
        dstination.append(feature3)
        a = len(num[i])
        classfication.append(num[i][a - 1])
    return (protocol, srouce, dstination, classfication)

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


def writeactionrule(p4info_helper, switch, a, b, c, action, port):
    para = get_actionpara(port)
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.ipv4_exact",
        match_fields={"meta.action_select1": a,
                      "meta.action_select2": b,
                      "meta.action_select3": c

                      },
        action_name=action,
        action_params=para
    )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule on %s" % switch.name)


def writefeature1rule(p4info_helper, switch, range, ind):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.feature1_exact",
        match_fields={
            "hdr.ipv4.protocol": range},
        action_name="MyIngress.set_actionselect1",
        action_params={
            "featurevalue1": ind,
        })
    switch.WriteTableEntry(table_entry)
    print("Installed feature1 rule on %s" % switch.name)


def writefeature2rule(p4info_helper, switch, range, ind):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.feature2_exact",
        match_fields={
            "hdr.tcp.srcPort": range},
        action_name="MyIngress.set_actionselect2",
        action_params={
            "featurevalue2": ind,
        })
    switch.WriteTableEntry(table_entry)
    print("Installed feature2 rule on %s" % switch.name)


def writefeature3rule(p4info_helper, switch, range, ind):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.feature3_exact",
        match_fields={
            "hdr.tcp.dstPort": range},
        action_name="MyIngress.set_actionselect3",
        action_params={
            "featurevalue3": ind,
        })
    switch.WriteTableEntry(table_entry)
    print("Installed feature3 rule on %s" % switch.name)


proto, src, dst = find_feature(inputfile)
protocol, srouce, dstination, classfication = find_classification(inputfile, proto, src, dst)
action = find_action(actionfile)


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

        for i in range(len(classfication)):
            a = protocol[i]
            id = len(a) - 1
            del a[1:id]
            if (len(a) == 1):
                a.append(a[0])
            b = srouce[i]
            id = len(b) - 1
            del b[1:id]
            if (len(b) == 1):
                b.append(b[0])
            c = dstination[i]
            id = len(c) - 1
            del c[1:id]
            if (len(c) == 1):
                c.append(c[0])

            ind = int(classfication[i])
            ac = action[ind]
            a = [i + 1 for i in a]
            b = [i + 1 for i in b]
            c = [i + 1 for i in c]

            if ac == 0:
                writeactionrule(p4info_helper, s1, a, b, c, "MyIngress.drop", 0)
            else:
                writeactionrule(p4info_helper, s1, a, b, c, "MyIngress.ipv4_forward", ac)
   

 
        if len(proto) != 0:
            proto.append(0)
            proto.append(32)
            proto.sort()
            for i in range(len(proto) - 1):
                writefeature1rule(p4info_helper, s1, proto[i:i + 2], i + 1)
        else:
            writefeature1rule(p4info_helper, s1, [0, 32], 1)

        if len(src) != 0:
            src.append(0)
            src.append(65535)
            src.sort()
            for i in range(len(src) - 1):
                writefeature2rule(p4info_helper, s1, src[i:i + 2], i + 1)
        if len(dst) != 0:
            dst.append(0)
            dst.append(65535)
            dst.sort()
            for i in range(len(dst) - 1):
                writefeature3rule(p4info_helper, s1, dst[i:i + 2], i + 1)

    except KeyboardInterrupt:
        print("Shutting down.")
    except grpc.RpcError as e:
        printGrpcError(e)

    ShutdownAllSwitchConnections()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/advanced.p4info')

    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/advanced.json')

    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print("\np4info file not found: %s\nHave you run 'make'?" % args.p4info)
        parser.exit(1)

    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print("\nBMv2 JSON file not found: %s\nHave you run 'make'?" % args.bmv2_json)
        parser.exit(1)
   
    start = time.time()
    main(args.p4info, args.bmv2_json)
    end = time.time()
    print("time to load the tables:", end-start)