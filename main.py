import requests
import json 
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import os
import html

"""
LOOK AT THIS LATERRR

import SimpleHTTPServer
import SocketServer

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/your_file.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)

server.serve_forever()
"""



"""
TOO DO LIST

Add error checking to everything.

Add automatic checking for advanced game choice validity

Make game remember the stuff

"""


#https://opentdb.com/api_count.php?category=9

response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]
a_g_m = [["Mode selection:",["Main","Entertainment","Science"]],["- difficulty selection:",["easy","medium","hard","any"]],["- Type selection:",["multiple","boolean","either"]]]
request_token = ""
catagories = [[],[],[]]
users = []
active_users = []
questions = ""
test_results=[]

user_menu = ["New User","Delete User","Change user pin"]



test_results_mabye=[["John",{
    "Q1":{
        "time":1,
        "catagory":"placeholder",
        "answered":"correct"
    },
    "Q2":{
        "time":1,
        "catagory":"placeholder",
        "answered":"correct"
    }
                       
}],["John"]]

#Runs on first start, never used again. -Final
def prepare_catagories():
    res = requests.get('https://opentdb.com/api_category.php')
    response = json.loads(res.text)
    response = response["trivia_categories"]
    for x in response:
        first_word = x["name"].split()[0]
        if first_word == "Entertainment:" or first_word == "Science:":
            pass
        else:
            catagories[0].append([ x["id"],x["name"]])
    for x in response:
        first_word = x["name"].split()[0]
        if first_word == "Entertainment:":
            catagories[1].append([x["id"],x["name"]])
    for x in response:
        first_word = x["name"].split()[0]
        if first_word == "Science:":
            catagories[2].append([x["id"],x["name"]])
#Runs on first start, never used again. -Final
def generate_data_file():
    x = {
        "users": [],
        "token": "",
        "catagories" : []
    }
    f = open("data.json", "w")
    f.write(json.dumps(x))
    f.close()
#Runs on first start, never used again. -Final
def one_time_start():
    print("Generating Start file")
    generate_data_file()
    prepare_catagories()
    response_code , request_token_temp = get_token()
    if response_code == 0:
        request_token = request_token_temp
    save_new([],request_token,catagories)
    data_manager()
#Runs on first start, never used again. -Final
def get_token():
    res = requests.get('https://opentdb.com/api_token.php?command=request')
    response = json.loads(res.text)
    return response["response_code"] , response["token"]
#Always runs at on startup -Final
def data_manager():
    try:
        f = open("data.json", "r")
        thing = json.loads(f.read())
        f.close()
        return [thing["users"] , thing["token"] , thing["catagories"]]
    except:
        one_time_start()
        return "o_t_s"
#Save data -Final
def save_new(users='',token='',catagories=''):
    with open('data.json') as infile:
        data = json.load(infile)
    if users:
        data["users"] = users
    if token:
        data["token"] = token
    if catagories:
        data["catagories"] = catagories

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

#Utilitys -Final
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def divider():
    print("\n" + 34 * "-" + "\n")
def cd():
    clear()
    divider()

#Not done?
def input_manager1(item_list,skip_func=1):
    chosen_item = None
    while True:
        try:
            number = input("-- ")
            if number  == '' and skip_func == 1:
                break
            elif number  == '' and skip_func == 0:
                print("\n Required \n")
            elif number:
                number=int(number)
                if number > 0:
                    number -=1 
                    chosen_item = (item_list[number])
                    return number
                    break
                else:
                    print("\n Input number above 0.\n")
        except:
            print("\n Enter valid Number corresponding to choices displayed.\n")
    return chosen_item




#Makes multilevel arrays useful -Final
def array_untangler(array,item=0):
    temp_array = []
    for x in array:
        temp_array.append(x[item])
    return temp_array 

#Prolly dont need
def reset_token(token):
    res = requests.get('https://opentdb.com/api_token.php?command=reset&token='+token)
    response = json.loads(res.text)
    return response_codes[response["response_code"]]

def request_questions(amount,catagory='',difficulty='',type='',token=''):
    if catagory:
        catagory = '&category=' + catagory
    if difficulty:
        if difficulty != "any":
            difficulty = '&difficulty=' + difficulty
        else:
            difficulty=''
    if type:
        if type != "either":
            type = '&type=' + type
        else:
            type=''
    if token:
        token = '&token='+ token
    res = requests.get('https://opentdb.com/api.php?amount=' + str(amount) + str(catagory) + difficulty + type + token)
    response = json.loads(res.text)
    return response["response_code"] , response["results"] 

