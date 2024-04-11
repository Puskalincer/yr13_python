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
import marshal
import pprint

#Make timer affect score and stuff, remake user menu : Done



score_multiplier = 100
streak_multiplier = 2




#Depreciated
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
response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]

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

def array_untangler(array:list,item:int=0) -> list:
    return [i[item] for i in array] 

def spaced_print(things):
    clear()
    print ('{0: <20}'.format('Name'),'highscore\n')
    for thing in things:
        print ('{0: <20}'.format(thing['name']),thing['all_score'])
    print('\n')

def enum_print(array):
    for index , item in enumerate(array,start=1):
        print(str(index) + ' ' + item)
    print('\n')

def view_user_data():
    generate_data_file({"users": users,"token": request_token,"catagories" : catagories,"counter":number},data_file)
    spaced_print(users)
    enum_print(user_menu.get('menu'))
    user_choice = le_input(len(user_menu.get('menu')),skip_func=main_menu)
    user_menu[user_choice]()
def new_user():
    user_name = input("user name : ")
    user_format = {
        "name": user_name,
        "all_score": 0,
        "games":[]
    }
    users.append(user_format)
    view_user_data()
def delete_user():
    beanz = le_input(renderer.list(["Delete pin",array_untangler(users,'name')]),skip_func=view_user_data)
    users.pop(beanz)
    view_user_data()
def advanced_user_view():
    #Through testing i have found that formatting the dictionary is easier to read than pprint
    #pprint.pprint(users,sort_dicts=False)
    print("\n")
    for user in users:
        print("{}: {}".format('name', user['name']))
        print("{}: {}".format('all_score', user['all_score']))
        for thing in user['games']:
            print("\n")
            for key, value in thing.items():
                print("{}: {}".format("\t"+key, value))
        print("\n")
    input('back')
    view_user_data()
user_menu = {
    'menu':["New User","Delete User","Advanced view"],
    0:new_user,
    1:delete_user,
    2:advanced_user_view
}

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
        data = read_data_file(data_file)
        return data
    except:
        one_time_start()
        return "o_t_s"

#Used to format the data for saving games
def generate_save_file(filename,active_users,questions,loop_override):
    x = {
        "u": active_users,
        "q": questions,
        "l" : loop_override,
    }
    generate_data_file(x,save_filepath+filename)

def read_data_file(name,filetype='.json'):
    return json.loads(open(name+filetype, "r").read())

def generate_data_file(info,name):
    file = open(name+".json", "w")
    json.dump(info,file,indent=4)

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



def play_save(name:str) -> None:
    save_data = read_data_file(save_filepath+name,'')
    prepare_quiz(save_data["q"],save_data["u"],loop_override=save_data['l'])



def prepare_quiz(questions:list,user_data:list=None,user_list:list=None,loop_override:list=None) -> None:
    #If you played another game there would be extra users cause i forgot to clear the array. woops.
    Game().clear_users()
    Game().set_users(data_list=user_data,names=user_list)

    #Comparing both systems to add exported objects to user variable user storage, to go in file
    clear()
    exported_users = Game().export_users()

    #print(exported_users[0])    
    #del my_dict['key']
    
    
    existing_users = array_untangler(users,'name')

    print(array_untangler(exported_users,'name'))
    



    #main_question_loop(questions,loop_override)








def format_display_question(questions:list) -> tuple:
    temp_array = [x for x in questions["incorrect_answers"]]
    temp_array.append(questions["correct_answer"])
    random.shuffle(temp_array)
    return temp_array , questions["question"]

def main_question_loop(questions:list,loop_override:list=None) -> None:
    if loop_override != None:
        x = loop_override[0]
        y = loop_override[1]
    else:
        x=0
        y=0
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
            print("\n")
            user_choice = le_input(len(choices),skip=False)
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
                generate_save_file(name,Game().export_users(),questions,[x,y])           
                main_menu()
                return
            elif user_choice == "menu":
                main_menu()
                return
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

    enum_print(['menu','advanced view'])
    user_choice = le_input(2,False)
    if user_choice == 1:
        for user in Game().export_users():
            for key, value in user.items():
                print("{}: {}".format(key, value))
            print("\n")
        input('back to menu')
        main_menu()
    else:
        main_menu()




    #print(Game().export_users())

    #for x in Game().user_array:
    #    pprint.pprint(x.__dict__,sort_dicts=False)
    #    print("\n")







def quiz_prepare(questions:list,quastion_amount:int=None) -> None:
    if quastion_amount != None:
        questions = random.sample(questions, quastion_amount)
    random.shuffle(questions)
    active_users = active_users_select()
    prepare_quiz(questions,user_list=active_users)

def active_users_select() -> list:
    user_names = array_untangler(users,'name')
    active_users = []
    player_amount = le_input(renderer.list(["Users",user_names],sub=1,sub_txt="Player amount"),skip_func=game_menu)
    player_amount+=1
    renderer.list(["Users",user_names])
    for y in range(player_amount):
        beanz = le_input(len(user_names),skip_func=game_menu)
        active_users.append(user_names[beanz])
    return active_users




#Depreciated

def old_main_question_loop(how_many_questions,questions,active_users,x=0,y=0,sub_text="10 secs"):
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
                generate_save_file(name,active_users,questions,[x,y])           
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

def old_quiz_prepare(quastion_amount,questions,change_range=50):
    current_question = []
    requested_quesions = random.sample(range(change_range), int(quastion_amount))
    for x , y in enumerate(requested_quesions):
        current_question.append(questions[requested_quesions[x]])
    active_users = active_users_select()
    old_main_question_loop(quastion_amount,current_question,active_users)

def old_active_users_select():
    active_users = []
    x = le_input(renderer.list(["Users",array_untangler(users,'name')],sub=1,sub_txt="Player amount"),skip_func=game_menu)
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

    if temp_array_69[a_g_m[1][1].index(request_diffuculty)] > 50:
        print("Max 50")
    else:
        print("Max "+str(temp_array_69[a_g_m[1][1].index(request_diffuculty)]))

    request_amount = le_input(temp_array_69[a_g_m[1][1].index(request_diffuculty)],skip_func=main_menu)
    request_amount+=1

    if request_type == 'either':
        request_type=''
    else:
        request_type='&type='+request_type

    if request_diffuculty == 'any':
        request_diffuculty=''
    else:
        request_diffuculty='&difficulty='+request_diffuculty

    questions , thing_code = api_request('https://opentdb.com/api.php?amount='+str(request_amount)+'&category='+request_catagory+request_diffuculty+request_type,"results")

    #Temp manuel check response code, make automatic later
    if thing_code != 0:
        print("failed")
        input("return to menu -- ")
        main_menu()
    #
    #generate_data_file(questions,question_file)
    quiz_prepare(questions)

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
        quiz_prepare(local_questions,g_m_o["data_2"][user_choice])

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
    1:view_user_data,
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


local_questions = read_data_file(question_file)

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

#main_menu()

play_save('new_user_system.json')




"""
#User deletion wasent working so i tested if pop still works and it does so i have to look elswhere.
print(users)

users.pop(0)

print('\n')

print(users)
"""


"""
#New simple user print
print ('{0: <20}'.format('Name'),'highscore\n')
for user in users:
    print ('{0: <20}'.format(user['name']),user['all_score'])
"""



#Testing new user format

#print(users[0]['name'])

#I have streamlines the user system by making it a keyed dictionary 
#It,s now easier to get user information

#for user in users:
#    print(user['name'])





#print(menu(["thing1","thing2","thing3"],"things",back_func=main_menu))
#gets current file path, kinda cool
#print(Path().resolve())