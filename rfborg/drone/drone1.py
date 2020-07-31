from time import sleep
import sys
import subprocess
import redis 
import json
import somefirmware as foo

if sys.version_info < (3,0):
    sys.exit("Please use Python >= 3.0")
subprocess.run("clear")

print(50*"=",end="\n")
print("Starting Programme...")
print(50*"=",end="\n\n")

# load firmware config
# lambda method use for general purpose firmware loading
f="somefirmware" # can be a user input
jsonpath= lambda name : "./"  + name + ".json"
cmdpath = lambda name : "./"  + name + ".py"

# Reading JSON File
with open(jsonpath(f),'r') as cmdlist:
    command_obj=cmdlist.read()
command_dict=json.loads(command_obj)

print("Command List:")
print(35*"-")
for c in command_dict:
    print(f"{c} | cmd: {command_dict[c]} ")
print("\n")

# Starting Redis client
hostname = 'commander' # Link drone to commander container
r = redis.Redis(host=hostname)
chnls_open = r.pubsub_channels()
print(f"Channels currently open: \'{chnls_open}\'" )

# Subscribing to channels
chnls = ['drone1','hive']
print(f"Subscribing to \'{chnls}\'...")
p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe('drone1')
p.subscribe('hive')

#foo = cmdpath

animation = "|/-\\"
i=0
while True:
    msg = p.get_message()
    if msg:
        chnl = msg['channel'].decode()
        cmd=msg['data'].decode()
        print(f"Message Recieved: \"{cmd}\"")
        try:
            if cmd == 'stop':
                break
            elif hasattr(foo,command_dict[cmd]):
                print(f"Running \'{command_dict[cmd]}\' Command.\n")
                getattr(foo,command_dict[cmd])()
                print("")
                confirmation = 'Running command'
                r.publish('borg',confirmation)
            else:
                print("Invalid Command Entered")
        except KeyError:
            print("Use keys from the command list.")
    sleep(0.1)
    sys.stdout.write("\rReady to Recieve Messages. " + animation[i%4])
    sys.stdout.flush()
    i+=1
p.close()
print("Exiting.")
