# Simple use case example

## Introduction
This example uses two parts of project's code:

1. ML training and model output: (../framwork)

2. The data plane and control plane for each algorithm (naive bayes, kmeans, decision tree, svm) 

## Environment Configuration:

We use the P4 tutorial VM as a simple environment for this example 

1. Install the P4 tutorial Virtual Machine:

* Download the virtual machine image

* Install VirtualBox

* Build the virtual machine from source

For the exact environment used in this example, follow the instructions on: https://p4.org/events/2018-06-06-p4-developer-day/

2. Clone the p4 tutorial repo: 
https://github.com/p4lang/tutorials

3. Install required packages: panda, scapy, sklearn, json.

## Framework

The framework folder has the scripts necessary for feature extraction, model training and control plane generation.

Detailed information can be found in the readme.md of the folder.

## naive bayes/kmeans/decision tree/svm

These folders are include simple devices built for the algorithms in use.

All the folders contain a p4 file and a p4runtime file (mycontroller.py) to build the device.

## Evaluation

1. Build the program in virtual machine:

make build: 

2. start the Mininet hosts:

xterm h1 h2..

3. send packets and received packets using the code in evaluation folder (known low performance).
