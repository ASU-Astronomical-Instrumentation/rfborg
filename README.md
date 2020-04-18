# rfborg: RFSoC detector readout software 
# -------------------------------------------------------------  
this library is for the firmware interface to the RFSoC ZCU111 with current firmware in development for MKID, uMux-TES, RF-SNSPD, and QCD detector technologies.
Remote control system is built using Docker. 
## Interface Layout  
USER <---> python-cli <---> redis-client <---> redis-server <---> python-overlay <---> ZCU111
