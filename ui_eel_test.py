import eel
import json
import random
import html

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


quiz_setup(50,local_questions)

eel.init('web')



setup_question(storage.current_num)
eel.update_page(storage.current_question['question'],storage.current_question['choices'])

#def check_answer(choice):







eel.start('main.html')

"""

@eel.expose
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')








# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function

eel.start('hello.html')             # Start (this blocks and enters loop

"""