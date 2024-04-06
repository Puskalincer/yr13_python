import eel


def main_menu():
    eel.menu(menu_options["items"],menu_options["title"],False)
    menu_storage.current_menu = menu_options

def game_menu():
    eel.menu(["Quick","Basic","Advanced","Custom"],"Game modes",True)
    menu_storage.previous_menu = bruh[0]


def Save_menu():
    eel.menu(["play save","delete saves"],"Saves",True)
    menu_storage.previous_menu = bruh[0]


menu_options = {
    "items":["Play","User managment","Continue game","settings"],
    "title":"Menu",
    0:game_menu,
    1:game_menu,
    2:Save_menu,
    3:Save_menu
}

bruh = {
    0:main_menu
}

class menu_storage:
    current_menu = None
    previous_menu = None



eel.init('web')

main_menu()

@eel.expose
def runfunc(id):
    menu_storage.current_menu[id]()

@eel.expose
def menu_back():
    menu_storage.previous_menu()



eel.start('test.html')
