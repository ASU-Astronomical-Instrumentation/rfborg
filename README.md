# rfborg: RFSoC Detector Readout Software 
this library is for the firmware interface to the RFSoC ZCU111 with current firmware in development for MKID, μMux-TES, RF-SNSPD, and QCD detector technologies.  

## Setting up Control PC with Docker
to be added
## General Info
### Interface Layout  
general diagram for how user input will map to firmware routines.  
>
> UI <---> [commander.py -- redis-PUB] <---> [redis-SUB -- drone.py] <----> firmware-overlay <---> ZCU111  
>


1. Processes in Container
    * __UI__:  get user input, display data  
    * __commander.py__:  link user commands to values in the command list
    * __redis-PUB__:  publishes message from the commandar.py output   
2. Process in RFSOC
    * __redis-SUB__:  listens for messages on subsriber channel, recieved messages are sent to drone.py 
    * __drone.py__:  subsriber-messages are decoded and mapped to a firmware-specific command list 
    * __firmware-overaly__:  python file which runs command issued by drone.py