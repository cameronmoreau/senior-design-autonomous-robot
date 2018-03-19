import tkinter as tk
from game_manager import *
from gui import *

game = GameManager('config.json')

root = tk.Tk()
app = GuiApplication(master=root, game_manager=game)
app.mainloop()