import json
import time
import os
import html
import random

def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def INPOOOOOOOT(range):
    while True:
        try:
            choice = int(input())
            if choice > 0 and choice <= range:
                return choice
            else:
                print("Number in range please")
        except:
            print("No letters")

class Active_user:
    name = None
    correct = 0
    incorrect = 0

class Game:
    user_array=[]


    def add_users(self,data_list:list=None,names:list=None) -> None:

        if data_list:
            user_amount = len(data_list)
        else:
            user_amount = len(names)
        
        for x in range(user_amount):  
            user = Active_user()
            if data_list != None:
                data = data_list[x]
                user.name=data.get('name')
                user.correct=data.get('correct')
                user.incorrect=data.get('incorrect')
            else:
                user.name=names[x]

            self.user_array.append(user)

    def export_users(self) -> None:
        formatted_user_array = []
        for x in self.user_array:
            user_data = {
                "name":x.name,
                "correct":x.correct,
                "incorrect":x.incorrect
            }
            formatted_user_array.append(user_data)
        return formatted_user_array

    def clear_users(self):
        self.user_array.clear()

def read_data_file(name,filetype='.json'):
    return json.loads(open(name+filetype, "r").read())

def question_function(questions,users): 
    for user in users:
        for counter,  question in enumerate(questions , start=1):
            clear()
            print(user. name+'\n')
            print("questions "+str(counter) + ' of ' + str(len(questions))+'\n')
            print(html.unescape(question["question"])+'\n')
            print("Options:")

            choices = [x for x in question["incorrect_answers"]]
            choices.append(question['correct_answer'])
            random.shuffle(choices)

            for id , items in enumerate(choices, start=1):
                print(str(id) + ' ' + items)
            print('\n')
            user_answer = INPOOOOOOOT(len(choices))
            user_answer-=1

            if choices[user_answer] == question['correct_answer']:
                print("Correct!")
                user.correct+=1
            else:
                print("Incorrect. Answer was " + question['correct_answer']) 
                user.incorrect+=1
            time.sleep(1)
        print('result')
        print('name '+user.name)
        print('correct '+str(user.correct))
        print('Incorrect '+str(user.incorrect))
        time.sleep(1)
    clear()
    print("Final score\n")
    for user in users:
        print('name '+user.name)
        print('correct '+str(user.correct))
        print('Incorrect '+str(user.incorrect))
        print('\n')





questions = read_data_file('data/questions')[:5]

chosen_names = ["John","Bob"]

Game().add_users(names=chosen_names)

users = Game().user_array

question_function(questions,users)