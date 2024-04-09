import random
import json
import os
import html
import requests
import time

example_data = {
    'date':'12/06/2006',
    'score':0,
    'correct':0,
    'incorrect':0,
    'breakdown':{
        "Q1":{
            "time":1,
            "catagory":"placeholder",
            "result":"correct"
        },
        "Q2":{
            "time":1,
            "catagory":"placeholder",
            "result":"correct"
        }
    }
}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def divider():
    print("\n" + 34 * "-" + "\n")
def array_untangler(array,item=0):
    return [i[item] for i in array] 
def le_input(range=0,skip=True,skip_func="",text_mode=False,specific=None):
    while True:
        try:
            user_input = input("-- ")
            if user_input  == '':
                if skip == True:
                    skip_func()
                    return
                else:
                    print("No skipping")
            elif text_mode == True:
                return user_input
            elif user_input in {"save","menu"}:
                return user_input
            elif text_mode == 'specify':
                if user_input in specific:
                    return user_input
                print("not valid")
            else:
                user_input = int(user_input)
                if user_input > 0:
                    if user_input <= range:
                        user_input-=1
                        return user_input
                print("num not in range")
        except:
            print("pick number")






class Active_user:
    name = None
    score = 0
    correct = 0
    incorrect = 0
    streak = 0
    highest_streak = 0
    questions_missed = 0
    answers = []
    times = []

    def __int__(self, name: str) -> None:
        self.name = name


class Game:

    user_array=[]

    def set_users(self,user_amount,data_list:list=None,names:list=None):
        for x in range(user_amount):  
            user = Active_user()

            if data_list != None:
                data = data_list[x]

                user.name=data.get('name')
                user.score=data.get('score')
                user.correct=data.get('correct')
                user.incorrect=data.get('incorrect')
                user.streak=data.get('streak')
                user.highest_streak=data.get('highest_streak')
                user.questions_missed=data.get('questions_missed')
                user.answers=data.get('answers')
                user.times=data.get('times')
            else:
                user.name=names[x]

            self.user_array.append(user)


    




"""
Main_game = Game()
Main_game.set_users(4)
for x in Main_game.user_array:
    print(x.name)
"""



saved_user_data = [
    {
        'name':'Beilif',
        'score':0,
        'correct':0,
        'incorrect':0,
        'streak':0,
        'highest_streak':0,
        'questions_missed':0,
        'answers':[],
        'times':[]
    }
]


def format_display_question(questions):
    temp_array = questions["incorrect_answers"]
    temp_array.append(questions["correct_answer"])
    random.shuffle(temp_array)
    return temp_array , questions["question"]


save_filepath = "saves/"



Game().set_users(user_amount=1,data_list=saved_user_data)

print(Game().user_array[0].name)

score_multiplier = 100
streak_multiplier = 2


def play_save(name):
    save_data = json.loads(open(save_filepath+name, "r").read())
    main_question_loop(save_data["question_amount"], save_data["questions"],save_data["active_users"],save_data["current_loop"])

def main_question_loop(how_many_questions:int,questions:list,active_users:list,loop_override=None):
    if loop_override != None:
        x = loop_override[0]
        y = loop_override[1]
    clear()
    while x < len(questions):
        current_question = questions[x]
        choices , displayed_question = format_display_question(current_question)
        while y < len(active_users):
            numba = x + 1
            print (Game().user_array[y].name+" -- Question " + str(numba) + " of " + str(how_many_questions))

            


            if Game().user_array[y].streak == 0 and Game().user_array[y].highest_streak == 0:
                print('No streak')
            elif Game().user_array[y].streak == 0:
                print('Previous streak -- ' + str(Game().user_array[y].highest_streak))
            elif Game().user_array[y].highest_streak == 0 :
                print('Current streak -- ' + str(Game().user_array[y].streak))




            
            print(html.unescape(displayed_question) + '\n')
            for d in choices:
                print(html.unescape(d))
            user_choice = le_input(len(choices),skip=False)
            if int(user_choice) == choices.index(current_question["correct_answer"]):
                print("\nCorrect")
                Game().user_array[y].correct+=1
                Game().user_array[y].streak+=1



                Game().user_array[y].score=(Game().user_array[y].score+score_multiplier)+(streak_multiplier*Game().user_array[y].streak)
            else:
                print("\nIncorrect : it was " + current_question["correct_answer"])
                Game().user_array[y].incorrect+=1

                if Game().user_array[y].streak != 0:
                    if Game().user_array[y].streak > Game().user_array[y].highest_streak:
                        Game().user_array[y].highest_streak=Game().user_array[y].streak
                    Game().user_array[y].streak=0


            time.sleep(1)
            y=y+1


        
        clear()
        for person in Game().user_array:


            print ('{0: <20}'.format('Name'),'Score')
            print ('{0: <20}'.format(person.name),person.score)
        time.sleep(2)





        x=x+1
        y=0
        clear()


play_save('2.json')