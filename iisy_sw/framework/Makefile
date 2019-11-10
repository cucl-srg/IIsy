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

BUILD_DIR = results

Extract_SCRIPT = ./Extractfeature.py
Csv = ./results/feature.csv


ML = ./Machinelearning.py
Decision = ./results/tree.txt

Runtime =  ./Runtime.py
Json = ./results/runtime.json
Action = ./action.txt

build: 
	mkdir results

class:
	$(Extract_SCRIPT) -i $(M) -o $(Csv) -c $(C)

	
tree:
	$(ML) -i $(Csv) -o $(Decision)

runtime:
	$(Runtime) -i1 $(Decision) -i2 $(Action) -o $(Json)
	

clean: 
	rm -rf $(BUILD_DIR) 

	
      
