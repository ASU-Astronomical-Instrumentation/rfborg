##################################################################################
# droneFun.py
# Sends command to DroneFun.py using fun.json file value keys
##################################################################################

import sys
import subprocess
import redis
import json
import fun as foo       #marries fun.py and fun.json
from time import sleep

# PART 1 ##################################################
# Ensures that the correct veresion of python is present
if sys.version_info < (3,7): #checking for python version...
	sys.exit("Please use Python >=3.7")
subprocess.run("clear")
print(50*"=",end="\n")
print("Starting Programme...")
print(50*"=",end="\n\n")

# PART 2 ##################################################
# load firmware config
# lambda method use for general purpose firmware loading
f = "fun" # can be a user input
jsonpath = lambda name : "./" + name + "/" + name + ".json"
cmdpath = lambda name : "./" + name + "/" + name + ".py"

# Reading JSON File
with open(jsonpath(f),'r') as cmdlist:
    command_obj = cmdlist.read()
command_dict = json.loads(command_obj)
#connects variable command_dict to fun.py/.json and can be used to reference
#   either file

# PART 3 ##################################################
print("Command List:")
print(35*"-")
for c in command_dict:
    print(f"{c} | cmd: {command_dict[c]} ") #will only have one command (00: funHello)
print("\n")

# PART 4 ##################################################
# Starting Redis client
chnl ="python-channel"
chnl2 = "borg"
print(f"Subscribing to \'{chnl}\'...")
r = redis.Redis()
p = r.pubsub(ignore_subscribe_messages=True)	#the messages for sub/unsub are read but won't send confirmation messages
p.subscribe(chnl)			#drone subscribes to channel here
print(f"Subscribed to \'{chnl}\'.\n")

# PART 5 ##################################################
animation = "|/-\\"
i=0
while True:
    msg = p.get_message()
    if msg:
        cmd=msg['data'].decode()
        print(f"Message Recieved: \"{cmd}\"")
        if cmd == 'stop':
            break
        elif hasattr(foo,command_dict[cmd]):
            print(f"Running \'{command_dict[cmd]}\' Command.\n")
            getattr(foo,command_dict[cmd])()
            print("")
        else:
            print("Invalid Command Entered")
    sleep(0.1)
    sys.stdout.write("\rReady to Recieve Messages. " + animation[i%4])
    sys.stdout.flush()
    i+=1
p.close()
print("Exiting.")