# Join both 
def list_formatter(arrayname,array_name_formatted):
    divider()
    print(array_name_formatted)
    for idx , array_item in enumerate(arrayname , start=1):
        print(str(idx) + " - "+ array_item[0])
    divider()

def list_formatter2(arrayname,array_name_formatted,instructions=""):
    if instructions:
        divider()
        print(instructions)
    divider()
    print(array_name_formatted)
    for idx , array_item in enumerate(arrayname , start=1):
        print(str(idx) + " - "+ array_item)
    divider()

#Main quizz stuff
def format_display_question(questions):
    temp_array = questions["incorrect_answers"]
    temp_array.append(questions["correct_answer"])
    random.shuffle(temp_array)
    return temp_array , questions["question"] , 

def question_request(amount,change_range=50):
    return random.sample(range(change_range), int(amount))

def main_question_loop(how_many_questions,questions,change_range):
    requested_quesions = question_request(how_many_questions,int(change_range))
    x=0
    while x < int(how_many_questions):
        question = questions[requested_quesions[x]]
        thing1 , thing2 = format_display_question(question)
        x=x+1
        y=0
        while y < len(active_users):
            clear()
            print(active_users[y][0] + " -- Question " + str(x) + " of " + str(how_many_questions))
            list_formatter2(html.unescape(thing1),html.unescape(thing2))
            user_choice = input()
            if int(user_choice) == thing1.index(question["correct_answer"])+1:
                print("\nCorrect")
                active_users[y][1] += 1
            else:
                print("\nIncorrect : " + question["correct_answer"])
                active_users[y][2] += 1
            input("")
            y=y+1
        clear()
        print("User \t Correct \t Incorrect\n")
        for beans, value in enumerate(active_users):
            print(active_users[beans][0] + " \t " + str(active_users[beans][1]) + " \t \t " + str(active_users[beans][2]))
        input("")

#User stuff
def view_user_data():
    save_new(users)
    clear()
    divider()
    print("User \t \t Correct \t Incorrect \t W/L Ratio \t Best category \n")
    for beans, value in enumerate(users):
        print(users[beans][0] + " \t \t " + str(users[beans][1]) + " \t \t " + str(users[beans][2]) + " \t \t " + str(users[beans][3]) + " \t \t " + str(users[beans][4]))
    list_formatter2(user_menu,"Options:")
    user_choice = input_manager1(user_menu)
    if user_choice == 0:
        new_user()
    elif user_choice == 1:
        delete_user()
    elif user_choice == 2:
        change_user_pin()
    elif user_choice == None:
        main_menu()

def new_user():
    #len(users)
    user = input("user name : ")
    users.append([user , 0, 0, 0, "none", "none" ])
    view_user_data()

def delete_user():
    clear()
    list_formatter(users,"Delete user")
    beanz = input("-- ")
    beanz = int(beanz) - 1
    clear()
    divider()
    print("User \t \t Correct \t Incorrect \t W/L Ratio \t Best category \n")
    print(users[beanz][0] + " \t \t " + str(users[beanz][1]) + " \t \t " + str(users[beanz][2]) + " \t \t " + str(users[beanz][3]) + " \t \t " + str(users[beanz][4]))
    divider()
    print("Confirm deletion of user y/n\n")
    deletion = input("-- ")
    if deletion == "y":
        if users[beanz][5] != "none":
            while True:
                secure = input("Enter pin : ")
                if secure == users[beanz][5]:
                    users.pop(int(beanz))
                    break
                elif secure == '':
                    break
                else:
                    print("Pin wrong")
        else:
            users.pop(int(beanz))
    view_user_data()
def change_user_pin():
    clear()
    list_formatter(users,"Change pin")
    beanz = input("-- ")
    beanz = int(beanz) - 1
    clear()
    print(users[beanz][0])
    wanted_pin = input("-- ")
    users[beanz][5] = wanted_pin
    view_user_data()
def active_users_select():
    clear()
    list_formatter(users,"Users")
    print("How many players?")
    x = input("Num : ")
    clear()
    list_formatter(users,"Users")
    for y in range(int(x)):
        beanz = input("Num : ")  
        beanz = int(beanz) - 1
        active_users.append(users[beanz])

