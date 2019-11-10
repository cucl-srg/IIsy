//
// Copyright (c) 2019 Noa Zilberman
// All rights reserved.
//
// @NETFPGA_LICENSE_HEADER_START@
//
// Licensed to NetFPGA C.I.C. (NetFPGA) under one or more contributor
// license agreements.  See the NOTICE file distributed with this work for
// additional information regarding copyright ownership.  NetFPGA licenses this
// file to you under the NetFPGA Hardware-Software License, Version 1.0 (the
// "License"); you may not use this file except in compliance with the
// License.  You may obtain a copy of the License at:
//
//   http://www.netfpga-cic.org
//
// Unless required by applicable law or agreed to in writing, Work distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations under the License.
//
// @NETFPGA_LICENSE_HEADER_END@
//


#include <core.p4>
#include <sume_switch.p4>

typedef bit<48> EthAddr_t; 
typedef bit<32> IPv4Addr_t;
typedef bit<16> TCPAddr_t;

#define IPV4_TYPE 0x0800
#define IPV6_TYPE 0x86DD
#define TCP_TYPE 6


//Standard Ethernet Header
header Ethernet_h {
    EthAddr_t dstAddr;
    EthAddr_t srcAddr;
    bit<16> etherType;
}

//IPv4 header without options
header IPv4_h {
    bit<4> version;
    bit<4> ihl;
    bit<8> tos;
    bit<16> totalLen;
    bit<16> identification;
    bit<3> flags;
    bit<13> fragOffset;
    bit<8> ttl;
    bit<8> protocol;
    bit<16> hdrChecksum;
    IPv4Addr_t srcAddr;
    IPv4Addr_t dstAddr;
}

//IPv6 header
header IPv6_h{
  bit<4> version;
  bit<8> trafficClass;
  bit<20> flowLabel;
  bit<16> payloadLen;
  bit<8> nxt;
  bit<8> hopLimit;
  bit<128> srcAddr;
  bit<128> dstAddr;
}

//TCP header without options
header TCP_h {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4> dataOffset;
    bit<4> res;
    bit<8> flags;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}


// List of all recognized headers
struct Parsed_packet {
    Ethernet_h ethernet;
    IPv4_h ip;
    IPv6_h ip6;
    TCP_h tcp;
}


// user defined metadata
// used for coding the decision 
struct user_metadata_t {
    bit<7> prob0;
    bit<7> prob1;
    bit<7> prob2;
    bit<7> prob3;
    bit<7> prob4;
}

// digest_data, MUST be 256 bits
struct digest_data_t {
    bit<256> unused;
}

// Parser Implementation


@Xilinx_MaxPacketRegion(8192)
parser TopParser(packet_in b,
                 out Parsed_packet p,
                 out user_metadata_t user_metadata,
                 out digest_data_t digest_data,
                 inout sume_metadata_t sume_metadata) {
    state start {
        b.extract(p.ethernet);
        transition select(p.ethernet.etherType) {
            IPV4_TYPE: parse_ipv4;
            IPV6_TYPE: parse_ipv6;
            default: accept;
        }
    }

    state parse_ipv4 {
        b.extract(p.ip);
        transition select(p.ip.protocol) {
            TCP_TYPE: parse_tcp;
            default: accept;
        }
    }

    state parse_ipv6 {
        b.extract(p.ip6);
        transition select(p.ip6.nxt) {
            TCP_TYPE: parse_tcp;
            default: accept;
        }
    }

    state parse_tcp {
        b.extract(p.tcp);
        transition accept;
    }
}


