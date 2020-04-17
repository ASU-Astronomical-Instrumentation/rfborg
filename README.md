# rfborg: RFSoC detector readout software 

this library is for the firmware interface to the RFSoC ZCU111 with current firmware in development for MKID, uMux-TES, and QCD detector technologies. 

Interface consists as such 
USER <--> python-cli <---> redis-client <-------> redis-server <---> python-overlay <----> ZCU111
