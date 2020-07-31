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
    
## Creating Redis Link Through Docker Containers
#### A Tale of Stack Overflow Posts
Running redis shell from docker container:

To run the redis interactive shell the Dockerfile must have CMD [“redis-server”,”--protected-mode no”] allowing redis-server to run in detached mode (-d)

Locate Dockerfile and run the command docker build -t “redis_image” . 
Check the image has been built successfully docker images ls
Run the docker image docker run --name “redis_container” -d redis_image
Check the container was made docker container ls

From the container we can open a redis shell docker exec -it redis_container sh

From this shell you can run as a redis client or execute a python script (i.e. You are IN the container utilizing the packages installed through the Dockerfile!)
Redis Client:
Type redis-cli to open shell as a redis client.
OR
docker exec -it redis_container redis-cli
Python:
Type python3
Run script contained in Dockerfile python3 script.py
Note: script.py must be in Docker container (or manually input). It is possible to copy a file from the host computer into a docker container (i.e. a user can run there own script from a docker container). docker cp script.py redis_container:path/script.py 


You can connect to another container.  
docker run --name “new_redis_container” --link redis_container:redis_image -d redis_image
Open a new interactive shell docker exec -it new_redis_container sh

You can now run redis client and communicate with the linked container:
In this shell run the same command but with a tagged host image redis-cli -h redis_image

You can also run a python script importing redis and setting host='redis_container' when instatiating the redis class:
r = redis.Redis(host = 'redis_container')
This links your python script to the 'redis_container', which in turn should be linked to the host machine.

