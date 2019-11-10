This folder contains the source files for the implementation of IIsy in P4-NetFPGA on NetFPGA-SUME, for the IoT use case.

To use this code you will need the P4-NetFPGA repository: https://github.com/NetFPGA/P4-NetFPGA-live/ (open source, but requires registration through https://goo.gl/forms/h7RbYmKZL7H4EaUf1).

The P4-NetFPGA commit used in this work was 5bd666ec8dcff3c7bb182e3654851e275f2ddf52 (May 8, 2019).

The code should be placed under $P4_DESIGN_DIR/src.  
The easiest way to compile the code is to update $SUME_FOLDER/tools/settings.sh, setting P4_PROJECT_NAME to iisy and using the p4 file of your choice. We used switch_calc as the base design that was replicated (i.e. 'cp -r switch_calc iisy').

The files in this folder are as follows:

1. iisy_decision_tree.p4 - The P4 implementation of a decision tree for NetFPGA.

2. iisy_svm.p4 - The P4 implementation of SVM for NetFPGA. 

3. iisy_naive_bayes.p4 - The P4 implementation of Naive Bayes for NetFPGA.

4. iisy_kmeans.p4 - The P4 implementation of K-means for NetFPGA.

5. commands.txt - The control plane generation file, matching the decision tree use case.

The bitfiles (compiled files to the NetFPGA target) can be found under https://www.cl.cam.ac.uk/research/srg/netos/projects/iisy. 
They can not be included here due to Xilinx license restrictions.


