from py_mp import CommandServer
from py_mp import ServerSideServerCommand
from py_mp.commands import NetworkFlag
import json
import random
import os
import time
import html

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()

class storage:
    current_question = []
    current_questions = []
    question_amount = 0

def quiz_setup(question_amount: int,questions,change_range=50):
    current_question = []
    requested_quesions = random.sample(range(int(change_range)), question_amount)
    for x , y in enumerate(requested_quesions):
        current_question.append(questions[requested_quesions[x]])
    storage.current_questions=current_question
    storage.question_amount=question_amount
    #main_question_loop(quastion_amount,current_question,active_users)

local_questions = json.loads(open('questions.json', 'r').read())

def greeting(name: str) -> str:
    return 'Hello ' + name

quiz_setup(50,local_questions)




port = 7000

def goodstuff():
    while True:
        try:
            server = CommandServer("localhost", port)
            print(port)
            return server
        except:
            print("fail") 
            time.sleep(1)  
            port = print(random.randint(7000,8000))
            



def setup_question(question):
    temp_array2=[]
    current_question = storage.current_questions[question]
    temp_array = current_question["incorrect_answers"]
    temp_array.append(current_question["correct_answer"])
    for x in temp_array:
        temp_array2.append(html.unescape(x))
    storage.current_question = {"question":html.unescape(current_question["question"]),'choices':temp_array2}





def beans():
    print("BEaF")

menu_options = {
    0:beans,
    1:beans
}
#menu_options[com.args['data']]()
#server = goodstuff()





server = CommandServer("localhost", 5435)
server.accept()

com = server.recv(server.clients[0])
server.send(
    ServerSideServerCommand(NetworkFlag.CONNECTED, server.clients[0], data=storage.question_amount), 
    server.clients[0]
)

number = 0
magic_aahh_loop = 0
while magic_aahh_loop < storage.question_amount:
    # Receive a Command from the Client
    com = server.recv(server.clients[0])
    setup_question(number)
    # Send a Test Command back to the Client
    server.send(
        ServerSideServerCommand(NetworkFlag.CONNECTED, server.clients[0], data=storage.current_question), 
        server.clients[0]
    )

    com = server.recv(server.clients[0])
    if storage.current_question['choices'][int(com.args['data'])-1] == storage.current_questions[number]['correct_answer']:
        result = "ye"
    else: 
        result = "na"
    # Send a Test Command back to the Client
    server.send(
        ServerSideServerCommand(NetworkFlag.CONNECTED, server.clients[0], data=result), 
        server.clients[0]
    )






    number+=1
    magic_aahh_loop+=1