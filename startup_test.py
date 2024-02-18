import requests
import json 
import os

response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]

request_token = ""

catagories = [[],[],[]]

users = []
active_users = []



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')    




#Runs on first start, never used again.
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

#Runs on first start, never used again.
def generate_data_file():
    x = {
        "users": [],
        "token": "",
        "catagories" : []
    }
    f = open("data_test.json", "w")
    f.write(json.dumps(x))
    f.close()

#Runs on first start, never used again.
def one_time_start():
    print("Generating Start file")
    generate_data_file()
    prepare_catagories()
    response_code , request_token_temp = get_token()
    if response_code == 0:
        request_token = request_token_temp
    save_new([],request_token,catagories)
    data_manager()

#Runs on first start, never used again.
def get_token():
    res = requests.get('https://opentdb.com/api_token.php?command=request')
    response = json.loads(res.text)
    return response["response_code"] , response["token"]

#Always runs at on startup
def data_manager():
    try:
        f = open("data_test.json", "r")
        thing = json.loads(f.read())
        f.close()
        return [thing["token"] , thing["users"] , thing["catagories"]]
    except:
        one_time_start()
        return "o_t_s"
        
        

#Depreciated
def save_data():
    x = {
        "users": users,
        "token": request_token,
        "catagories" : catagories
    }
    f = open("data_test.json", "w")
    f.write(json.dumps(x))
    f.close()

#Replacment
def save_new(users='',token='',catagories=''):
    with open('data_test.json') as infile:
        data = json.load(infile)
    if users:
        data["users"] = users
    if token:
        data["token"] = token
    if catagories:
        data["catagories"] = catagories

    with open('data_test.json', 'w') as outfile:
        json.dump(data, outfile)






results = data_manager()
if results != "o_t_s":
    users = results[0]
    request_token = results[1]
    catagories = results[2]



print(users)
print(request_token)
print(catagories)


#save_data()
        