// match-action pipeline
control TopPipe(inout Parsed_packet p,
                inout user_metadata_t user_metadata, 
                inout digest_data_t digest_data,
                inout sume_metadata_t sume_metadata) {


 
    action set_prob0(bit<7> code){
        user_metadata.prob0 = code;
    }
    
    action set_prob1(bit<7> code){
        user_metadata.prob1 = code;
    }
    action set_prob2(bit<7> code){
        user_metadata.prob2 = code;
    }
    action set_prob3(bit<7> code){
        user_metadata.prob3 = code;
    }
    action set_prob4(bit<7> code){
        user_metadata.prob4 = code;
    }



// Calculate probability 0
    table tprob0{
        key = {  sume_metadata.pkt_len++p.ip.protocol++p.ip.flags++p.tcp.srcPort++p.tcp.dstPort:ternary @name("features"); }

         actions = {
            set_prob0;
            NoAction;
        }
        size = 63;
        default_action = NoAction;
    }

// Calculate probability 1
    table tprob1{
        key = {  sume_metadata.pkt_len++p.ip.protocol++p.ip.flags++p.tcp.srcPort++p.tcp.dstPort:ternary @name("features"); }

         actions = {
            set_prob1;
            NoAction;
        }
        size = 63;
        default_action = NoAction;
    }

// Calculate probability 2
  table tprob2 {
         key = {  sume_metadata.pkt_len++p.ip.protocol++p.ip.flags++p.tcp.srcPort++p.tcp.dstPort:ternary @name("features"); }
        
         actions = {
            set_prob2;
            NoAction;
        }
        size = 63;
        default_action = NoAction;
    }

// Calculate probability 3
  table tprob3 {
         key = {  sume_metadata.pkt_len++p.ip.protocol++p.ip.flags++p.tcp.srcPort++p.tcp.dstPort:ternary @name("features"); }

         actions = {
            set_prob3;
            NoAction;
        }
        size = 63;
        default_action = NoAction;
    }

// Calculate probability 4
  table tprob4{
         key = {  sume_metadata.pkt_len++p.ip.protocol++p.ip.flags++p.tcp.srcPort++p.tcp.dstPort:ternary @name("features"); }

         actions = {
            set_prob4;
            NoAction;
        }
        size = 63;
        default_action = NoAction;
    }


    apply {

        user_metadata.prob0=0;
        user_metadata.prob1=0;
        user_metadata.prob2=0;
        user_metadata.prob3=0;
        user_metadata.prob4=0;
       
        tprob0.apply();
        tprob1.apply(); 
        tprob2.apply();
        tprob3.apply();
        tprob4.apply();

//Select the destination port based on the classification - highest probability
        if ((user_metadata.prob0>user_metadata.prob1) && (user_metadata.prob0>user_metadata.prob2) && (user_metadata.prob0>user_metadata.prob3) && (user_metadata.prob0>user_metadata.prob4)) {
            sume_metadata.dst_port = 8w0b00000001;
        }
        else{
          if ((user_metadata.prob1>=user_metadata.prob0) && (user_metadata.prob1>user_metadata.prob2) && (user_metadata.prob1>user_metadata.prob3) && (user_metadata.prob1>user_metadata.prob4)) {
              sume_metadata.dst_port = 8w0b00000100;
          }
          else{
            if ((user_metadata.prob2>=user_metadata.prob0) && (user_metadata.prob2>=user_metadata.prob1) && (user_metadata.prob2>user_metadata.prob3) && (user_metadata.prob2>user_metadata.prob4)) {
                sume_metadata.dst_port = 8w0b00010000;
            }
            else{
              if ((user_metadata.prob3>=user_metadata.prob0) && (user_metadata.prob3>=user_metadata.prob1) && (user_metadata.prob3>=user_metadata.prob2) && (user_metadata.prob3>user_metadata.prob4)) {
                  sume_metadata.dst_port = 8w0b01000000;
              }
              else
              {
                    sume_metadata.dst_port = 8w0b00000010; //send to host
              }  
            } 
            } 
         }
      }
}

// Deparser Implementation
@Xilinx_MaxPacketRegion(1024)
control TopDeparser(packet_out b,
                    in Parsed_packet p,
                    in user_metadata_t user_metadata,
                    inout digest_data_t digest_data,
                    inout sume_metadata_t sume_metadata) { 
    apply {
        b.emit(p.ethernet); 
        b.emit(p.ip);
        b.emit(p.ip6);
	b.emit(p.tcp);
    }
}


// Instantiate the switch
SimpleSumeSwitch(TopParser(), TopPipe(), TopDeparser()) main;

