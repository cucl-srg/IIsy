#!/usr/bin/env python3
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

import json
import re
import argparse

# Add argument
parser = argparse.ArgumentParser()
parser.add_argument('-i1', required=True, help='path to text tree')
parser.add_argument('-i2', required=True, help='path to text action')
parser.add_argument('-o', required=True, help='output path')
args = parser.parse_args()
inputfile = args.i1
actionfile = args.i2
outputfile = args.o

# read the action.text, find the actions for different classes.
def find_action(textfile):
    action =[]
    f = open(textfile)
    for line in f:
        n = re.findall(r"class", line)
        if n:
            fea = re.findall(r"\d",line)
            action.append(int(fea[1]))
    f.close()
    return action

# read the tree model, search the threshold value
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
    return proto,src,dst

# read the leaf node description and find the corresponding ranges
def find_classification(textfile,proto,src,dst):
    fea = []
    sign =[]
    num =[]
    f = open(textfile,'r')
    for line in f:
        n = re.findall(r"when", line)
        if n:
            fea.append(re.findall(r"(proto|src|dst)",line))
            sign.append(re.findall(r"(<=|>)",line))
            num.append(re.findall(r"\d+\.?\d*", line))
    f.close()


    protocol =[]
    srouce = []
    dstination =[]
    classfication =[]


    for i in range(len(fea)):
        feature1 = [i for i in range(len(proto) + 1)]
        feature2 = [i for i in range(len(src) + 1)]
        feature3 = [i for i in range(len(dst) + 1)]
        for j,feature in enumerate(fea[i]):
            if feature == 'proto':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = proto.index(thres)
                if sig == '<=':
                    while id < len(proto):
                        if id + 1 in feature1:
                            feature1.remove(id+1)
                        id = id+1
                else:
                    while id >= 0:
                        if id  in feature1:
                            feature1.remove(id)
                        id = id-1
            elif feature == 'src':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = src.index(thres)
                if sig == '<=':
                    while id < len(src):
                        if id+1 in feature2:
                            feature2.remove(id+1)
                        id = id+1
                else:
                    while id >= 0:
                        if id  in feature2:
                            feature2.remove(id)
                        id = id-1
            else:
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = dst.index(thres)
                if sig == '<=':
                    while id < len(dst):
                        if id + 1 in feature3:
                            feature3.remove(id+1)
                        id = id+1
                else:
                    while id >= 0:
                        if id  in feature3:
                            feature3.remove(id)
                        id = id-1
        protocol.append(feature1)
        srouce.append(feature2)
        dstination.append(feature3)
        a= len(num[i])
        classfication.append(num[i][a-1])
    return(protocol,srouce,dstination,classfication)

# write json file information 
def write_info(file):
    file.write("\"target\":\"bmv2\",\n")
    file.write("\"p4info\":\"build/example.p4info\",\n")
    file.write("\"bmv2_json\":\"build/example.json\",\n")
    file.write("\"table_entries\":[\n")

# get action parameters 
def get_actionpara(action):
    para = {}
    if action == 0 :
        para = {}
    elif action == 2:
        para = {'dstAddr': '00:00:00:02:02:00','port': 2}
    elif action == 3:
        para = {'dstAddr': '00:00:00:03:03:00','port': 3}
    elif action == 4:
        para = {'dstAddr': '00:00:00:04:04:00','port': 4}

    return para

# write default action
def write_ingress_default(file):
    file.write("{\n")
    file.write("    \"table\": \"MyIngress.ipv4_exact\",\n")
    file.write("    \"default\": true ,\n")
    file.write("    \"action_name\": \"MyIngress.drop\",\n")
    file.write("    \"action_params\": {}\n")
    file.write("}\n")


# write the entries for decision table
def write_ingress(file,a,b,c,action,port):

    para = get_actionpara(port)

    data = {'table': 'MyIngress.ipv4_exact',
            'match': {'meta.action_select1': a,
                      'meta.action_select2': b,
                      'meta.action_select3': c },
            'action_name': action,
            'action_params': para

            }

    jsondata =json.dumps(data,
                      indent=4,
                      separators=(', ', ': '), ensure_ascii=False)
    file.write(jsondata)
    file.write(",\n")

# write the entries for feature1 table
def write_feature1(file,a,ind):
    data = {'table':'MyIngress.feature1_exact',
            'match': { 'hdr.ipv4.protocol': a},
            'action_name':'MyIngress.set_actionselect1',
            'action_params':{'featurevalue1':ind}
            }

    jsondata =json.dumps(data,
                      indent=4, ensure_ascii=False)
    file.write(jsondata)
    file.write(",\n")

# write the entries for feature 2 table
def write_feature2(file,a,ind):
    data = {'table':'MyIngress.feature2_exact',
            'match': { 'hdr.tcp.srcPort': a},
            'action_name':'MyIngress.set_actionselect2',
            'action_params':{'featurevalue2':ind}
            }

    jsondata =json.dumps(data,
                      indent=4, ensure_ascii=False)
    file.write(jsondata)
    file.write(",\n")

# write the entries for feature 3 table
def write_feature3(file,a,ind):
    data = {'table':'MyIngress.feature3_exact',
            'match': { 'hdr.tcp.dstPort': a},
            'action_name':'MyIngress.set_actionselect3',
            'action_params':{'featurevalue3':ind}
            }

    jsondata =json.dumps(data,
                      indent=4, ensure_ascii=False)
    file.write(jsondata)
    file.write(",\n")


proto,src,dst = find_feature(inputfile)
protocol,srouce,dstination,classfication = find_classification(inputfile,proto,src,dst)
action = find_action(actionfile)


runtime = open(outputfile,"w+")
runtime.write("{ \n")
write_info(runtime)

# parameter for decision table
for i in range(len(classfication)):
    a = protocol[i]
    id = len(a) - 1
    del a[1:id]
    if(len(a) == 1):
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
    a = [i+1 for i in a]
    b = [i+1 for i in b]
    c = [i+1 for i in c]
    if ac == 0:
        write_ingress(runtime, a, b, c, 'MyIngress.drop', 0)
    else:
        print(a,b,c,ac)
        write_ingress(runtime, a, b, c,'MyIngress.ipv4_forward',ac)

#parameter in feature 1 table
if len(proto)!= 0:
    proto.append(0)
    proto.append(32)
    proto.sort()
    for i in range(len(proto)-1):
        write_feature1(runtime, proto[i:i + 2], i+1)
else:
    write_feature1(runtime,[0,32],1)
#parameter in feature 2 table
if len(src) != 0:
    src.append(0)
    src.append(65535)
    src.sort()
    for i in range(len(src)-1):
        write_feature2(runtime, src[i:i + 2], i+1)
#parameter in feature 3 table
if len(dst) != 0:
    dst.append(0)
    dst.append(65535)
    dst.sort()
    for i in range(len(dst)-1):
        write_feature3(runtime, dst[i:i + 2], i+1)



write_ingress_default(runtime)

runtime.write("] \n  }")
runtime.close()



