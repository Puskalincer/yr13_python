import eel
import json
import random
import html
import time

local_questions = json.loads(open('questions.json', 'r').read())



class storage:
    current_question = []
    current_questions = []
    question_amount = 0
    current_num = 0

def quiz_setup(question_amount: int,questions,change_range=50):
    current_question = []
    requested_quesions = random.sample(range(int(change_range)), question_amount)
    for x , y in enumerate(requested_quesions):
        current_question.append(questions[requested_quesions[x]])
    storage.current_questions=current_question
    storage.question_amount=question_amount

def setup_question(question):
    temp_array2=[]
    current_question = storage.current_questions[question]
    temp_array = current_question["incorrect_answers"]
    temp_array.append(current_question["correct_answer"])
    for x in temp_array:
        temp_array2.append(html.unescape(x))
    storage.current_question = {"question":html.unescape(current_question["question"]),'choices':temp_array2}




quiz_setup(37,local_questions,37)

eel.init('web')
#,storage.current_question['choices']
setup_question(storage.current_num)
eel.question_timed(storage.current_question['question'],storage.current_question['choices'])

@eel.expose
def check_answer(choice):
    eel.hide_button()
    if choice == html.unescape(storage.current_questions[storage.current_num]["correct_answer"]):
        print("yes")
        eel.result("Correct")
    else:
        print("no")
        eel.result("wrong - " + storage.current_questions[storage.current_num]["correct_answer"])
    time.sleep(1)
    storage.current_num+=1
    setup_question(storage.current_num)
    eel.update_page(storage.current_question['question'],storage.current_question['choices'])






eel.start('menu.html')