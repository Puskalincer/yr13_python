import flet as ft
import json 
import misc
import random
import html
import time

class magic:
    x=0
    max=5

current_question = magic



offline_file = json.loads(open('questions.json', 'r').read())
question = offline_file["questions"]


def play_save(name):
    f = open("saves/"+name, "r")
    thing = json.loads(f.read())
    f.close()
    main_question_loop(thing["how_many_questions"], thing["questions"],thing["active_users"],thing["current_loop"][0],thing["current_loop"][1])

def format_display_question(questions):
    temp_array = questions["incorrect_answers"]
    temp_array.append(questions["correct_answer"])
    random.shuffle(temp_array)
    return temp_array , questions["question"] , 

def input_manager2(max_override=0,skip_func=1,input_text_override="-- ",any_num=1,bruhz=0):
    while True:
        try:
            number = input(input_text_override)
            if number  == '':
                if skip_func == 1:
                    break
                else:
                    print("\n Required \n")
            elif number == 'save':
                return "save"
            elif number == 'menu':
                return "menu"
            elif number:
                number=int(number)
                if number > 0:
                    number -=1 
                    if any_num == 1:
                        if number >= max_override:
                            print("\n Number to big, limit "+str(max_override)+"\n")
                        else:
                            if bruhz == 1:
                                number+=1
                            return number
                    if any_num == 2:
                        return number
                else:
                    print("\n Input number above 0.\n")
        except:
            print("\n Enter valid Number corresponding to choices displayed.\n")

def main_question_loop(how_many_questions,questions,active_users,x=0,y=0):
    while x < int(how_many_questions):
        question = questions[x]
        thing1 , thing2 = format_display_question(question)
        while y < len(active_users):
            misc.clear()
            print(active_users[y][0] + " -- Question " + str(x) + " of " + str(how_many_questions))
            misc.list_formatter(thing1,thing2)
            user_choice = input_manager2(4,0)
            if int(user_choice) == thing1.index(question["correct_answer"]):
                print("\nCorrect")
                active_users[y][1] += 1
            else:
                print("\nIncorrect : " + question["correct_answer"])
                active_users[y][2] += 1
            input("")
            y=y+1
        x=x+1
        y=0
        misc.clear()
        print("User \t Correct \t Incorrect\n")
        for beans, value in enumerate(active_users):
            print(active_users[beans][0] + " \t " + str(active_users[beans][1]) + " \t \t " + str(active_users[beans][2]))
        input("")

 

def main(page: ft.Page):
    page.title = "Quizzz"
    #page.theme_mode = ft.ThemeMode.DARK
    #page.padding = 50
    #page.update()
        
    """
     def button_clicked(e):
        b.data += 1
        t.value = f"Button clicked {b.data} time(s)"
        page.update()

    b = ft.ElevatedButton("Button with 'click' event", on_click=button_clicked, data=0)
    t = ft.Text()

    page.add(b, t)
    """



    def start(e):
        answer_1.visible = True
        answer_2.visible = True
        answer_3.visible = True
        answer_4.visible = True
        question_text.visible = True
        result_text.visible = True
        start_button.visible = False
        question_counter.visible = True


        answer_1.disabled = False
        answer_2.disabled = False
        answer_3.disabled = False
        answer_4.disabled = False
        update_button.visible=False
        thing1 , thing2 = format_display_question(question[current_question.x])
        result_text.value=""
        temp_num = current_question.x+1
        question_counter.value = temp_num

        print(thing1)
        print(thing2)
        print(len(thing1))

        if len(thing1) == 4:
            answer_1.text = html.unescape(thing1[0])
            answer_2.text = html.unescape(thing1[1])
            answer_3.text = html.unescape(thing1[2])
            answer_4.text = html.unescape(thing1[3])
            answer_3.visible = True
            answer_4.visible = True
        elif len(thing1) == 2:
            answer_1.text = html.unescape(thing1[0])
            answer_2.text = html.unescape(thing1[1])
            answer_3.visible = False
            answer_4.visible = False
        question_text.value = html.unescape(thing2)
        page.update()
        
    def update(e):
        answer_1.disabled = False
        answer_2.disabled = False
        answer_3.disabled = False
        answer_4.disabled = False
        update_button.visible=False
        current_question.x+=1
        thing1 , thing2 = format_display_question(question[current_question.x])
        result_text.value=""
        question_counter.value = current_question.x

        print(thing1)
        print(thing2)
        print(len(thing1))

        if len(thing1) == 4:
            answer_1.text = html.unescape(thing1[0])
            answer_2.text = html.unescape(thing1[1])
            answer_3.text = html.unescape(thing1[2])
            answer_4.text = html.unescape(thing1[3])
            answer_3.visible = True
            answer_4.visible = True
        elif len(thing1) == 2:
            answer_1.text = html.unescape(thing1[0])
            answer_2.text = html.unescape(thing1[1])
            answer_3.visible = False
            answer_4.visible = False
        question_text.value = html.unescape(thing2)
        page.update()


    def answer(e):
        print(e.control.text)
        print(question[current_question.x]["correct_answer"])
        answer_1.disabled = True
        answer_2.disabled = True
        answer_3.disabled = True
        answer_4.disabled = True

        if html.unescape(question[current_question.x]["correct_answer"]) == e.control.text:
            result_text.value="yes"
        else:
            result_text.value="Nope"
        update_button.visible=True
        current_question.x+=1
        page.update()

            
        






    answer_1 = ft.ElevatedButton( visible=False , text="Answer 1", color="blue" , on_click=answer)
    answer_2 = ft.ElevatedButton( visible=False , text="Answer 2", color="red" , on_click=answer)
    answer_3 = ft.ElevatedButton( visible=False , text="Answer 3", color="green" , on_click=answer)
    answer_4 = ft.ElevatedButton( visible=False , text="Answer 4", color="yellow" , on_click=answer)

    update_button = ft.ElevatedButton(text="Next question", on_click=update , visible=False)
    start_button = ft.ElevatedButton(text="Start", on_click=start)

    question_text = ft.Text("question" ,  visible=False)
    result_text = ft.Text("" , visible=False)
    question_counter = ft.Text("" , visible=False)
    

    page.add(   
        question_counter,
        start_button,
        question_text,
        ft.Row(
            [
                ft.Column(
                    [
                        answer_1,
                        answer_3
                    ],
                ),
                ft.Column(
                    [
                        answer_2,
                        answer_4
                    ],
                )
            ]
        ),
        result_text,
        update_button
    )



ft.app(target=main)