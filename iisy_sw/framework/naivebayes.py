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

# naive base fit
clf = GaussianNB()
clf.fit(X, Y)
Predict_Y = clf.predict(X)
print(accuracy_score(Y, Predict_Y))

Predict_Yt = clf.predict(Xt)
print(accuracy_score(Yt, Predict_Yt))

# output the model in a text file, wirte it
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

model = open(outputfile,"w+")

aver_feature1_0 = np.array(Training_0[:,0]).mean()
var_feature1_0 = np.array(Training_0[:,0]).var()+0.001
aver_feature2_0 = np.array(Training_0[:,1]).mean()
var_feature2_0 = np.array(Training_0[:,1]).var()+0.001
aver_feature3_0 = np.array(Training_0[:,2]).mean()+0.001
var_feature3_0 = np.array(Training_0[:,2]).var()



model.write("class 0: \n")
model.write("feature 1, average value: " + str(aver_feature1_0)  + ", standard error: " + str(var_feature1_0)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature2_0)  + ", standard error: " + str(var_feature2_0)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature3_0)  + ", standard error: " + str(var_feature3_0)+ ";\n")



aver_feature1_1 = np.array(Training_1[:,0]).mean()
var_feature1_1 = np.array(Training_1[:,0]).var()+0.001
aver_feature2_1 = np.array(Training_1[:,1]).mean()
var_feature2_1 = np.array(Training_1[:,1]).var()+0.001
aver_feature3_1 = np.array(Training_1[:,2]).mean()
var_feature3_1 = np.array(Training_1[:,2]).var()

model.write("class 1: \n")
model.write("feature 1, average value: " + str(aver_feature1_1)  + ", standard error: " + str(var_feature1_1)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature2_1)  + ", standard error: " + str(var_feature2_1)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature3_1)  + ", standard error: " + str(var_feature3_1)+ ";\n")


aver_feature1_2 = np.array(Training_2[:,0]).mean()
var_feature1_2 = np.array(Training_2[:,0]).var()+0.001
aver_feature2_2 = np.array(Training_2[:,1]).mean()
var_feature2_2 = np.array(Training_2[:,1]).var()+0.001
aver_feature3_2 = np.array(Training_2[:,2]).mean()
var_feature3_2 = np.array(Training_2[:,2]).var()+0.001

model.write("class 2: \n")
model.write("feature 1, average value: " + str(aver_feature1_2)  + ", standard error: " + str(var_feature1_2)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature2_2)  + ", standard error: " + str(var_feature2_2)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature3_2)  + ", standard error: " + str(var_feature3_2)+ ";\n")




aver_feature1_3 = np.array(Training_3[:,0]).mean()
var_feature1_3 = np.array(Training_3[:,0]).var()+0.001
aver_feature2_3 = np.array(Training_3[:,1]).mean()
var_feature2_3 = np.array(Training_3[:,1]).var()+0.001
aver_feature3_3 = np.array(Training_3[:,2]).mean()
var_feature3_3 = np.array(Training_3[:,2]).var()+0.001

model.write("class 3: \n")
model.write("feature 1, average value: " + str(aver_feature1_3)  + ", standard error: " + str(var_feature1_3)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature2_3)  + ", standard error: " + str(var_feature2_3)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature3_3)  + ", standard error: " + str(var_feature3_3)+ ";\n")



aver_feature1_4 = np.array(Training_4[:,0]).mean()
var_feature1_4 = np.array(Training_4[:,0]).var()+0.001
aver_feature2_4 = np.array(Training_4[:,1]).mean()
var_feature2_4 = np.array(Training_4[:,1]).var()+0.001
aver_feature3_4= np.array(Training_4[:,2]).mean()
var_feature3_4= np.array(Training_4[:,2]).var()+0.001

model.write("class 4: \n")
model.write("feature 1, average value: " + str(aver_feature1_4)  + ", standard error: " + str(var_feature1_4)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature2_4)  + ", standard error: " + str(var_feature2_4)+ ";\n")
model.write("feature 2, average value: " + str(aver_feature3_4)  + ", standard error: " + str(var_feature3_4)+ ";\n")



model.close()
