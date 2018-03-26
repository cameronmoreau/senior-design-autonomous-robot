import tkinter as tk

from game_manager import *
from gui import *
from robot_controller import *
from localization_manager import *
from navigation_manager import *
from localization_manager import *
from vision_manager import *

class MainApplication():
  def __init__(self):
    self.game = GameManager('config.json')
    self.robot = RobotController(simulate=True)
    self.nav = NavigationManager(self.game.path)
    self.local = LocalizationManager(robot=self.robot, game=self.game, start_x=380, start_y=0)
    self.vision = VisionManager()

    # UI
    root = tk.Tk()
    self.gui = GuiApplication(master=root, vision=self.vision, game_manager=self.game, robot=self.robot, localization_manager=self.local)

    # TEMP
    self.local.subscribe_to_events(self.new_waypoint)
    self.last_waypoint = None

  def new_waypoint(self):
    # On new waypoint
    curr = self.local.current_waypoint
    if self.last_waypoint is None and curr is not None:
      self.robot.stop()
      d, p = self.nav.get_route(curr.id, '15')
      print('Path to 15', d, str(p))
      next_point = p[1]
      x, y = self.local.position_x, self.local.position_y
      a = self.game.get_angle_to_coin(next_point, x, y)
      print('Next point', next_point, 'angle is', a)

  def start(self):
    self.vision.start()
    self.gui.mainloop()

    # Stop visioning
    self.vision.stop()