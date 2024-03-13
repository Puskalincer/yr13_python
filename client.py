from py_mp import CommandClient
from py_mp import ClientCommand
from py_mp.commands import NetworkFlag
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def divider():
    print("\n" + 34 * "-" + "\n")
def list(items,b_t=0):
    divider()
    print(items[0])
    for idx , array_item in enumerate(items[1] , start=1):
        print(str(idx) + " - "+ array_item)
    divider()
    if b_t == 1:
        print(items[2])
    return len(items[1])
def query_server():
    try:
        client = CommandClient("localhost", 6433)
        # Send a Test Command to the Server
        client.send(ClientCommand(NetworkFlag.CONNECTED, data=0))

        # Receive a Command from the Server
        com = client.recv()
        question = com.args["data"]
        
        list([question['question'],question['choices']])


    except:
        print("Failed to connect")
        return

clear()
client = CommandClient("localhost", 5435)

client.send(ClientCommand(NetworkFlag.CONNECTED, data=0))
com = client.recv()
question_amount = com.args["data"]


magic_aahh_loop = 0
while magic_aahh_loop < question_amount:
    client.send(ClientCommand(NetworkFlag.CONNECTED, data=0))
    com = client.recv()
    question = com.args["data"]
    clear()
    list([question['question'],question['choices']])
    choice = input()
    client.send(ClientCommand(NetworkFlag.CONNECTED, data=choice))
    com = client.recv()
    print(com.args["data"])
    time.sleep(4)
    magic_aahh_loop+=1
print("fin")