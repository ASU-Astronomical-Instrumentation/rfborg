# commander.py
# command line commander
# redis server on localhost must be running
import redis

# bind to host redis server ip
r = redis.Redis(host='localhost')
# set channel(s) to publish to

chnls = ['drone1','drone2','hive']
command_list = ['counter','VNASweep']
print(f"Publishing to \'{chnls}\'...")
def usrInput(command_list):
    while True:
        print("Which channel would you like to publish to?"+'\n' + str(chnls))
        drone = str(input())
        if drone in chnls:
            print("Publishing to " + str(drone))
            while True:
                print("What message would you like to publish?")
                print("To select a different drone enter 'change'.")
                # print list of commands
                command = str(input())
                if command == 'stop':
                    r.publish(drone,command)
                    break
                elif command == 'change':
                    print("Changing drone selection...")
                    break
                elif command in command_list:
                    print("Sending " +str(command))
                    r.publish(drone,command)
                    print("Published")
                else:
                    print("Invalid command.")
            if command == 'stop':
                break # Breaks the outer while loop
            else:
                continue
        else:
            print("Try a different channel.")
    print("Exiting Commander")
usrInput(command_list)
