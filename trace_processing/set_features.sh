#!/bin/bash
#################################################################################
#
# Copyright (c) 2019 Noa Zilberman
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
#
# Description: this file takes as input a folder with pcap files, and converts them
# to CSV files. It extracts just specific features form the file, e.g., frame len,
# Ether type, IP protocols etc.
#
# You will need python and tshark installed to run this code
#

FILES=$(find original_files/ -type f)
TARGET='csv_files'

echo "Usage: ./set_features.py <substitution file>"

for file in $FILES; do
    echo "${file}"
    rm tmp
    ofile="$(cut -d'/' -f2 <<<"$file" |cut -d'.' -f1)"
    tshark -r ${file} -Tfields -E occurrence=f -E separator=, -e frame.len -e eth.type -e ip.proto -e ip.flags -e ipv6.nxt -e ipv6.opt -e tcp.srcport -e tcp.dstport -e tcp.flags -e udp.srcport -e udp.dstport  -e eth.src > ${ofile}.csv
    cp ${ofile}.csv  else.csv
    while IFS= read -r line
    do
      MAC="$(echo $line |cut -d/ -f1)"
      grep -i $MAC ${ofile}.csv |sed  "s/$line/gI" >>tmp
      grep -v -i $MAC else.csv >else1.csv
      mv else1.csv else.csv
    done < "$1"
    mv tmp ${TARGET}/${ofile}-labeled.csv
    rm ${ofile}.csv
    cat else.csv | sed 's/.\{17\}$/4/' >> ${TARGET}/${ofile}-labeled.csv
    cat ${TARGET}/${ofile}-labeled.csv |sed 's/,,/,-1,/gI' | sed 's/,,/,-1,/gI' > ${TARGET}/${ofile}-labeled.csv1
    mv ${TARGET}/${ofile}-labeled.csv1 ${TARGET}/${ofile}-labeled.csv 
done
