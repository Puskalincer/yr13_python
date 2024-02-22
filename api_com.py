import requests
import json 

response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]

def get_catagories():
    res = requests.get('https://opentdb.com/api_category.php')
    response = json.loads(res.text)
    return response["trivia_categories"]

def request_questions(amount,catagory='',difficulty='',type='',token=''):
    #print("harry is better")
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

def get_token():
    res = requests.get('https://opentdb.com/api_token.php?command=request')
    response = json.loads(res.text)
    return response["response_code"] , response["token"]

# Prolly dont need
def reset_token(token):
    res = requests.get('https://opentdb.com/api_token.php?command=reset&token='+token)
    response = json.loads(res.text)
    return response_codes[response["response_code"]]

#Does stuff? prolly wont need
def question_reroll():
    thing_code , questions =  request_questions(50)
    open('questions.json', 'w').write(json.dumps(questions , ensure_ascii=False, indent=4 ))