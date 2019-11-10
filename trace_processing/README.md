# Trace Processing

This folder contains the script required to extract data from traces and assign labels. It is customized to the IoT packet classification use case, but can be easily adapted to other use cases.
Labels are assigned based on the MAC address of the devices, where each MAC address is substituted for the class number.

The classes are enumerated as follows:
0 - Static smart
1 - Sensors
2 - Audio
3 - Video
4 - Others

pcap files are expected to be in a sub-folder called original_files, and the processed files are created in a sub-folder called csv_files. These paths can be changed within the script.

The file replacement numeric provides a mapping of a MAC address to a numeric class substitute.

To invoke the script, use ./set_features.sh replacement_numeric

Dependencies: python, tshark