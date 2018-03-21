import threading
import tkinter as tk
from game_manager import *
from gui import *
from robot_controller import *
from localization_manager import *

if __name__ == '__main__':
  game = GameManager('config.json')
  robot = RobotController(simulate=True)
  local = LocalizationManager(game.path)

  print('finding path between 1 and 15')
  p, c = local.get_route('1', '15')
  print('path', str(p), 'cost', c)

  root = tk.Tk()
  app = GuiApplication(master=root, game_manager=game, robot=robot)
  app.mainloop()