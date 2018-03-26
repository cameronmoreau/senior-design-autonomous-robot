import threading
import tkinter as tk
from game_manager import *
from gui import *
from robot_controller import *
from localization_manager import *
from navigation_manager import *
from localization_manager import *
from vision_manager import *

def main():
  game = GameManager('config.json')
  robot = RobotController(simulate=True)
  nav = NavigationManager(game.path)
  local = LocalizationManager(robot=robot, game=game, start_x=380, start_y=0)

  # Testing path and navigation
  # print('finding path between 1 and 15')
  # p, c = nav.get_route('1', '15')
  # print('path', str(p), 'cost', c)

  # root = tk.Tk()
  # app = GuiApplication(master=root, game_manager=game, robot=robot, localization_manager=local)
  
  # app.mainloop()

  vision = VisionManager()
  vision.start()

  
if __name__ == '__main__':
  main()