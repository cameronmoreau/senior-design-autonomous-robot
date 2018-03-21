import threading
import tkinter as tk
from game_manager import *
from gui import *
from robot import *

game = GameManager('config.json')
robot = Robot(simulate=True)

root = tk.Tk()
app = GuiApplication(master=root, game_manager=game, robot=robot)
app.mainloop()