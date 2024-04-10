import os

class Menu:
    current_menu = None
    previous_menu = None

    options_choice = None
    options = None
    title = None

    def setup_menu(self):
        self.options_choice = self.current_menu.get('options_choice')
        self.options = self.current_menu.get('options')
        self.title = self.current_menu.get('title')

    def display_menu(self):
        self.setup_menu()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.title + '\n')
        for x , y in enumerate(self.options , start=1):
            print(str(x)+' '+y)
        print("\n")
        user_choice = input()
        if user_choice == '':
            self.change_menu(self.previous_menu)
        user_choice = int(user_choice)
        user_choice-=1
        self.change_menu(self.options_choice[user_choice]())

    def change_menu(self,menu):
        self.previous_menu=self.current_menu
        self.current_menu=menu
        self.display_menu()
       


def main_menu():
    return {
        'title':'Menu',
        'options':['play','users','saves','settings'],
        'options_choice':[game_menu]
    }

def game_menu():
    return {
        'title':'Game Menu',
        'options':["Quick","Basic","Advanced","Custom"],
        'options_choice':[main_menu]
    }


menu = Menu()

menu.current_menu = main_menu()
menu.display_menu()
