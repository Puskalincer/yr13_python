import random
import json
import os
import html
import time
import pprint

save_filepath = "saves/"

score_multiplier = 100
streak_multiplier = 2




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
    answers = []

    def __int__(self, name: str) -> None:
        self.name = name

class Game:

    user_array=[]

    def set_users(self,data_list:list=None,names:list=None):

        if data_list:
            user_amount = len(data_list)
        else:
            user_amount = len(names)
        
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
                user.answers=data.get('answers')
            else:
                user.name=names[x]

            self.user_array.append(user)

    def export_users(self):
        formatted_user_array = []
        for x in self.user_array:
            user_data = {
                "name":x.name,
                "score":x.score,
                "correct":x.correct,
                "incorrect":x.incorrect,
                "streak":x.streak,
                "highest_streak":x.highest_streak,
                "answers":x.answers,
            }

            formatted_user_array.append(user_data)

        return formatted_user_array
    
    def clear_users(self):
        self.user_array = []

def format_display_question(questions:list) -> tuple:
    temp_array = questions["incorrect_answers"]
    temp_array.append(questions["correct_answer"])
    random.shuffle(temp_array)
    return temp_array , questions["question"]

def play_save(name:str) -> None:
    save_data = json.loads(open(save_filepath+name, "r").read())
    prepare_quiz(save_data["q"],save_data["u"],loop_override=save_data['l'])

def prepare_quiz(questions:list,user_data:list=None,user_list:list=None,loop_override:list=None) -> None:
    Game().set_users(data_list=user_data,names=user_list)
    main_question_loop(questions,loop_override)

def main_question_loop(questions:list,loop_override:list=None) -> None:
    if loop_override != None:
        x = loop_override[0]
        y = loop_override[1]
    while x < len(questions):
        current_question = questions[x]
        choices , displayed_question = format_display_question(current_question)
        while y < len(Game().user_array):
            numba = x + 1

            if Game().user_array[y].streak == 0 and Game().user_array[y].highest_streak == 0:
                current_streak='No streak'
            elif Game().user_array[y].streak == 0:
                current_streak='Previous best streak -- ' + str(Game().user_array[y].highest_streak)
            else:
                current_streak='Current streak -- ' + str(Game().user_array[y].streak)
            clear()
            print ('{0: <30}'.format(Game().user_array[y].name+" -- Question " + str(numba) + " of " + str(len(questions))),current_streak+'\n')
            print(html.unescape(displayed_question) + '\n')
            for n , d in enumerate(choices , start=1):
                print(str(n) + ' ' + html.unescape(d))
            user_choice = le_input(len(choices),skip=False)
            Game().user_array[y].answers.append(choices[user_choice])
            if int(user_choice) == choices.index(current_question["correct_answer"]):
                print("\nCorrect")
                Game().user_array[y].correct+=1
                Game().user_array[y].streak+=1
                Game().user_array[y].score=(Game().user_array[y].score+score_multiplier)+(streak_multiplier*Game().user_array[y].streak)
            else:
                print("\nIncorrect : it was - " + current_question["correct_answer"])
                Game().user_array[y].incorrect+=1
                if Game().user_array[y].streak != 0:
                    if Game().user_array[y].streak > Game().user_array[y].highest_streak:
                        Game().user_array[y].highest_streak=Game().user_array[y].streak
                    Game().user_array[y].streak=0
            time.sleep(1)
            y=y+1
        clear()
        print ('{0: <20}'.format('Name'),'Score')
        for person in Game().user_array:
            print ('{0: <20}'.format(person.name),person.score)
        time.sleep(2)
        x=x+1
        y=0
        clear()
    print('Final scores\n')
    print ('{0: <20}'.format('Name'),'Score')
    for person in Game().user_array:
        print ('{0: <20}'.format(person.name),person.score)
    print("\n")
    input("back to menu")

    #print(Game().export_users())

    #for x in Game().user_array:
    #    pprint.pprint(x.__dict__,sort_dicts=False)
    #    print("\n")





play_save('new_user_system.json')