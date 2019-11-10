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

from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd
import argparse

from sklearn.metrics import *
from sklearn.naive_bayes import GaussianNB
import pydotplus


from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.tree import export_graphviz
import pydotplus
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn import linear_model 



parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-i', required=True, help='path to dataset')
parser.add_argument('-o', required=True, help='path to outputfile')
parser.add_argument('-t', required=True, help='path to testfile')
args = parser.parse_args()

# extract argument
input = args.i
outputfile = args.o
testfile = args.t


# Training set X and Y
Set1 = pd.read_csv(input)
Set = Set1.values.tolist()
X = [i[0:11] for i in Set]
Y =[i[11] for i in Set]
class_names=['smart-static','sensor','audio','video','else']
feature_names=['frame_len','eth_type','ip_proto','ip_flags','ipv6_nxt','ipv6_opt','tcp_srcport','tcp_dstport','tcp_flags','udp_srcport','udp_dstport']


# prepare training and testing set
X = np.array(X)
Y = np.array(Y)

# fit
clf = GaussianNB()
clf.fit(X, Y)
Predict_Y = clf.predict(X)
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
Predict_Yt = clf.predict(Xt)
print(accuracy_score(Yt, Predict_Yt))
print("\tPrecision: %1.3f" % precision_score(Yt, Predict_Yt,average='weighted'))
print("\tRecall: %1.3f" % recall_score(Yt, Predict_Yt,average='weighted'))
print("\tF1: %1.3f\n" % f1_score(Yt, Predict_Yt,average='weighted'))


# output the model in a text file

model = open(outputfile,"w+")

Training_0 =[]
Training_1 =[]
Training_2 =[]
Training_3 =[]
Training_4 =[]
for i,cate in enumerate(Y):
    if  cate ==0:
        Training_0.append(X[i])
    elif  cate ==1:
        Training_1.append(X[i])
    elif  cate ==2:
        Training_2.append(X[i])
    elif  cate ==3:
        Training_3.append(X[i])
    else:
        Training_4.append(X[i])


Training_0 = np.array(Training_0)
Training_1 = np.array(Training_1)
Training_2 = np.array(Training_2)
Training_3 = np.array(Training_3)
Training_4 = np.array(Training_4)




model.write("class 0: \n")
for j in range(11):
   aver_feature = np.array(Training_0[:,j]).mean()
   var_feature  = np.array(Training_0[:,j]).var()
   model.write("feature "+str(j)+", average value: " + str(aver_feature)  + ", standard error: " + str(var_feature)+ ";\n")

model.write("class 1: \n")
for j in range(11):
   aver_feature = np.array(Training_1[:,j]).mean()
   var_feature  = np.array(Training_1[:,j]).var()
   model.write("feature "+str(j)+", average value: " + str(aver_feature)  + ", standard error: " + str(var_feature)+ ";\n")

model.write("class 2: \n")
for j in range(11):
   aver_feature = np.array(Training_2[:,j]).mean()
   var_feature  = np.array(Training_2[:,j]).var()
   model.write("feature "+str(j)+", average value: " + str(aver_feature)  + ", standard error: " + str(var_feature)+ ";\n")

model.write("class 3: \n")
for j in range(11):
   aver_feature = np.array(Training_3[:,j]).mean()
   var_feature  = np.array(Training_3[:,j]).var()
   model.write("feature "+str(j)+", average value: " + str(aver_feature)  + ", standard error: " + str(var_feature)+ ";\n")

model.write("class 4: \n")
for j in range(11):
   aver_feature = np.array(Training_4[:,j]).mean()
   var_feature  = np.array(Training_4[:,j]).var()
   model.write("feature "+str(j)+", average value: " + str(aver_feature)  + ", standard error: " + str(var_feature)+ ";\n")

model.close()
