IIsy - In Network Inference Made Easy

# Introduction

In-network classification refers to taking classification decision within network devices (e.g., switches, NICs), as the data goes through the network.

IIsy is a framework that maps the output of a machine learning training framework to a programmable network device. Currently IIsy supports scikit-learn as the training framework. Two network-device targets are currently supported by IIsy: bmv2 and NetFPGA SUME.

bmv2 is a behavioral model of a P4-based switch, and it is used with the v1model architecture. The switch is emulated using Mininet. P4Runtime is used for the control plane.

NetFPGA SUME is an open source platform for rapid prototyping of network devices. The board uses the Xilinx Virtex-7 690T FPGA and utilizes 4x10GE ports. Here, the board is used with the P4->NetFPGA workflow and the SimpleSumeSwitch architecture. The control plane is P4->NetFPGA proprietary.

# Installation

As each component under this repository is independent, installation instructions and dependencies are listed separately under each folder. This means that you can run the software environment without installing the NetFPGA environment and vice versa. 

# Structure

The repository is structured as follows:

1. trace_processing - The trace_processing folder is used by the training stage. It is used to convert trace files (pcap format) to text files (csv format) that can be processed by the ML framework (scikit-learn), and adds labels. The labelling fits the classes we used in this work.

2. iisy_sw - The software components of IIsy. This folder includes both the ML training scripts and the mapping from ML-training to the software switch.

3. iisy_hw - The hardware implementation of IIsy over NetFPGA SUME, using P4-NetFPGA.

Refer to the README files under each folder for more information.

# License

This project is released under the NetFPGA C.I.C license (http://netfpga-cic.org/)

The NetFPGA C.I.C license is a modified version of Apache License Version 2.0 to support also hardware targets.

# Citation

When referencing this work, please use the following citation:

[1] Zhaoqi Xiong and Noa Zilberman, "Do Switches Dream of Machine Learning? Toward In-Network Classification", In the Proceedings of ACM Workshop on Hot Topics in Networks (HotNets), 2019.

An open access version of the paper is available at https://doi.org/10.17863/CAM.45171.
