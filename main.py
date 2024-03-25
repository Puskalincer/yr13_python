import os
import json 
import time
import random
import requests
import socket
import html
from pyboxen import boxen
from timeit import default_timer as timer
from pathlib import Path

#Make timer affect score and stuff, remake user menu

score_time_limit = 10
score_modifier_base = 50
score_modifier_win = 10
score_modifier_lose = 0
score_modifier_time = 5


"""
score_time_limit = 10
score_modifier_base = 73
score_modifier_win = 2
score_modifier_lose = 0
score_modifier_time = 5
"""

request_token = ""
local_questions = ""
catagories = []
users = []
online = True
number = 0

question_file = "questions"
data_file = "data"
save_filepath = "saves/"

a_g_m = [["Mode selection:",["Main","Entertainment","Science"]],["- difficulty selection:",["easy","medium","hard","any"]],["- Type selection:",["multiple","boolean","either"]]]
user_menu = ["New User","Delete User","Change user pin"]
response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]

test_results_format=[["John",{
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

def api_request(request_string,specify_thingy='',mode=0):
    res = requests.get(request_string)
    response = json.loads(res.text)
    if mode == 1:
        return response[specify_thingy]
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

class user_manager:    
    def view_user_data(self):
        generate_data_file({"users": users,"token": request_token,"catagories" : catagories,"counter":number},data_file)
        user_choice = le_input(renderer.option_list(["Users",users,"Options:",user_menu],1),skip_func=main_menu)
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
    def list(items,mode=0,question='',sub=0,sub_txt='',no_num=0):
        title = html.unescape(items[0])
        if mode == 0:
            clear()
        temp_array = []
        if no_num == 0:
            for idx , array_item in enumerate(items[1] , start=1):
                temp_array.append(html.unescape(str(idx) + " - "+ array_item))
        else:
            for array_item in items[1]:
                temp_array.append(array_item)

        b = '\n'.join(temp_array)
        text=html.unescape(question)+b
        if sub == 1:
            l=sub_txt
            sub_align="left"
        else:
            l=title
            sub_align="right"
        print(
            boxen(
                text,
                title=title,
                subtitle=l,
                subtitle_alignment=sub_align,
                color="cyan",
                padding=(1,5),
            )
        )
        return len(items[1])

    def option_list(items):
        clear()
        temp_array = []
        title = items[0]
        for array_item in items[1]:
            temp_array.append(array_item)
        temp_array.append("\n"+items[2])
        for idx , array_item in enumerate(items[3] , start=1):
            temp_array.append(html.unescape(str(idx) + " - "+ array_item))
        text = '\n'.join(temp_array)
        print(
            boxen(
                html.unescape(text),
                title=title,
                subtitle=title,
                subtitle_alignment="right",
                color="cyan",
                padding=(1,5),
            )
        )
        return len(items[3])

    def list_result(items):
        title = items[0]
        clear()
        temp_array = []
        for idx , array_item in enumerate(items[1]):
            temp_array.append(' {left:<7}    {right:>7}'.format(left= array_item, right=str(items[2][idx])))
        text = '\n'.join(temp_array)
        text = ' {left:<7}    {right:>7}'.format(left= "user", right="score\n") + text
        print(
            boxen(
                text,
                title=title,
                subtitle=title,
                subtitle_alignment="right",
                color="cyan",
                padding=(1,5),
            )
        )
        return len(items[1])



    """
    def option_list(items,mode=0):
        clear()
        if mode == 0:
            temp_array = []
            title = html.unescape(items[0])
            for idx , array_item in enumerate(items[1] , start=1):
                temp_array.append(html.unescape(str(idx) + " - "+ array_item))
            text = '\n'.join(temp_array)
            print(
                boxen(
                    html.unescape(text),
                    title=title,
                    subtitle=title,
                    subtitle_alignment="right",
                    color="cyan",
                    padding=(1,5),
                )
            )



        elif mode == 1:
            users = items[1]
            temp_array = []
            title = html.unescape(items[0])



            
            question = "User \t \t Correct \t Incorrect \t W/L Ratio \t Best category \n"
            for beans, value in enumerate(users):
                temp_array.append(value[0] + " \t  " + str(value[1]) + " \t  " + str(value[2]) + " \t  " + str(value[3]) + " \t  " + str(value[4]))
        

                
            text = '\n'.join(temp_array)

            text=question+text

            print(
                boxen(
                    html.unescape(text),
                    title=title,
                    subtitle=title,
                    subtitle_alignment="right",
                    color="cyan",
                    padding=(1,5),
                )
            )






            
        
        divider()
        print(items[2])
        for idx , array_item in enumerate(items[3] , start=1):
            print(html.unescape(str(idx) + " - "+ array_item))
        divider()
        return len(items[3])
    """

USER_MANAGER = user_manager()

def prepare_catagories():
    temp_array = [[],[],[]]
    response = api_request('https://opentdb.com/api_category.php',"trivia_categories")
    for x in response:
        first_word = x["name"].split()[0]
        if first_word == "Entertainment:" or first_word == "Science:":
            pass
        else:
            temp_array[0].append([ x["id"],x["name"]])
    for x in response:
        first_word = x["name"].split()[0]
        if first_word == "Entertainment:":
            temp_array[1].append([x["id"],x["name"]])
    for x in response:
        first_word = x["name"].split()[0]
        if first_word == "Science:":
            temp_array[2].append([x["id"],x["name"]])
    return temp_array

def one_time_start():
    print("Generating Start file")
    catagories = prepare_catagories()
    request_token = api_request('https://opentdb.com/api_token.php?command=request',"token",1) 
    generate_data_file(api_request('https://opentdb.com/api.php?amount=50')["results"],question_file)
    generate_data_file({"users": [],"token": request_token,"catagories" : catagories,"counter":0},data_file)
    data_manager()

def data_manager():
    try:
        data = json.loads(open(data_file+".json", "r").read())
        return data
    except:
        one_time_start()
        return "o_t_s"

def generate_save_file(filename,active_users,questions,question_amount,current_loop):
    x = {
        "active_users": active_users,
        "questions": questions,
        "current_loop" : current_loop,
        "question_amount" : question_amount
    }
    file_path = save_filepath+filename
    generate_data_file(x,file_path)

def generate_data_file(info,name):
    file = open(name+".json", "w")
    json.dump(info,file,indent=4)

#Play saved games make a menu that displays them.
def play_save(name):
    save_data = json.loads(open(save_filepath+name, "r").read())
    main_question_loop(save_data["question_amount"], save_data["questions"],save_data["active_users"],save_data["current_loop"][0],save_data["current_loop"][1])

#Quiz utilitys
def format_display_question(questions):
    temp_array = questions["incorrect_answers"]
    temp_array.append(questions["correct_answer"])
    random.shuffle(temp_array)
    return temp_array , questions["question"]

def main_question_loop(how_many_questions,questions,active_users,x=0,y=0,sub_text="10 secs"):
    current_score = []
    for users in active_users:
        current_score.append(0)
    while x < int(how_many_questions):
        question = questions[x]
        thing1 , thing2 = format_display_question(question)
        while y < len(active_users):
            renderer.list([active_users[y][0] + " -- Question " + str(x) + " of " + str(how_many_questions),thing1],question=thing2+"\n",sub=1,sub_txt=sub_text)
            start = timer()
            user_choice = le_input(len(thing1),skip=False)
            end = timer()
            if user_choice == "save":
                saves = os.listdir('saves')
                if len(saves) == 0:
                    saves = ["No saves"]
                name = menu(saves,"Saves",sub_txt="Save name",no_index=1,text_mode=True,back_func=main_menu)
                for save_item in saves:
                    save = Path(save_item).stem
                    if save == name:
                        print("Overwrite save? y/n")
                        user_choice = le_input(text_mode='specify',specific={"y","n"})
                        if user_choice == "n":
                            main_menu()
                            return
                generate_save_file(name,active_users,questions,how_many_questions,[x,y])           
                main_menu()
                return
            elif user_choice == "menu":
                main_menu()
                return
            elif int(user_choice) == thing1.index(question["correct_answer"]):
                print("\nCorrect")
                final_time = int(end - start)
                if final_time < 10:
                    le_numbers = score_modifier_base-(final_time*score_modifier_time)
                    current_score[y] = current_score[y] + le_numbers
            else:
                print("\nIncorrect : " + question["correct_answer"])
            #print(final_time) 
            #print(final_time*score_modifier_time)
            #print(score_modifier_base-(final_time*score_modifier_time))
            input("")
            y=y+1
        x=x+1
        y=0
        clear()
        renderer.list_result(["scores",array_untangler(active_users,0),current_score])
        input("")
    main_menu()

def quiz_prepare(quastion_amount,questions,change_range=50):
    current_question = []
    requested_quesions = random.sample(range(change_range), int(quastion_amount))
    for x , y in enumerate(requested_quesions):
        current_question.append(questions[requested_quesions[x]])
    active_users = active_users_select()
    main_question_loop(quastion_amount,current_question,active_users)

#Pretty much finished
def active_users_select():
    active_users = []
    x = le_input(renderer.list(["Users",array_untangler(users)],sub=1,sub_txt="Player amount"),skip_func=game_menu)
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
    if online == False:
        input("Internet required")
        game_menu()
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




    if request_type == 'either':
        request_type=''
    else:
        request_type='&type='+request_type



    questions , thing_code = api_request('https://opentdb.com/api.php?amount='+str(request_amount)+'&category='+request_catagory+'&difficulty='+request_diffuculty+request_type+token,"results")

    #Temp manuel check response code, make automatic later
    if thing_code != 0:
        print("failed")
        input("return to menu -- ")
        main_menu()
    #
    #generate_data_file(questions,question_file)
    quiz_prepare(request_amount,questions,request_amount)

#everything down is done ish.
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

def save_menu():
    saves = os.listdir('saves')
    if len(saves) == 0:
        menu(["No Saves"],"Saves",main_menu,no_index=1,text_mode=True)
        main_menu()
    magic_array = ["Saves",saves,"\nOptions:",["Continue game","Delete game"]]
    user_choice = le_input(renderer.option_list(magic_array),skip_func=main_menu)
    if user_choice == 0:
        user_choice = le_input(renderer.list(["Load Save",saves]),skip_func=save_menu)
        play_save(saves[user_choice])
    elif user_choice == 1:
        os.remove("saves/"+saves[le_input(renderer.list(["Delete Save",saves]),skip_func=save_menu)])
        input("Save deleted")
        main_menu()

def main_menu():
    menu_options[menu(menu_options["items"],menu_options["title"])]()

setting_items = ["Gui mode = console","score_time_limit = " + str(score_time_limit),"score_modifier_base = " + str(score_modifier_base),"score_modifier_win = "+str(score_modifier_win),"score_modifier_lose = "+str(score_modifier_lose),"score_modifier_time = "+str(score_modifier_time),"request_token = "+request_token,"online = "+str(online),"question_file_name = "+question_file,"data_file_name = "+data_file,"save_filepath_name = "+save_filepath]

def setting_menu():
    menu(setting_items,"Settings",main_menu)

def game_menu():
    user_choice = menu(g_m_o["items"],g_m_o["title"],main_menu)
    if user_choice == 3:
        advanced_game()
    else:
        quiz_prepare(g_m_o["data_2"][user_choice],local_questions)

g_m_o = {
    "items":["Quick","Basic","Advanced","Custom"],
    "title":"Game menu",
    "data_2":[5,20,30],
    3:advanced_game
}

menu_options = {
    "items":["Play","User managment","Continue game","settings"],
    "title":"Menu",
    0:game_menu,
    1:USER_MANAGER.view_user_data,
    2:save_menu,
    3:setting_menu
}

online = internet()
#Initialization things -Final
clear()
results = data_manager()
if results != "o_t_s":
    users = results["users"]
    request_token = results["token"]
    catagories = results["catagories"]
    if results["counter"]>20:
        questions = api_request('https://opentdb.com/api.php?amount=50')["results"]
        generate_data_file(questions,question_file)
        number = 0
    else:
        #number = results["counter"]+1
        pass
    generate_data_file({"users": users,"token": request_token,"catagories" : catagories,"counter":number},data_file)
else:
    time.sleep(1)
local_questions = json.loads(open(question_file+'.json', 'r').read())

if not os.path.exists(Path(save_filepath)):
    Path(save_filepath).mkdir(parents=True, exist_ok=True)

def menu(menu_items,title,back_func=None,sub_txt=None,no_index=0,text_mode=False):
    clear()
    if back_func == None:
        skip=False
    else:
        skip=True
    if sub_txt == None:
        sub=0
    else:
        sub=1
    return le_input(renderer.list([title,menu_items],sub=sub,sub_txt=sub_txt,no_num=no_index),skip=skip,skip_func=back_func,text_mode=text_mode)

main_menu()

#print(menu(["thing1","thing2","thing3"],"things",back_func=main_menu))
#gets current file path, kinda cool
#print(Path().resolve())