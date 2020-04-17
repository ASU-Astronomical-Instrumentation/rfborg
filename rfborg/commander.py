# commander.py
# command line commander
# redis server on localhost must be running
from subprocess import call
import redis 
# bind to host redis server ip
r = redis.Redis(host='localhost')

jokes=False
if jokes:
  call(['espeak "We are the RF Borg, your detector technology will be assimilated" 2>/dev/null'],shell=True)

"""
# list possible commands to send as key values
example_commands = ["command1","command2"]

while True:
  cmd = int(raw_input("send command:"))
  print("sent command: "+example_commands[cmd])

"""
