import os
import json 
import time
import random
from datetime import datetime
import requests
import socket
import html
from cryptography.fernet import Fernet

request_token = ""
offline_questions = ""
catagories = [[],[],[]]
users = []
online = True

a_g_m = [["Mode selection:",["Main","Entertainment","Science"]],["- difficulty selection:",["easy","medium","hard","any"]],["- Type selection:",["multiple","boolean","either"]]]
user_menu = ["New User","Delete User","Change user pin"]
response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]

def api_request(request_string,specify_thingy=''):
    res = requests.get(request_string)
    response = json.loads(res.text)
    try:
        return response[specify_thingy] , response["response_code"]
    except:
        if specify_thingy:
            return response[specify_thingy]
        return response

#Utilitys -Final
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def divider():
    print("\n" + 34 * "-" + "\n")

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        #print(ex)
        return False

def array_untangler(array,item=0):
    temp_array = []
    for x in array:
        temp_array.append(x[item])
    return temp_array 

class SaveFile:
    save_file = "data.json"
    save_data = {}
    def __init__(self, save_file: str = None, auto_load: bool = True) -> None:
        self.save_file = save_file
    def prepare_catagories(self):
        response = api_request('https://opentdb.com/api_category.php',"trivia_categories")
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
    def generate_data_file(self):
        x = {
            "users": [],
            "token": "",
            "catagories" : []
        }
        f = open("data.json", "w")
        f.write(json.dumps(x))
        f.close()
    def one_time_start(self):
        print("Generating Start file")
        self.generate_data_file()
        self.prepare_catagories()
        request_token_temp , response_code = api_request('https://opentdb.com/api_token.php?command=request',"token") 
        if response_code == 0:
            request_token = request_token_temp
        self.save_new([],request_token,catagories)
        self.data_manager()
    def data_manager(self):
        try:
            f = open("data.json", "r")
            thing = json.loads(f.read())
            f.close()
            return [thing["users"] , thing["token"] , thing["catagories"]]
        except:
            self.one_time_start()
            return "o_t_s"
    def save_new(self,users='',token='',catagories=''):
        with open('data.json') as infile:
            data = json.load(infile)
        if users:
            data["users"] = users
        if token:
            data["token"] = token
        if catagories:
            data["catagories"] = catagories

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

class user_manager:    
    def view_user_data(self):
        SAVEOBJECT.save_new(users)
        user_choice = le_input(renderer.option_list(["",users,"Options:",user_menu],1),skip_func=main_menu)
        if user_choice == 0:
            self.new_user()
        elif user_choice == 1:
            self.delete_user()
        elif user_choice == 2:
            self.change_user_pin()
    def new_user(self):
        user = input("user name : ")
        users.append([user , 0, 0, 0, "none", "none" ])
        self.view_user_data()
    def delete_user(self):
        beanz = le_input(renderer.list(["Delete pin",array_untangler(users)]),skip_func=self.view_user_data)
        if beanz >= 0:
            renderer.option_list(["",[users[beanz]],"Confirm deletion of user\n",["delete","cancel"]],mode=1)
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
            self.view_user_data()
        elif beanz == None:
            self.view_user_data()
    def change_user_pin(self):
        clear()
        renderer.list(["Change pin",array_untangler(users)])
        beanz = input("-- ")
        beanz = int(beanz) - 1
        clear()
        print(users[beanz][0])
        wanted_pin = input("-- ")
        users[beanz][5] = wanted_pin
        self.view_user_data()

class renderer:
    def list(items,mode=0,b_t=0):
        if mode == 0:
            clear()
        divider()
        print(html.unescape(items[0]))
        for idx , array_item in enumerate(items[1] , start=1):
            print(html.unescape(str(idx) + " - "+ array_item))
        divider()
        if b_t == 1:
            print(items[2])
        return len(items[1])

    def option_list(items,mode=0):
        clear()
        divider()
        if mode == 0:
            print(html.unescape(items[0]))
            for idx , array_item in enumerate(items[1] , start=1):
                print(html.unescape(str(idx) + " - "+ array_item))
        elif mode == 1:
            users = items[1]
            print("User \t \t Correct \t Incorrect \t W/L Ratio \t Best category \n")
            for beans, value in enumerate(users):
                print(value[0] + " \t \t " + str(value[1]) + " \t \t " + str(value[2]) + " \t \t " + str(value[3]) + " \t \t " + str(value[4]))
        divider()
        print(items[2])
        for idx , array_item in enumerate(items[3] , start=1):
            print(html.unescape(str(idx) + " - "+ array_item))
        divider()
        return len(items[3])

