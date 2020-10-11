import PySimpleGUI as sg
import math
import game as logame

# https://stackoverflow.com/questions/60352034/is-there-a-way-to-update-the-grid-in-pysimplegui-after-clicking-on-it

sg.theme('DarkAmber')
        
# Initialize a game matrix
length = 4
width = length

# Create layout
layout = [[sg.B(str(j*length+i), size=(8,4), key=(i,j), button_color=('black','white')) for i in range(length)] for j in range(width)]
layout2 = [sg.B('Start'), sg.B('Hint')]#,sg.Text('',key='hint text')]
layout.append(layout2)

# Create the Window
window = sg.Window('Window Title', layout)

def update_gui():
    for i, row in enumerate(game.matrix):
        for j, value in enumerate(row):
            if value == 1:
                layout[i][j].update(button_color=('white', 'purple'))
            else:
                layout[i][j].update(button_color=('black','white'))

def animate_moves():
    
    window.Read(timeout=1000)
    
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    
    game = logame.Game(length, width)
    text = window[event].get_text()
    
    if text == 'Start':
        game.scramble()
        update_gui()
        
    else:
        continue
                        
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        text = window[event].get_text()
        
        if text == 'Hint':
            hint = game.get_hint()
            sg.popup('hint',hint)
            
        elif text == 'Start':
            game.scramble()
            update_gui()
            
        else:
            num = int(text)
            x = (num)%length
            y = math.floor(num/length)
            logame.perform_move(game.matrix, game.length, game.width, y, x)
            update_gui()

        if logame.is_solved(game.matrix):
            sg.popup('You won!')
            
window.close()