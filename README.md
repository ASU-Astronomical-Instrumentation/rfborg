# rfborg: RFSoC Detector Readout Software 
this library is for the firmware interface to the RFSoC ZCU111 with current firmware in development for MKID, μMux-TES, RF-SNSPD, and QCD detector technologies.  

## Setting up Control PC with Docker
to be added
## General Info
### Interface Layout  
USER <---> python-cli <---> redis-client <---> redis-server <---> python-overlay <---> ZCU111
