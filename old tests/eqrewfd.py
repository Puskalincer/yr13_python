from simple_term_menu import TerminalMenu
import os
from pyboxen import boxen

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()


print(
    boxen(
        "Python is cool!",
        padding=1,
        margin=1,
        color="cyan",
    )
)




def main():
    options = ["entry 1", "entry 2", "entry 3"]
    terminal_menu = TerminalMenu(options)


    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")

if __name__ == "__main__":
    main()