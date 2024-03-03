import api_com
import misc
import os
import json 
import time
import random
from datetime import datetime

a_g_m = [["Mode selection:",["Main","Entertainment","Science"]],["- difficulty selection:",["easy","medium","hard","any"]],["- Type selection:",["multiple","boolean","either"]]]
request_token = ""
catagories = [[],[],[]]
users = []
offline_questions = ""
test_results=[]

offline = False

active_game = []

user_menu = ["New User","Delete User","Change user pin"]

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

class SaveFile:
    save_file = "data.json"
    save_data = {}
    def __init__(self, save_file: str = None, auto_load: bool = True) -> None:
        self.save_file = save_file
    def prepare_catagories(self):
        response = api_com.get_catagories()
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
        response_code , request_token_temp = api_com.get_token()
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
    def display_all_user_data(self,users):
        misc.clear()
        misc.divider()
        print("User \t \t Correct \t Incorrect \t W/L Ratio \t Best category \n")
        for beans, value in enumerate(users):
            print(users[beans][0] + " \t \t " + str(users[beans][1]) + " \t \t " + str(users[beans][2]) + " \t \t " + str(users[beans][3]) + " \t \t " + str(users[beans][4]))
    def view_user_data(self):
        SAVEOBJECT.save_new(users)
        self.display_all_user_data(users)
        misc.list_formatter(user_menu,"Options:")
        user_choice = input_manager(user_menu)
        if user_choice == 0:
            self.new_user()
        elif user_choice == 1:
            self.delete_user()
        elif user_choice == 2:
            self.change_user_pin()
        elif user_choice == None:
            main_menu() 
    def new_user(self):
        user = input("user name : ")
        users.append([user , 0, 0, 0, "none", "none" ])
        self.view_user_data()
    def delete_user(self):
        misc.clear()
        misc.list_formatter(misc.array_untangler(users),"Delete pin")
        beanz = input_manager(misc.array_untangler(users))
        if beanz >= 0:
            temp_users=[]
            temp_users.append(users[beanz])
            self.display_all_user_data(temp_users)
            misc.divider()
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
            self.view_user_data()
        elif beanz == None:
            self.view_user_data()
    def change_user_pin(self):
        misc.clear()
        misc.list_formatter(misc.array_untangler(users),"Change pin")
        beanz = input("-- ")
        beanz = int(beanz) - 1
        misc.clear()
        print(users[beanz][0])
        wanted_pin = input("-- ")
        users[beanz][5] = wanted_pin
        self.view_user_data()

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


#Make better
def input_manager(item_list,skip_func=1,input_text_override="-- ",any_num=2,max_override=0,bruhz=0):
    chosen_item = None
    while True:
        try:
            number = input(input_text_override)
            if number  == '':
                if skip_func == 1:
                    break
                else:
                    print("\n Required \n")
            elif number:
                number=int(number)
                if number > 0:
                    number -=1 
                    if any_num == 0:
                        chosen_item = (item_list[number])
                        return number
                    if any_num == 1:
                        if number >= max_override:
                            print("\n Number to big, limit "+str(max_override)+"\n")
                        else:
                            if bruhz == 1:
                                number+=1
                            return number
                    if any_num == 2:
                        return number
                else:
                    print("\n Input number above 0.\n")
        except:
            print("\n Enter valid Number corresponding to choices displayed.\n")
    return chosen_item

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

def input_manager2(max_override=0,skip_func=1,input_text_override="-- ",any_num=1,bruhz=0):
    while True:
        try:
            number = input(input_text_override)
            if number  == '':
                if skip_func == 1:
                    break
                else:
                    print("\n Required \n")
            elif number == 'save':
                return "save"
            elif number == 'menu':
                return "menu"
            elif number:
                number=int(number)
                if number > 0:
                    number -=1 
                    if any_num == 1:
                        if number >= max_override:
                            print("\n Number to big, limit "+str(max_override)+"\n")
                        else:
                            if bruhz == 1:
                                number+=1
                            return number
                    if any_num == 2:
                        return number
                else:
                    print("\n Input number above 0.\n")
        except:
            print("\n Enter valid Number corresponding to choices displayed.\n")

#Fix later
def main_question_loop(how_many_questions,questions,active_users,x=0,y=0):
    while x < int(how_many_questions):
        question = questions[x]
        thing1 , thing2 = format_display_question(question)
        while y < len(active_users):
            misc.clear()
            print(active_users[y][0] + " -- Question " + str(x) + " of " + str(how_many_questions))
            misc.list_formatter(thing1,thing2)
            user_choice = input_manager2(4,0)
            if user_choice == "save":
                misc.clear()
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
        misc.clear()
        print("User \t Correct \t Incorrect\n")
        for beans, value in enumerate(active_users):
            print(active_users[beans][0] + " \t " + str(active_users[beans][1]) + " \t \t " + str(active_users[beans][2]))
        input("")


    main_menu()
 
