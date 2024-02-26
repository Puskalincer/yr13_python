import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

"""
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(
        len(data), address))
    print(data)

    if data:
        sent = sock.sendto(bytes("0", 'utf-8'), address)
        print('sent {} bytes back to {}'.format(sent, address))
"""


def send_data(message):
    print(message)
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(
        len(data), address))
    print(data)

    if data:
        sent = sock.sendto(str(message).encode('ascii'), address)
        print('sent {} bytes back to {}'.format(sent, address))


import json 
import random

def format_display_question(questions):
    temp_array = questions["incorrect_answers"]
    temp_array.append(questions["correct_answer"])
    random.shuffle(temp_array)
    return temp_array , questions["question"] , 
def question_request(amount,change_range=50):
    return random.sample(range(change_range), int(amount))

def quiz_prepare(quastion_amount,change_range=50):
    current_question = []
    requested_quesions = question_request(quastion_amount,int(change_range))
    for x , y in enumerate(requested_quesions):
        current_question.append(offline_questions[requested_quesions[x]])
    return  current_question

offline_questions = json.loads(open('questions.json', 'r').read())["questions"]
 
def main_quiz(how_many_questions,questions):
    x=0
    while x < int(how_many_questions):
        question = questions[x]
        thing1 , thing2 = format_display_question(question)
        x=x+1
        temp_array=[]
        temp_array.append(thing2)
        temp_array.append(thing1)
        print(temp_array)

        send_data(temp_array)

        input()
        """

        thingymabob=0

        if int(thingymabob) == thing1.index(question["correct_answer"]):
            print("\nCorrect")
        else:
            print("\nIncorrect : " + question["correct_answer"])
        """



main_quiz(5,quiz_prepare(5))




