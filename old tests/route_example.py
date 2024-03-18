import flet as ft
import json 
import random
import html


class magic:
    x=0
    max=5

current_question = magic



offline_file = json.loads(open('questions.json', 'r').read())
question = offline_file


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


"""
def main(page: ft.Page):
    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )

    def show_drawer(e):
        page.drawer.open = True
        page.drawer.update()

    page.add(ft.ElevatedButton("Show drawer", on_click=show_drawer))

"""





def main(page: ft.Page):
    page.title = "Routes Example"




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


    side_bar = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )


    """
    def show_drawer(e):
        side_bar.open = True
        side_bar.update()
    """

    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Le Quiz"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Users", on_click=lambda _: page.go("/store")),
                    ft.ElevatedButton("Saved quizes", on_click=lambda _: page.go("/quiz")),
                    ft.ElevatedButton("New Quiz", on_click=lambda _: page.go("/quiz")),
                ],
                drawer=side_bar
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT,actions=[ft.IconButton(icon=ft.icons.CHEVRON_LEFT,on_click=lambda _: page.go("/"),tooltip="back",icon_size=35)]),
                        #ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                    drawer=side_bar
                )
            )
        if page.route == "/quiz":
            page.views.append(
                ft.View(
                    "/quiz",
                    [
                    ft.AppBar(title=ft.Text("Quiz"), bgcolor=ft.colors.SURFACE_VARIANT ,actions=[ft.IconButton(icon=ft.icons.CHEVRON_LEFT,on_click=lambda _: page.go("/"),tooltip="back",icon_size=35)]),
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
                    ],
                    drawer=side_bar
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

#, view=ft.AppView.WEB_BROWSER
ft.app(target=main)