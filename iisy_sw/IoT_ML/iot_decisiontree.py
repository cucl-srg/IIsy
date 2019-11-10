#!/usr/bin/env python
#################################################################################
#
# Copyright (c) 2019 Zhaoqi Xiong, Noa Zilberman
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

import numpy as np
import pandas as pd
import argparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import *
from sklearn.tree import export_graphviz
import pydotplus



parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i', required=True, help='path to training dataset')
parser.add_argument('-o', required=True, help='path to outputfile')
parser.add_argument('-t', required=True, help='path to test dataset')
args = parser.parse_args()

input = args.i
test = args.t
outputfile = args.o


def get_lineage(tree, feature_names, file):

    frame_len=[]  
    eth_type=[]
    ip_proto=[]
    ip_flags=[]
    ipv6_nxt=[]
    ipv6_opt=[]
    tcp_srcport=[]
    tcp_dstport=[]
    tcp_flags=[]
    udp_srcport=[]
    udp_dstport=[]
    left = tree.tree_.children_left
    right = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value
    le = '<='
    g = '>'
    # get ids of child nodes
    idx = np.argwhere(left == -1)[:, 0]
    
    def recurse(left, right, child, lineage=None):
        if lineage is None:
            lineage = [child]
        if child in left:
            parent = np.where(left == child)[0].item()
            split = 'l'
        else:
            parent = np.where(right == child)[0].item()
            split = 'r'
        
        lineage.append((parent, split, threshold[parent], features[parent]))
        if parent == 0:
            lineage.reverse()
            return lineage
        else:
            return recurse(left, right, parent, lineage)

    for j, child in enumerate(idx):
        clause = ' when '
        for node in recurse(left, right, child):
                if len(str(node)) < 3:
                    continue
                i = node
                
                if i[1] == 'l':
                    sign = le
                else:
                    sign = g
                clause = clause + i[3] + sign + str(i[2]) + ' and '

        a = list(value[node][0])
        ind = a.index(max(a))
        clause = clause[:-4] + ' then ' + str(ind)
        file.write(clause)
        file.write(";\n")


Set1 = pd.read_csv(input)
Set = Set1.values.tolist()
X = [i[0:10] for i in Set]
Y = [i[11] for i in Set]
class_names=['smart-static','sensor','audio','video','else']
feature_names=['frame_len','eth_type','ip_proto','ip_flags','ipv6_nxt','ipv6_opt','tcp_srcport','tcp_dstport','tcp_flags','udp_srcport','udp_dstport']



#debug = open("debug.txt","w+")
#debug.write("Y = ")
#debug.write(str(Y))
#debug.write(";\n")
#debug.close()


#prepare training and testing set
X = np.array(X)
Y = np.array(Y)

# decision tree fit

dt = DecisionTreeClassifier(max_depth = 5)
dt.fit(X, Y)
Predict_Y = dt.predict(X)
print(accuracy_score(Y, Predict_Y))
#print("\tBrier: %1.3f" % (clf_score))
print("\tPrecision: %1.3f" % precision_score(Y, Predict_Y,average='weighted'))
print("\tRecall: %1.3f" % recall_score(Y, Predict_Y,average='weighted'))
print("\tF1: %1.3f\n" % f1_score(Y, Predict_Y,average='weighted'))

#Test set 
Set2 = pd.read_csv(test)
Set_t = Set2.values.tolist()
Xt = [i[0:10] for i in Set_t]
Yt = [i[11] for i in Set_t]

Predict_Yt = dt.predict(Xt)
print(accuracy_score(Yt, Predict_Yt))
#print("\tBrier: %1.3f" % (clf_score))
print("\tPrecision: %1.3f" % precision_score(Yt, Predict_Yt,average='weighted'))
print("\tRecall: %1.3f" % recall_score(Yt, Predict_Yt,average='weighted'))
print("\tF1: %1.3f\n" % f1_score(Yt, Predict_Yt,average='weighted'))

print(confusion_matrix(Yt, Predict_Yt))

# output
threshold = dt.tree_.threshold
features  = [feature_names[i] for i in dt.tree_.feature]
frame_len=[]
eth_type=[]
ip_proto=[]
ip_flags=[]
ipv6_nxt=[]
ipv6_opt=[]
tcp_srcport=[]
tcp_dstport=[]
tcp_flags=[]
udp_srcport=[]
udp_dstport=[]

for i, fe in enumerate(features):

    if fe == 'frame_len' and threshold[i]>-2:
        frame_len.append(threshold[i])
    elif fe == 'eth_type' and threshold[i]>-2:
        eth_type.append(threshold[i])
    elif fe == 'ip_proto' and threshold[i]>-2:
        ip_proto.append(threshold[i])
    elif fe == 'ip_flags' and threshold[i]>-2:
        ip_flags.append(threshold[i])
    elif fe == 'ipv6_nxt' and threshold[i]>-2:
        ipv6_nxt.append(threshold[i])
    elif fe == 'ipv6_opt' and threshold[i]>-2:
         ipv6_opt.append(threshold[i])
    elif fe == 'tcp_srcport' and threshold[i]>-2:
        tcp_srcport.append(threshold[i])
    elif fe == 'tcp_dstport' and threshold[i]>-2:
        tcp_dstport.append(threshold[i])
    elif fe == 'tcp_flags' and threshold[i]>-2:
        tcp_flags.append(threshold[i])
    elif fe == 'udp_srcport' and threshold[i]>-2:
        udp_srcport.append(threshold[i])
    else:
        if threshold[i]>-2:
	        udp_dstport.append(threshold[i])
#proto = [int(i) for i in proto]
#src = [int(i) for i in src]
#dst = [int(i) for i in dst]
#proto.sort()
#src.sort()
#dst.sort()

tree = open(outputfile,"w+")
tree.write("frame_len = ")
tree.write(str(frame_len))
tree.write(";\n")
tree.write("eth_type = ")
tree.write(str(eth_type))
tree.write(";\n")
tree.write("ip_proto = ")
tree.write(str(ip_proto))
tree.write(";\n")
tree.write("ip_flags = ")
tree.write(str(ip_flags))
tree.write(";\n")
tree.write("ipv6_nxt = ")
tree.write(str(ipv6_nxt))
tree.write(";\n")
tree.write("ipv6_opt = ")
tree.write(str(ipv6_opt))
tree.write(";\n")
tree.write("tcp_srcport = ")
tree.write(str(tcp_srcport))
tree.write(";\n")
tree.write("tcp_dstport = ")
tree.write(str(tcp_dstport))
tree.write(";\n")
tree.write("tcp_flags = ")
tree.write(str(tcp_flags))
tree.write(";\n")
tree.write("udp_srcport = ")
tree.write(str(udp_srcport))
tree.write(";\n")
tree.write("udp_dstport = ")
tree.write(str(udp_dstport))
tree.write(";\n")
get_lineage(dt,feature_names,tree)

tree.close()
