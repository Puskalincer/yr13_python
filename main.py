import requests
import json 
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import os

hostName = "localhost"
serverPort = 8080

response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]

difficulty = ["easy","medium","hard"]
types = ["multiple","boolean","either"]

request_token = ""

catagories = [[],[],[]]

users = []
active_users = []

questions = ""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def array_untangler(array,item=0):
    temp_array = []
    for x in array:
        temp_array.append(x[item])
    return temp_array 

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
    save_data()

def webserver():
    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

    if __name__ == "__main__":        
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")

def reset_token(token):
    res = requests.get('https://opentdb.com/api_token.php?command=reset&token='+token)
    response = json.loads(res.text)
    return response_codes[response["response_code"]]
def get_token():
    res = requests.get('https://opentdb.com/api_token.php?command=request')
    response = json.loads(res.text)
    if response["response_code"] == 0:
        print(response["token"]) 
        print(response_codes[response["response_code"]])
        return response["token"]
    else:
        print(response_codes[response["response_code"]])

def data_manager():
    try:
        f = open("data.json", "r")
        thing = json.loads(f.read())
        f.close()
        return thing["token"] , thing["users"] , thing["catagories"]
    except:
        prepare_catagories()
        return get_token() , [] , []
def save_data():
    x = {
        "users": users,
        "token": request_token,
        "catagories" : catagories
    }
    f = open("data.json", "w")
    f.write(json.dumps(x))
    f.close()


#Old one
#def request_questions(amount,token='',catagory='',difficulty='',type=''):
#Fixed
def request_questions(amount,catagory='',difficulty='',type='',token=''):
    if catagory:
        catagory = '&category=' + catagory
    if difficulty:
        difficulty = '&difficulty=' + difficulty
    if type:
        if type != "either":
            type = '&type=' + type
        else:
            type=''
    if token:
        token = '&token='+ token
    res = requests.get('https://opentdb.com/api.php?amount=' + str(amount) + str(catagory) + difficulty + type + token)

    #Adding this debug line i found that if i didnt include a token it would be the parsed data meant for the catagory as the token was second not last.
    print('https://opentdb.com/api.php?amount=' + str(amount) + str(catagory) + difficulty + type + token)

    response = json.loads(res.text)
    return response["response_code"] , response["results"] 

def divider():
    print("\n" + 34 * "-" + "\n")
def list_formatter(arrayname,array_name_formatted,instructions=""):
    if instructions:
        divider()
        print(instructions)
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
    return temp_array , questions["question"]

def question_request(amount,change_range=50):
    return random.sample(range(change_range), int(amount))

def main_question_loop(how_many_questions,questions):
    requested_quesions = question_request(how_many_questions)
    x=0
    while x < int(how_many_questions):
        question = questions[requested_quesions[x]]
        thing1 , thing2 = format_display_question(question)
        x=x+1
        y=0
        while y < len(active_users):
            clear()
            print(active_users[y][0] + " -- Question " + str(x))
            list_formatter2(thing1,thing2)
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
    save_data()
    clear()
    divider()
    print("User \t \t Correct \t Incorrect \t W/L Ratio \t Best category \n")
    for beans, value in enumerate(users):
        print(users[beans][0] + " \t \t " + str(users[beans][1]) + " \t \t " + str(users[beans][2]) + " \t \t " + str(users[beans][3]) + " \t \t " + str(users[beans][4]))
    list_formatter2(["New User","Delete User","Change user pin"],"Options:")
    user_choice = input("-- ")
    if user_choice == "1":
        new_user()
    elif user_choice == "2":
        delete_user()
    elif user_choice == "3":
        change_user_pin()
    elif user_choice == '':
        main_menu()
def new_user():
    len(users)
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

def question_reroll():
    thing_code , questions =  request_questions(50,request_token,catagory=0)
    open('1questions.json', 'w').write(json.dumps(questions , ensure_ascii=False, indent=4 ))

def catagory_other_thing(that_one):
    inpurt = input()
    inpurt =- 1
    aids = array_untangler(catagories[that_one],0)
    return aids[int(inpurt)]

def diffuculty_other_thing():
    clear()
    list_formatter2(["easy","medium","hard"],"- difficulty selection:")
    inpurt = input()
    inpurt = int(inpurt) - 1
    return difficulty[inpurt]

def type_other_thing():
    clear()
    list_formatter2(["multiple","boolean","either"],"- Type selection:")
    inpurt = input()
    inpurt = int(inpurt) - 1
    return types[inpurt]

def advanced_game():
    clear()
    list_formatter2(["Main","Entertainment","Science"],"Mode selection:")
    inpoot = input()
    if inpoot == "1":
        clear()
        list_formatter2(array_untangler(catagories[0],1),"- Mode selection:")
        request_catagory = catagory_other_thing(0)
        request_diffuculty = diffuculty_other_thing()
        request_type = type_other_thing()
        clear()
        divider()
        request_amount = input("How many questions:")

        print(request_catagory)
        print(request_diffuculty)
        print(request_type)


        thing_code , questions =  request_questions(request_amount,str(request_catagory),request_diffuculty,request_type)
        print( response_codes[thing_code])
        print(questions)
        #MAIN_QUIZ(request_amount,questions)






    elif inpoot == "2":
        clear()
        list_formatter2(array_untangler(catagories[1],1),"- Mode selection:")
        print(catagory_other_thing(1))
    elif inpoot == "3":
        clear()
        list_formatter2(array_untangler(catagories[2],1),"- Mode selection:")
        print(catagory_other_thing(2))
    elif inpoot == '':
        game_menu()

def main_menu():
    clear()
    list_formatter2(["Play","User managment"],"Menu:")
    user_choice = input("-- ")
    if user_choice == "1":
        game_menu()
    elif user_choice == "2":
        view_user_data()

def game_menu():
    clear()
    list_formatter2(["Quick","Basic","Advanced","Custom"],"Game mode:")
    user_choice = input("-- ")
    if user_choice == "1":
        MAIN_QUIZ(5)
    elif user_choice == "2":
        MAIN_QUIZ(10)
    elif user_choice == "3":
        MAIN_QUIZ(20)
    elif user_choice == "4":
        advanced_game()

def MAIN_QUIZ(quastion_amount,questions):
    active_users_select()
    main_question_loop(quastion_amount,questions)
    clear()



#Initialization things
request_token , users , catagories = data_manager()
save_data()

questions = json.loads(open('questions.json', 'r').read())

main_menu()