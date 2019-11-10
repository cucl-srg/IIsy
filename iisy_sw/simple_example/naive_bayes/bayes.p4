/* -*- P4_16 -*- */
/********************************************************************************
*
* Copyright (c) 2019 Zhaoqi Xiong
* All rights reserved.
*
*
* @NETFPGA_LICENSE_HEADER_START@
*
* Licensed to NetFPGA C.I.C. (NetFPGA) under one or more contributor
* license agreements.  See the NOTICE file distributed with this work for
* additional information regarding copyright ownership.  NetFPGA licenses this
* file to you under the NetFPGA Hardware-Software License, Version 1.0 (the
* "License"); you may not use this file except in compliance with the
* License.  You may obtain a copy of the License at:
*
*   http://www.netfpga-cic.org
*
* Unless required by applicable law or agreed to in writing, Work distributed
* under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
* CONDITIONS OF ANY KIND, either express or implied.  See the License for the
* specific language governing permissions and limitations under the License.
*
* @NETFPGA_LICENSE_HEADER_END@
*
********************************************************************************/ 

#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<3>  res;
    bit<3>  ecn;
    bit<6>  ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

struct metadata {
    bit<32> action_select1;
    bit<32> action_select2;
    bit<32> classification;
    bit<32> x;
    bit<32> y;
}

struct headers {
    ethernet_t   ethernet;
    ipv4_t     ipv4;
    tcp_t      tcp;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {
    
    state start {
        transition parse_ethernet;
    }
    
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
}
}
    
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            6: parse_tcp;
            default: accept;
    }
    }
    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
}
}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop();
    }
    
    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
                  }


action set_p1(bit<32> square){
    meta.x =  square;
}
action set_p2(bit<32> square ){
    meta.y =  square;
}

action set_select1(bit<32> probility){
    meta.action_select1 = probility;
}

action set_select2(bit<32> probility){
    meta.action_select2 = probility;
}

table class1_p1 {
    key = {
        hdr.tcp.srcPort: exact;
        }
        actions = {
            NoAction;
            set_p1;
                }
                    size = 65535;
}

table class1_p2 {
    key = {
    hdr.tcp.dstPort: exact;
        }
        actions = {
            NoAction;
            set_p2;
            }
                size = 65535;
}

table class2_p1 {
    key = {
        hdr.tcp.srcPort: exact;
        }
        actions = {
            NoAction;
            set_p1;
                }
                    size = 65535;
}

table class2_p2 {
    key = {
    hdr.tcp.dstPort: exact;
        }
        actions = {
            NoAction;
            set_p2;
            }
                size = 65535;
}

table class1_pro {
    key = {
    meta.x: range;
    meta.y: range;
        }
        actions = {
            NoAction;
            set_select1;
            }
                size = 70000;
}

table class2_pro {
    key = {
    meta.x: range;
    meta.y: range;
        }
        actions = {
            NoAction;
            set_select2;
        }
            size = 700000;
}



table ipv4_exact {
    key = {
        meta.classification: exact;
}
    
    actions = {
        ipv4_forward;
        drop;
        NoAction;
}
    size = 1024;
        default_action = drop();
    }

    apply {
        if (hdr.ipv4.isValid() ) {
            if(hdr.ipv4.protocol ==6) {
                class1_p1.apply();
                class1_p2.apply();
                class1_pro.apply();
                    
                    class2_p1.apply();
                    class2_p2.apply();
                    class2_pro.apply();

if ( meta.action_select1 >= meta.action_select2 )
    {  meta.classification = 1; }
        else { meta.classification = 2;}
}

}

ipv4_exact.apply();

}
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
    apply {
    update_checksum(
                    hdr.ipv4.isValid(),
                    { hdr.ipv4.version,
                    hdr.ipv4.ihl,
                    hdr.ipv4.diffserv,
                    hdr.ipv4.totalLen,
                    hdr.ipv4.identification,
                    hdr.ipv4.flags,
                    hdr.ipv4.fragOffset,
                    hdr.ipv4.ttl,
                    hdr.ipv4.protocol,
                    hdr.ipv4.srcAddr,
                    hdr.ipv4.dstAddr },
                    hdr.ipv4.hdrChecksum,
                    HashAlgorithm.csum16);
}
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
}
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
         MyParser(),
         MyVerifyChecksum(),
         MyIngress(),
         MyEgress(),
         MyComputeChecksum(),
         MyDeparser()
         ) main;
