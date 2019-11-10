# Intro

The framework provided under this folder implements a simple use case, where traffic from different applications is mapped to different ports.

# Framework 

There are three scripts in the framework:

## Extractfeature.py

### usage: ./Extractfeature.py -i [input pcap file] -o [output csv file]

Read the pcap file and convert to csv file. Extracts features: protocol, source port and destination port.

## Machinelearning.py
### usage: ./Machinelearning.py -i [csv file with label] -t [test csv file] -o [output txt file] 

Read the csv file and print the rules of a decision tree model into a txt file.

kmeans.py, svm.py and naivebayes.py provide similar functionality but for different training algorithms. 
Substitute the file to use.

## Runtime.py
### usage:  ./Runtime.py -i [input txt file] -o [output json file]

Reads the text file describing the rules of a  decision tree and outputs the json file which defines the table entries.

# Makefile: 
## make clean: 
remove the results file
## make build:
build the results file
## make class -i M(input file) -c (classification)
runs the Extract feature value
## make tree
runs the Machine learning script
## make runtime
runs the Runtime script
# Other files
## action.txt:
Used for changing actions of different classes.

## basic.p4
General p4 program for a switch data plane

## mycontroller.py
p4runtime program (control plane of the switch)
