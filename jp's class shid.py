import os

os.system('cls' if os.name == 'nt' else 'clear')

class Active_user:
    name = None
    correct = 0
    incorrect = 0

class Game:
    user_array=[]


    def add_users(self,data_list:list=None,names:list=None) -> None:

        if data_list:
            user_amount = len(data_list)
        else:
            user_amount = len(names)
        
        for x in range(user_amount):  
            user = Active_user()
            if data_list != None:
                data = data_list[x]
                user.name=data.get('name')
                user.correct=data.get('correct')
                user.incorrect=data.get('incorrect')
            else:
                user.name=names[x]

            self.user_array.append(user)

    def export_users(self) -> None:
        formatted_user_array = []
        for x in self.user_array:
            user_data = {
                "name":x.name,
                "correct":x.correct,
                "incorrect":x.incorrect
            }
            formatted_user_array.append(user_data)
        return formatted_user_array

    def clear_users(self):
        self.user_array.clear()





chosen_names = ["John","Bob"]

chosen_data = [{
                "name":"Beilif",
                "correct":50,
                "incorrect":521,
            },
            {
                "name":"John",
                "correct":4321,
                "incorrect":12,
            }]




Game().add_users(data_list=chosen_data)

users = Game().user_array

for user in users:
    print(user.name)
    user.correct+=5
    print(user.correct)
    print(user.incorrect)

Game().clear_users()
Game().add_users(names=["Dean","Jeremy"])

for user in users:
    print(user.name)
    print(user.correct)
    print(user.incorrect)




print(Game().export_users())