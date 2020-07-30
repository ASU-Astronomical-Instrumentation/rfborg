import sys
import redis 
from time import sleep

print("Starting Programme...")

class Foo:
    def counter(self):
        for i in range(10):
            print(f"{i}", end=", ", flush=True)
        print()

hostname = 'commander'
r = redis.Redis(host=hostname)
p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe('drone1')
p.subscribe('hive') 
foo=Foo()

while True:
    msg = p.get_message()
    if msg:
        cmd=msg['data'].decode()
        print(str(cmd)) 
        if cmd == 'stop':
            break
        elif hasattr(foo,cmd):
            getattr(foo,cmd)()
        else:
            print("Invalid Command Entered")
    sleep(0.001)
p.close()
print("Exiting.")
