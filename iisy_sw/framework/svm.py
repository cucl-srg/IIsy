#!/usr/bin/env python
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
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd
import argparse

from sklearn.metrics import accuracy_score

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
X = [i[0:3] for i in Set]
Y =[i[3] for i in Set]
class_names=['iperf','memcached','ping','sparkglm','sparkkmeans']
feature_names=['proto','src','dst']

# Test set Xt and Yt
Set2 = pd.read_csv(input)
Sett = Set2.values.tolist()
Xt = [i[0:3] for i in Set]
Yt =[i[3] for i in Set]

# prepare training and testing set
X = np.array(X)
Y = np.array(Y)
Xt = np.array(Xt)
Yt = np.array(Yt)

# svm fit
clf = SVC(kernel = 'linear')
clf.fit(X, Y)
Predict_Y = clf.predict(X)
print(accuracy_score(Y, Predict_Y))

Predict_Yt = clf.predict(Xt)
print(accuracy_score(Yt, Predict_Yt))

# output the model in a text file, wirte it
coe = clf.coef_
int = clf.intercept_

model = open(outputfile,"w+")
for i in range(len(coe)):
    model.write("hyperplane = ")
    model.write(str(coe[i][0]) + "x1 + "+ str(coe[i][1]) + "x2 + "+ str(coe[i][2])+ "x3 + " + str(int[i]))
    model.write(";\n")

model.close()
