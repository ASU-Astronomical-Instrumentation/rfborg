import json 

with open("somefirmware.json") as f:
    data=json.load(f)

def displayCommands(data):
    cmds=list(data.keys())
    for cmd in cmds:
        x=data[cmd]
        if type(x)==str:
            print(f"{cmd} : {x}")
        else:
            funcp=(next(iter(x)))
            print(f"{cmd} : {funcp}")
            for param,val in x[funcp].items():
                print(f"\t\\{param} : {val}")
    return None

displayCommands(data)