SAVEOBJECT = SaveFile()
USER_MANAGER = user_manager()

def offline_file_manager(counter='',questions=''):
    with open('questions.json') as infile:
        data = json.load(infile)
    if counter >= 0:
        data["counter"] = counter
    if questions:
        data["questions"] = questions
    with open('questions.json', 'w') as outfile:
        json.dump(data, outfile , indent=4)

#Play saved games make a menu that displays them.
def play_save(name):
    f = open("saves/"+name, "r")
    thing = json.loads(f.read())
    f.close()
    main_question_loop(thing["how_many_questions"], thing["questions"],thing["active_users"],thing["current_loop"][0],thing["current_loop"][1])

#Quiz utilitys
def format_display_question(questions):
    temp_array = questions["incorrect_answers"]
    temp_array.append(questions["correct_answer"])
    random.shuffle(temp_array)
    return temp_array , questions["question"] , 
def question_request(amount,change_range=50):
    return random.sample(range(change_range), int(amount))

def generate_save_file(filename,active_users,questions,how_many_questions,current_loop):
    x = {
        "active_users": active_users,
        "questions": questions,
        "current_loop" : current_loop,
        "how_many_questions" : how_many_questions,
        "time" : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_file_directory = './saves/'
    #filename = "save"+str(id)+".json"
    filename = filename + ".json"
    file_path = os.path.join(save_file_directory, filename)
    if not os.path.isdir(save_file_directory):
        os.mkdir(save_file_directory)
    f = open(file_path, "w")
    f.write(json.dumps(x))
    f.close()

#Fix later
def main_question_loop(how_many_questions,questions,active_users,x=0,y=0):
    while x < int(how_many_questions):
        question = questions[x]
        thing1 , thing2 = format_display_question(question)
        while y < len(active_users):
            clear()
            print(active_users[y][0] + " -- Question " + str(x) + " of " + str(how_many_questions))
            renderer.list([thing2,thing1],mode=1)
            user_choice = le_input(len(thing1),skip=False)
            if user_choice == "save":
                clear()
                print("Name for save")
                name = input("-- ")
                generate_save_file(name,active_users,questions,how_many_questions,[x,y])
                main_menu()
                return
            elif user_choice == "menu":
                main_menu()
                return
            elif int(user_choice) == thing1.index(question["correct_answer"]):
                print("\nCorrect")
                active_users[y][1] += 1
            else:
                print("\nIncorrect : " + question["correct_answer"])
                active_users[y][2] += 1
            input("")
            y=y+1
        x=x+1
        y=0
        clear()
        print("User \t Correct \t Incorrect\n")
        for beans, value in enumerate(active_users):
            print(active_users[beans][0] + " \t " + str(active_users[beans][1]) + " \t \t " + str(active_users[beans][2]))
        input("")


    main_menu()
 
def quiz_prepare(quastion_amount,questions,change_range=50):
    current_question = []
    requested_quesions = question_request(quastion_amount,int(change_range))
    for x , y in enumerate(requested_quesions):
        current_question.append(questions[requested_quesions[x]])
    active_users = active_users_select()
    main_question_loop(quastion_amount,current_question,active_users)

#Pretty much finished
def active_users_select():
    active_users = []
    x = le_input(renderer.list(["Users",array_untangler(users),"How many players?"],b_t=1),skip_func=game_menu)
    x+=1
    renderer.list(["Users",array_untangler(users)])
    for y in range(int(x)):
        beanz = le_input(len(array_untangler(users)),skip_func=game_menu)
        active_users.append(users[beanz])
    return active_users

#Custom game setup
def base_custom_input(array,array_name,misc_option=''): 
    renderer.list([array_name,array])
    chosen_item = le_input(len(array),skip_func=game_menu)
    if misc_option == "num":
        return chosen_item
    if misc_option:
        misc_option = misc_option - 1
        nested_catagory = array_untangler(catagories[misc_option],0)
        return nested_catagory[chosen_item]
    return array[chosen_item]

def advanced_game():
    sub_cat = base_custom_input(a_g_m[0][1],a_g_m[0][0],"num")
    temp_cat_select = sub_cat + 1
    request_catagory = str(base_custom_input(array_untangler(catagories[sub_cat],1),"- Catagoey selection:",temp_cat_select))

    #Get limits impliment thing.
    beunos = api_request('https://opentdb.com/api_count.php?category='+request_catagory,"category_question_count")

    temp_array_69 = []
    temp_array_69.append(beunos['total_easy_question_count'])
    temp_array_69.append(beunos['total_medium_question_count'])
    temp_array_69.append(beunos['total_hard_question_count'])
    temp_array_69.append(beunos['total_easy_question_count']+beunos['total_medium_question_count']+beunos['total_hard_question_count'])
    
    request_diffuculty = base_custom_input(a_g_m[1][1],a_g_m[1][0])
    request_type = base_custom_input(a_g_m[2][1],a_g_m[2][0])
    clear()
    divider()

    print("Max "+str(temp_array_69[a_g_m[1][1].index(request_diffuculty)]))
    request_amount = le_input(temp_array_69[a_g_m[1][1].index(request_diffuculty)],skip_func=main_menu)
    request_amount+=1
    token=''
    questions , thing_code = api_request('https://opentdb.com/api.php?amount='+str(request_amount)+'&category='+request_catagory+'&difficulty='+request_diffuculty+'&type='+request_type+token,"results")

    #Temp manuel check response code, make automatic later
    if thing_code != 0:
        print("failed")
        input("return to menu -- ")
        main_menu()
    #
    quiz_prepare(request_amount,questions,request_amount)

#everything down is done ish.
def le_input(range,skip=True,skip_func=""):
    while True:
        try:
            user_input = input("-- ")
            if user_input  == '':
                if skip == True:
                    skip_func()
                    return
                else:
                    print("No skipping")
            elif user_input == 'save':
                return "save"
            elif user_input == 'menu':
                return "menu"
            else:
                user_input = int(user_input)
                if user_input > 0:
                    if user_input <= range:
                        user_input-=1
                        return user_input
                print("num not in range")
        except:
            print("pick number")

def save_menu():
    saves = os.listdir('saves')
    magic_array = ["Saves:",saves,"Options:",["Continue game","Delete game"]]
    user_choice = le_input(renderer.option_list(magic_array),skip_func=main_menu)
    if user_choice == 0:
        play_save(saves[le_input(renderer.list(["Load Save:",saves]),skip_func=save_menu)])
    elif user_choice == 1:
        os.remove("saves/"+saves[le_input(renderer.list(["Delete Save:",saves]),skip_func=save_menu)])
        input("Save deleted")
        main_menu()

def main_menu():
    menu_options[le_input(renderer.list(menu_options["data"]),skip=False)]()

def game_menu():
    user_choice = le_input(renderer.list(game_menu_options["data"]),skip_func=main_menu)
    if user_choice == 3:
        advanced_game()
    else:
        quiz_prepare(game_menu_options["data_2"][user_choice],offline_questions)

game_menu_options = {
    "data":["Game mode:",["Quick","Basic","Advanced","Custom"]],
    "data_2":[5,20,30],
    3:advanced_game
}

online = internet()
if online == False:
    game_menu_options["data"] = ["Game mode:",["Quick","Basic","Advanced"]]

menu_options = {
    "data":["Menu:",["Play","User managment","Continue game"]],
    0:game_menu,
    1:USER_MANAGER.view_user_data,
    2:save_menu
}

#Initialization things -Final
clear()
results = SAVEOBJECT.data_manager()
if results != "o_t_s":
    users = results[0]
    request_token = results[1]
    catagories = results[2]
else:
    time.sleep(1)

offline_file = json.loads(open('questions.json', 'r').read())
"""
online = internet()
if online == True:
    if offline_file["counter"] >= 20:
        offline_questions = api_request('https://opentdb.com/api.php?amount=50')["results"]
        offline_file_manager(0,offline_questions)
    else:
        offline_file["counter"] += 1
        offline_file_manager(offline_file["counter"])
"""
offline_questions = offline_file["questions"]

main_menu()