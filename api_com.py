import requests
import json 

response_codes = ["Success","No Results","Invalid Parameter ","Token Not Found ","Token Empty ","Rate Limit"]

def api_request(request_string,specify_thingy=''):
    res = requests.get(request_string)
    response = json.loads(res.text)
    if specify_thingy:
        return response[specify_thingy]
    return response

def get_catagories():
    return api_request('https://opentdb.com/api_category.php',"trivia_categories")
     
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
    return api_request('https://opentdb.com/api.php?amount=' + str(amount) + str(catagory) + difficulty + type + token,"results")

def get_token():
    return api_request('https://opentdb.com/api_token.php?command=request',"token") 

def reset_token(token):
    return response_codes[api_request('https://opentdb.com/api_token.php?command=reset&token='+token,"response_code")]

def question_reroll():
    thing_code , questions =  request_questions(50)
    open('questions.json', 'w').write(json.dumps(questions , ensure_ascii=False, indent=4 ))

def catagory_limit(catagory_id):
    return api_request('https://opentdb.com/api_count.php?category='+ str(catagory_id),"category_question_count")