# drone.py
#import firmware_drivers as fw
#import detector_functions as det
#import command_list as cmd_list

import sys
import redis
# bind to host redis server ip and start redis client
r = redis.Redis(host='localhost')
designation = sys.argv[1]
r.client_setname(designation)
p = r.pubsub()
p.subscribe("cmd")
# while waiting for command
for new_message in p.listen() :
  print("new message received"+str(new_message["data"]))
  print("Performing action:")
  r.publish('ack',1)
  #cmd = r.get('cmd')
  #print("Received command index: "+cmd)
  #print("Corresponding command: "+cmd_list[cmd]) 
