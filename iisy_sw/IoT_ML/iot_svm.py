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
from sklearn import svm
from sklearn.metrics import *
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
import pydotplus



parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i', required=True, help='path to training set')
parser.add_argument('-o', required=True, help='path to outputfile')
parser.add_argument('-t', required=True, help='path to test set')
args = parser.parse_args()

input = args.i
outputfile = args.o
test=args.t


Set1 = pd.read_csv(input)
Set1 = Set1.apply(pd.to_numeric, downcast='float', errors='coerce')
#print(Set1.dtypes)

Set = Set1.values.tolist()
X = [i[0:11] for i in Set]
Y = [i[11] for i in Set]
class_names=['smart-static','sensor','audio','video','else']
feature_names=['frame_len','eth_type','ip_proto','ip_flags','ipv6_nxt','ipv6_opt','tcp_srcport','tcp_dstport','tcp_flags','udp_srcport','udp_dstport']



#debug = open("debug.txt","w+")
#debug.write("Y = ")
#debug.write(str(Y))
#debug.write(";\n")
#debug.close()


#prepare training and testing set
X = np.array(X,dtype=float)
Y = np.array(Y,dtype=float)


# SVM fit
clf = svm.LinearSVC(random_state=8)
clf.fit(X,Y) 


Predict_Y = clf.predict(X)
print("Original dataset")
print(accuracy_score(Y, Predict_Y))
#print("\tBrier: %1.3f" % (clf_score))
print("\tPrecision: %1.3f" % precision_score(Y, Predict_Y,average='weighted'))
print("\tRecall: %1.3f" % recall_score(Y, Predict_Y,average='weighted'))
print("\tF1: %1.3f\n" % f1_score(Y, Predict_Y,average='weighted'))


Set2 = pd.read_csv(test)
Set2 = Set2.apply(pd.to_numeric, downcast='float', errors='coerce')
#print(Set1.dtypes)

Set_t = Set2.values.tolist()
X_t = [i[0:11] for i in Set_t]
Y_t = [i[11] for i in Set_t]

Predict_Yt = clf.predict(X_t)

print("test dataset")
print(accuracy_score(Y_t, Predict_Yt))
#print("\tBrier: %1.3f" % (clf_score))
print("\tPrecision: %1.3f" % precision_score(Y_t, Predict_Yt,average='weighted'))
print("\tRecall: %1.3f" % recall_score(Y_t, Predict_Yt,average='weighted'))
print("\tF1: %1.3f\n" % f1_score(Y_t, Predict_Yt,average='weighted'))

# output


SV=clf.coef_

print(SV)

print("printing items")
for item in SV:
   print(item)

# output the model in a text file, write
coe = clf.coef_
intr = clf.intercept_

model = open(outputfile,"w+")
for i in range(len(coe)):
    model.write("hyperplane = ")
    for j in range(11):
       model.write(str(coe[i][j-1]) + "x"+str(j)+ "+ ")
    model.write(str(intr[i])+";\n")

model.close()