#Does stuff? prolly wont need
def question_reroll():
    thing_code , questions =  request_questions(50)
    open('questions.json', 'w').write(json.dumps(questions , ensure_ascii=False, indent=4 ))

#Custom game setup
def base_custom_input(array,array_name,misc=''):
    clear() 
    list_formatter2(array,array_name)
    chosen_item = int(input())
    chosen_item = chosen_item - 1
    if misc == "num":
        return chosen_item
    if misc:
        misc = misc - 1
        nested_catagory = array_untangler(catagories[misc],0)
        return nested_catagory[chosen_item]
    return array[chosen_item]
def advanced_game():
    clear()
    sub_cat = base_custom_input(a_g_m[0][1],a_g_m[0][0],"num")
    #print(main_catagory)
    #input()
    temp_cat_select = sub_cat + 1
    clear()
    request_catagory = base_custom_input(array_untangler(catagories[sub_cat],1),"- Catagoey selection:",temp_cat_select)
    request_diffuculty = base_custom_input(a_g_m[1][1],a_g_m[1][0])
    request_type = base_custom_input(a_g_m[2][1],a_g_m[2][0])
    cd()
    request_amount = input("How many questions:")
    thing_code , questions =  request_questions(request_amount,str(request_catagory),request_diffuculty,request_type)
    #Temp manuel check response code, make automatic later
    print( response_codes[thing_code])
    input()
    #
    MAIN_QUIZ(request_amount,questions,request_amount)

def main_menu():
    clear()
    list_formatter2(["Play","User managment"],"Menu:")
    user_choice = input_manager1(["Play","User managment"],0)
    if user_choice == 0:
        game_menu()
    elif user_choice == 1:
        view_user_data()

def game_menu():
    clear()
    list_formatter2(["Quick","Basic","Advanced","Custom"],"Game mode:")
    user_choice = input_manager1(["Quick","Basic","Advanced","Custom"])
    if user_choice == 0:
        MAIN_QUIZ(5,questions)
    elif user_choice == 1:
        MAIN_QUIZ(10,questions)
    elif user_choice == 2:
        MAIN_QUIZ(20,questions)
    elif user_choice == 3:
        advanced_game()
    elif user_choice == None:
        main_menu()

def MAIN_QUIZ(quastion_amount,questions,change_range=50):
    active_users_select()
    main_question_loop(quastion_amount,questions,change_range)

#Initialization things -Final
clear()
results = data_manager()
if results != "o_t_s":
    users = results[0]
    request_token = results[1]
    catagories = results[2]

questions = json.loads(open('questions.json', 'r').read())


main_menu()



"""
#Timer
start = time.time()
#stuff
end = time.time()
length = start - end
print("It took", length, "seconds!")



#Wrong
class User_tracker:
    def __init__(self, User_name):
        self.User_name = User_name

    def __str__(self):
        return f"{self.User_name}{self.age}"

    def myfunc(self):
        print("Hello my name is " + self.User_name)

p1 = User_tracker("Bob")
p1.myfunc()

"""

def main_question_loop_test(how_many_questions,questions,change_range=50):
    requested_quesions = question_request(how_many_questions,int(change_range))
    current_question=0



    for x in active_users:
        test_results.append([x[0]]) 
    print(test_results)
    input()

    while current_question < int(how_many_questions):
        question = questions[requested_quesions[current_question]]
        thing1 , thing2 = format_display_question(question)
        current_question=current_question+1
        y=0


        print(question["catagory"])
        input()


        while y < len(active_users):
            clear()
            print(active_users[y][0] + " -- Question " + str(current_question) + " of " + str(how_many_questions))
            list_formatter2(html.unescape(thing1),html.unescape(thing2))
            user_choice = input()
            if int(user_choice) == thing1.index(question["correct_answer"])+1:
                print("\nCorrect")
                active_users[y][1] += 1
            else:
                print("\nIncorrect : " + question["correct_answer"])
                active_users[y][2] += 1
            input("")
            y=y+1
        clear()
        print("User \t Correct \t Incorrect\n")
        for beans, value in enumerate(active_users):
            print(active_users[beans][0] + " \t " + str(active_users[beans][1]) + " \t \t " + str(active_users[beans][2]))
        input("")

#active_users_select()
#main_question_loop_test(2,questions)

#print(test_results_mabye[0][1]["Q1"])