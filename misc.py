import os
import socket

#Utilitys -Final
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def divider():
    print("\n" + 34 * "-" + "\n")
def cd():
    clear()
    divider()

#Checks internet connection https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

def list_formatter(arrayname,array_name_formatted,instructions=""):
    if instructions:
        divider()
        print(instructions)
    divider()
    print(array_name_formatted)
    for idx , array_item in enumerate(arrayname , start=1):
        print(str(idx) + " - "+ array_item)
    divider()

def array_untangler(array,item=0):
    temp_array = []
    for x in array:
        temp_array.append(x[item])
    return temp_array 

#https://opentdb.com/api_count.php?category=9

"""
LOOK AT THIS LATERRR

import SimpleHTTPServer
import SocketServer

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/your_file.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)

server.serve_forever()
"""

"""
TOO DO LIST

Add error checking to everything. Done

Add automatic checking for advanced game choice validity

Make game remember the stuff

"""

"""
class SaveFile:
    save_file = "save.json"
    save_data = {}

    def __init__(self, save_file: str, auto_load: bool = True) -> None:
        self.save_file = save_file
        if auto_load:
            self.load()

    def load(self) -> None:
        try:
            with open(self.save_file, "r") as file:
                data = file.read().encode('utf-8')
                try:
                    data = base64.b64decode(data)
                except base64.binascii.Error:
                    debug_message("File is not base64 encoded, must be an older save", "save_file")
                try:
                    self.save_data = json.loads(data.decode('utf-8'))
                except json.decoder.JSONDecodeError:
                    error("File is corrupt, deleting file automatically")
                    file.close()
                    os.remove(self.save_file)
                    return
                file.close()

        except FileNotFoundError:
            return

    def save(self) -> None:
        if not os.path.exists(DATA_FOLDER):
            os.mkdir(DATA_FOLDER)
        with open(self.save_file, "w") as file:
            save_dict = self.save_data
            try:
                del save_dict["save_data"]
            except KeyError:
                pass
            data = json.dumps(save_dict, ensure_ascii=False).encode('utf-8')
            data = base64.b64encode(data)
            file.write(data.decode('utf-8'))
            file.close()

class UserData(SaveFile):
    # User settings
    display_mode = None
    network = None
    auto_fix_api = None

    def __init__(self) -> None:
        super().__init__(DATA_FOLDER + "data.json")

        # Load the data from the save file
        self.display_mode = try_convert(self.save_data.get("display_mode"), str)
        self.network = try_convert(self.save_data.get("network"), bool)
        self.auto_fix_api = try_convert(self.save_data.get("auto_fix_api"), bool)

        # Load the default values if the data is not found
        self.load_defaults()

    def load_defaults(self) -> None:
        self.display_mode = set_if_none(self.display_mode, "GUI")
        self.network = set_if_none(self.network, True)
        self.auto_fix_api = set_if_none(self.auto_fix_api, True)

    def save(self) -> None:
        self.save_data = self.__dict__

        super().save()
"""

"""

#print(internet())


#Timer
start = time.time()
#stuff
end = time.time()
length = start - end
print("It took", length, "seconds!")



def main_question_loop_test(how_many_questions,questions,change_range=50):
    requested_quesions = question_request(how_many_questions,int(change_range))
    current_question=0



    for x in active_users:
        test_results.append([x[0]]) 
    print(test_results)
    input()

    while current_question < int(how_many_questions):
        question = questions[requested_quesions[current_question]]
        thing1 , thing2 = format_display_question(question)
        current_question=current_question+1
        y=0
        while y < len(active_users):
            misc.clear()
            print(active_users[y][0] + " -- Question " + str(current_question) + " of " + str(how_many_questions))
            misc.list_formatter(html.unescape(thing1),html.unescape(thing2))
            user_choice = input()
            if int(user_choice) == thing1.index(question["correct_answer"])+1:
                print("\nCorrect")
                active_users[y][1] += 1
            else:
                print("\nIncorrect : " + question["correct_answer"])
                active_users[y][2] += 1
            input("")
            y=y+1
        misc.clear()
        print("User \t Correct \t Incorrect\n")
        for beans, value in enumerate(active_users):
            print(active_users[beans][0] + " \t " + str(active_users[beans][1]) + " \t \t " + str(active_users[beans][2]))
        input("")

#active_users_select()
#main_question_loop_test(2,questions)

#print(test_results_mabye[0][1]["Q1"])
        
"""

"""
#Progress bar
def start_progress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def end_progress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()

misc.clear()
start_progress("Time")
for x in range(100):
    time.sleep(0.1)
    progress(x)


"""
