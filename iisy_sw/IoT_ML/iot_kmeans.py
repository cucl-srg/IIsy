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
from sklearn.cluster import KMeans
from sklearn.metrics import *
#from sklearn.cluster import export_graphviz
from sklearn.preprocessing import StandardScaler
import pydotplus



parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i', required=True, help='path to dataset')
parser.add_argument('-o', required=True, help='path to outputfile')
parser.add_argument('-t', required=True, help='path to testfile')

args = parser.parse_args()

input = args.i
outputfile = args.o
testfile = args.t


Set1 = pd.read_csv(input)
Set = Set1.values.tolist()
#print(Set1.describe())

X = [i[0:11] for i in Set]
Y = [i[11] for i in Set]
class_names=['smart-static','sensor','audio','video','else']
feature_names=['frame_len','eth_type','ip_proto','ip_flags','ipv6_nxt','ipv6_opt','tcp_srcport','tcp_dstport','tcp_flags','udp_srcport','udp_dstport']


# prepare training and testing set
X = np.array(X)
Y = np.array(Y)

# kmeans fit
kmeans = KMeans(n_clusters=5, random_state= 9).fit(X)

Predict_Y = kmeans.predict(X)
print(accuracy_score(Y, Predict_Y))
print("\tPrecision: %1.3f" % precision_score(Y, Predict_Y,average='weighted'))
print("\tRecall: %1.3f" % recall_score(Y, Predict_Y,average='weighted'))
print("\tF1: %1.3f\n" % f1_score(Y, Predict_Y,average='weighted'))
print("\tConfusion matrix:\n" )
print(confusion_matrix(Y, Predict_Y))


# Test set X and Y
Set2 = pd.read_csv(testfile)
Sett = Set2.values.tolist()
Xt = [i[0:11] for i in Sett]
Yt =[i[11] for i in Sett]

# prepare training and testing set
Xt = np.array(Xt)
Yt = np.array(Yt)

# fit
Predict_Yt = kmeans.predict(Xt)
print(accuracy_score(Yt, Predict_Yt))
print("\tPrecision: %1.3f" % precision_score(Yt, Predict_Yt,average='weighted'))
print("\tRecall: %1.3f" % recall_score(Yt, Predict_Yt,average='weighted'))
print("\tF1: %1.3f\n" % f1_score(Yt, Predict_Yt,average='weighted'))


print(confusion_matrix(Yt, Predict_Yt))


# output the model in a text file, wirte it
centre = kmeans.cluster_centers_

model = open(outputfile,"w+")
for i in range(len(centre)):
    model.write("centre point : ( ")
    for j in range(11):
      model.write(str(centre[i][j])+",")
    model.write(");\n")

model.close()