def quiz_prepare(quastion_amount,questions,question_mode,change_range=50):
    current_question = []
    if question_mode == True:
        change_range = 50
        questions = offline_questions

    requested_quesions = question_request(quastion_amount,int(change_range))
    for x , y in enumerate(requested_quesions):
        current_question.append(questions[requested_quesions[x]])

    active_users = active_users_select()
    main_question_loop(quastion_amount,current_question,active_users)

#Pretty much finished
def active_users_select():
    active_users = []
    misc.clear()
    misc.list_formatter(misc.array_untangler(users),"Users")
    print("How many players?")
    x = input_manager(misc.array_untangler(users))
    x+=1
    if x == None:
        game_menu()
    misc.clear()
    misc.list_formatter(misc.array_untangler(users),"Users")
    for y in range(int(x)):
        beanz = input_manager(misc.array_untangler(users))  
        if beanz == None:
            game_menu()
        active_users.append(users[beanz])
    return active_users

#Custom game setup
def base_custom_input(array,array_name,misc_option=''):
    misc.clear() 
    misc.list_formatter(array,array_name)
    chosen_item = input_manager(array)
    if chosen_item == None:
        game_menu()
    if misc_option == "num":
        return chosen_item
    if misc_option:
        misc_option = misc_option - 1
        nested_catagory = misc.array_untangler(catagories[misc_option],0)
        return nested_catagory[chosen_item]
    return array[chosen_item]
def advanced_game():
    misc.clear()
    sub_cat = base_custom_input(a_g_m[0][1],a_g_m[0][0],"num")
    temp_cat_select = sub_cat + 1
    misc.clear()
    request_catagory = base_custom_input(misc.array_untangler(catagories[sub_cat],1),"- Catagoey selection:",temp_cat_select)

    #Get limits impliment thing.
    beunos = api_com.catagory_limit(request_catagory)

    temp_array_69 = []
    temp_array_69.append(beunos['total_easy_question_count'])
    temp_array_69.append(beunos['total_medium_question_count'])
    temp_array_69.append(beunos['total_hard_question_count'])

    temp_array_69.append(beunos['total_easy_question_count']+beunos['total_medium_question_count']+beunos['total_hard_question_count'])
    
    request_diffuculty = base_custom_input(a_g_m[1][1],a_g_m[1][0])
    request_type = base_custom_input(a_g_m[2][1],a_g_m[2][0])
    misc.cd()

    print("Max "+str(temp_array_69[a_g_m[1][1].index(request_diffuculty)]))
    request_amount = input_manager("How many questions:",1,"-- ",1,temp_array_69[a_g_m[1][1].index(request_diffuculty)],bruhz=1)


    thing_code , questions =  api_com.request_questions(request_amount,str(request_catagory),request_diffuculty,request_type)
    #Temp manuel check response code, make automatic later
    if thing_code != 0:
        print("failed")
        input()
        main_menu()
    #
    quiz_prepare(request_amount,questions,offline,request_amount)

def save_menu():
    misc.clear()
    arr = os.listdir('saves')
    misc.list_formatter(arr,"Saves:")
    print("Options:")
    print("1 - Continue game")
    print("2 - Delete game")
    misc.divider()
    user_choice = input_manager(["Continue game","Delete game"])
    if user_choice == 0:
        inpoot = int(input("-- "))
        inpoot-=1
        play_save(arr[inpoot])
    elif user_choice == 1:
        inpoot = int(input("-- "))
        inpoot-=1
        os.remove("saves/"+arr[inpoot])
        input("Save deleted")
        main_menu()
    elif user_choice == None:
        main_menu()

#Could do with an exit button.
def main_menu():
    misc.clear()
    misc.list_formatter(["Play","User managment","Continue game"],"Menu:")
    user_choice = input_manager(["Play","User managment"],0)
    if user_choice == 0:
        game_menu()
    elif user_choice == 1:
        USER_MANAGER.view_user_data()
    elif user_choice == 2:
        save_menu()

#Options not final , menu is.
def game_menu():
    misc.clear()
    misc.list_formatter(["Quick","Basic","Advanced","Custom"],"Game mode:")
    user_choice = input_manager(["Quick","Basic","Advanced","Custom"])
    if user_choice == 0:
        quiz_prepare(5,offline_questions,offline)
    elif user_choice == 1:
        quiz_prepare(10,offline_questions,offline)
    elif user_choice == 2:
        quiz_prepare(20,offline_questions,offline)
    elif user_choice == 3:
        advanced_game()
    elif user_choice == None:
        main_menu()

#Initialization things -Final
misc.clear()
results = SAVEOBJECT.data_manager()
if results != "o_t_s":
    users = results[0]
    request_token = results[1]
    catagories = results[2]
else:
    time.sleep(1)

offline_file = json.loads(open('questions.json', 'r').read())
'''
if offline_file["counter"] >= 20:
    offline_questions = api_com.request_questions(50)[1]
    offline_file_manager(0,offline_questions)
else:
    offline_file["counter"] += 1
    offline_file_manager(offline_file["counter"])
    offline_questions = offline_file["questions"]
'''
offline_questions = offline_file["questions"]

#You need this.
main_menu()