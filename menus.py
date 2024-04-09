import eel
import json


users = []
data_file = 'new_data'

def data_manager():
    try:
        data = json.loads(open(data_file+".json", "r").read())
        return data['users']
    except:
        print("error")



def main_menu():
    eel.menu(menu_options["items"],menu_options["title"],False)
    menu_storage.current_menu = menu_options

def game_menu():
    eel.menu(["Quick","Basic","Advanced","Custom"],"Game modes",True)
    menu_storage.current_menu = game_options
    menu_storage.previous_menu = bruh[0]

def user_menu():
    eel.menu(["New user","Delete user","Advanced view"],"Users",True,temp_array)
    menu_storage.previous_menu = bruh[0]


def choose_people():
    eel.menu([i[0] for i in users] ,"Users",True)
    menu_storage.previous_menu = game_menu
    eel.user_chosen




def Save_menu():
    eel.menu(["play save","delete saves"],"Saves",True,[["2","11/9/2001"],["bob","11/9/2001"],["bad","11/9/2001"],["No saves",""]])
    menu_storage.previous_menu = bruh[0]

def setting_menu():
    eel.menu(["Gui mode = web"],"Settings",True)
    menu_storage.previous_menu = bruh[0]

menu_options = {
    "items":["Play","User managment","Continue game","settings"],
    "title":"Menu",
    0:game_menu,
    1:user_menu,
    2:Save_menu,
    3:setting_menu
}

game_options = {
    0:choose_people,
    1:choose_people,
    2:choose_people,
    3:choose_people
}



bruh = {
    0:main_menu
}

class menu_storage:
    current_menu = None
    previous_menu = None




users = data_manager()
temp_array = [x for x in users]
temp_array.insert(0,["User","Score"])
print(users)
print(temp_array)

eel.init('web')

main_menu()

@eel.expose
def runfunc(id):
    menu_storage.current_menu[id]()

@eel.expose
def menu_back():
    menu_storage.previous_menu()



eel.start('test.html')
