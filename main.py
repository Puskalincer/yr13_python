import requests
import json 
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import os

hostName = "localhost"
serverPort = 8080

response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]

request_token = ""

users = []
active_users = []

questions = ""

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
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        return thing["token"] , thing["users"]
    except:
        return get_token() , []
def save_data():
    x = {
      "users": users,
      "token": request_token
    }
    f = open("data.json", "w")
    f.write(json.dumps(x))
    f.close()

def request_questions(amount,token,catagory='',difficulty='',type=''):
    if catagory:
        catagory = '&category=' + catagory
    if difficulty:
        difficulty = '&difficulty=' + difficulty
    if type:
        type = '&type=' + type
    res = requests.get('https://opentdb.com/api.php?amount=' + amount + str(catagory) + difficulty + type + '&token='+ token)
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
    return random.sample(range(change_range), amount)



def main_question_loop(how_many_questions):
    requested_quesions = question_request(how_many_questions)
    x=0
    while x < how_many_questions:
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
    thing_code , questions =  request_questions('50',request_token,catagory=0)
    open('1questions.json', 'w').write(json.dumps(questions , ensure_ascii=False, indent=4 ))

#Initialization things
request_token , users = data_manager()
save_data()

questions = json.loads(open('questions.json', 'r').read())

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
        question_reroll()
        MAIN_QUIZ(20)
    elif user_choice == "4":
        MAIN_QUIZ(10)

def MAIN_QUIZ(quastion_amount):
    active_users_select()
    main_question_loop(quastion_amount)
    clear()

main_menu()