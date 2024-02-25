#!/usr/bin/env python3
from nicegui import ui
import asyncio


dark = ui.dark_mode()
dark.enable()

#ui.spinner('tail',size='lg')


with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('A')
        ui.tab('B')
        ui.tab('C')

with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.left_drawer().style('border-right:2px solid #5898d4') as left_drawer:
    ui.label('Side menu')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='A').classes('w-full'):
    with ui.tab_panel('A'):
    

        async def compute():
            n = ui.notification(timeout=None)
            for i in range(10):
                n.message = f'Computing {i/10:.0%}'
                n.spinner = True
                await asyncio.sleep(0.2)
            n.message = 'Done!'
            n.spinner = False
            await asyncio.sleep(1)
            n.dismiss()

        ui.button('Compute', on_click=compute)

        def on_click1():
            print(catagory_menu.value)
            if catagory_menu.value == 1:
                select.set_options(['General Knowledge', 'Science & Nature', 'Mythology', 'Sports', 'Geography', 'History', 'Politics', 'Art', 'Celebrities', 'Animals', 'Vehicles'], value='General Knowledge')
            if catagory_menu.value == 2:
                select.set_options(['Entertainment: Books', 'Entertainment: Film', 'Entertainment: Music', 'Entertainment: Musicals & Theatres', 'Entertainment: Television', 'Entertainment: Video Games', 'Entertainment: Board Games', 'Entertainment: Comics', 'Entertainment: Japanese Anime & Manga', 'Entertainment: Cartoon & Animations'], value='Entertainment: Books')
            if catagory_menu.value == 3:
                select.set_options(['Science: Computers', 'Science: Mathematics', 'Science: Gadgets'], value='Science: Computers')

        with ui.row().style('display:flex;align-items: center;'):
            catagory_menu = ui.toggle({1: 'Main', 2 :'Entertainment' , 3: 'Science'}, value=1)
            catagory_menu.on("click", on_click1)

            select = ui.select(['General Knowledge', 'Science & Nature', 'Mythology', 'Sports', 'Geography', 'History', 'Politics', 'Art', 'Celebrities', 'Animals', 'Vehicles'], value='General Knowledge')

        toggle2 = ui.toggle({1: 'all', 2 :'easy' , 3: 'medium', 4: 'hard'},value=1)
        toggle4 = ui.toggle({1: 'all', 2 :'mulitple choice' , 3: 'true/false'},value=1)

        ui.input(label='Question amount', placeholder='e.g:5',
                on_change=lambda e: result.set_text('you typed: ' + e.value),
                validation={'Input too long': lambda value: len(value) < 20})
        result = ui.label()

        ui.button('Start quiz', on_click=lambda: ui.notify('Verifying parameters'))

    with ui.tab_panel('B'):
        ui.label('Content of B')
    with ui.tab_panel('C'):
        ui.label('Content of C')

ui.run()