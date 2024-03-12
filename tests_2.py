import os
import json 
import time
from datetime import datetime
import requests
import html

request_token = ""
offline_questions = ""
catagories = []
users = []

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

def array_untangler(array,item=0):
    temp_array = []
    for x in array:
        temp_array.append(x[item])
    return temp_array 


class user_manager:    
    def view_user_data(self):
        #SAVEOBJECT.save_new(users)
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
    generate_data_file({"users": [],"token": request_token,"catagories" : catagories},"test_data")
    data_manager()

def data_manager():
    try:
        file = open("test_data.json", "r")
        thing = json.loads(file.read())
        file.close()
        return [thing["users"] , thing["token"] , thing["catagories"]]
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
    file_path = "saves/"+filename
    generate_data_file(x,file_path)

def generate_data_file(info,name):
    file = open(name+".json", "w")
    json.dump(info,file,indent=4)

#generate_save_file("test",[],[],0,[0,0])










response = api_request('https://opentdb.com/api_category.php',"trivia_categories")
print(response)
for x in response:
    print(x["name"])




def main_menu():
    menu_options[le_input(renderer.list(menu_options["data"]),skip=False)]()

menu_options = {
    "data":["Menu:",["User managment"]],
    0:USER_MANAGER.view_user_data,
}

"""
clear()
results = data_manager()
if results != "o_t_s":
    users = results[0]
    request_token = results[1]
    catagories = results[2]
else:
    time.sleep(1)



offline_file = json.loads(open('questions.json', 'r').read())
offline_questions = offline_file["questions"]
"""

#main_menu()