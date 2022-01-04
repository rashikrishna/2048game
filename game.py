from os import remove
import tkinter as tk
from tkinter import filedialog
import sys
from collections import namedtuple

from game2048 import Game2048

root = tk.Tk()
root.title('2048')
# canvas = tk.Canvas(root, width=600, height=600)
# canvas.grid(columnspan=6, rowspan=4)


colour = namedtuple('colour', ('bg', 'fg'))
colour_palette = {
    0: colour('#FFFFFF', '#000000'),
    2: colour('#FFEAE5', '#000000'),
    4: colour('#FFD5CC', '#000000'),
    8: colour('#FFC0B3', '#000000'),
    16: colour('#FFAB99', '#000000'),
    32: colour('#FF9680', '#000000'),
    64: colour('#FF8166', '#000000'),
    128: colour('#FF6C4D', '#000000'),
    256: colour('#FF5733', '#000000'),
    512: colour('#DF4C2D', '#FFFFFF'),
    1024: colour('#9F3620', '#FFFFFF'),
    2048: colour('#602113', '#FFFFFF'),
}
    

tiles = [tk.Label(root, padx=40, pady=40, width=6, font = "Calibiri 25 bold") for _ in range(16)]

def replay():
    game = Game2048()
    game.insert_element()
    for widget in reversed(game_over_widgets):
        widget.grid_remove()
    # canvas.destroy()
    change_tiles_on_board(game)

def exit_game():
    sys.exit(0)


def game_over(status):
    #TODO: replace with appropriate action when game is lost
    overlay()
    msg_label.grid(row=1, column = 1, columnspan=4, rowspan=4)
    replay_button.grid(row=5, column=1)
    exit_button.grid(row=5, column=2)
    msg_label.config(text=f'You {status} the game!')
    # input("You lost the game")
    # sys.exit(0)

def move(direction: str, game_obj: Game2048) -> None:
    if game_obj.perform_move(direction):
        if game_obj.check_if_won():
            game_over('won')
        game_obj.insert_element()
        change_tiles_on_board(game_obj)
        if game_obj.is_game_over():
            game_over('lost')

def change_tiles_on_board(game_obj):
    for idx, tile in enumerate(tiles):
        row = idx//4
        col = idx%4
        tile_val = game_obj.board[idx//4, idx%4]
        tile.grid(column=col+1, row=row+2)
        tile.config(text = str(tile_val), bg=colour_palette[tile_val].bg, fg=colour_palette[tile_val].fg)

def load():
    file = filedialog.askopenfilename(title='Select save file', filetypes=(('text files', '*.txt'), ))
    game.load_game(file)
    change_tiles_on_board(game)

def save():
    overlay()
    save_entry.grid(row=1, column=2)
    save_entry_label.grid(row=1, column=1)
    confirm_save_button.grid(row=2, column=1)
    cancel_save_button.grid(row=2, column=2)

def remove_save_widgets():
    save_entry_label.grid_remove()
    save_entry.grid_remove()
    confirm_save_button.grid_remove()
    cancel_save_button.grid_remove()
    canvas.grid_remove()

def confirm_save():
    file = save_entry.get()
    game.save_game(file)
    remove_save_widgets()

def overlay():
    canvas.grid(row=1, column=1, rowspan=4, columnspan=4)


save_button = tk.Button(root, text='Save', command=save)
load_button = tk.Button(root, text='Load', command=load)
load_button.grid(row=1, column=2)
save_button.grid(row=1, column=1)

canvas = tk.Canvas(root, width=300, height=300)

#save widgets
save_entry_label = tk.Label(canvas, font='Calibiri 25', text='File Name: ')
save_entry = tk.Entry(canvas, font='Calibiri 25')
confirm_save_button = tk.Button(canvas, text='Save', padx=20, pady=20, font='Calibiri 25 bold', command=confirm_save)
cancel_save_button = tk.Button(canvas, text="Cancel", padx=20, pady=20, font='Calibiri 25 bold', command=remove_save_widgets)

msg_label = tk.Label(canvas, font='Calibiri 25 bold', pady=25)
replay_button = tk.Button(canvas, text='replay', padx=20, pady=20, font='Calibiri 25 bold', command=replay)
exit_button = tk.Button(canvas, text='exit', padx=20, pady=20, font='Calibiri 25 bold', command=exit_game)
game_over_widgets = (canvas, msg_label, replay_button, exit_button)

game = Game2048()
game.insert_element()
change_tiles_on_board(game)
# game_over('lost')

root.bind('<Up>', lambda x: move('up', game))
root.bind('<Down>', lambda x: move('down', game))
root.bind('<Left>', lambda x: move('left', game))
root.bind('<Right>', lambda x: move('right', game))




root.mainloop()