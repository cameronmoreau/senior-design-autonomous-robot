import threading
import tkinter as tk
from game_manager import *
from gui import *
from robot_controller import *

game = GameManager('config.json')
robot = RobotController(simulate=True)

root = tk.Tk()
app = GuiApplication(master=root, game_manager=game, robot=robot)
app.mainloop()