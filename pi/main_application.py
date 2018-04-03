import tkinter as tk
from tkinter import messagebox
import time

from game_manager import *
from gui import *
from robot_controller import *
from localization_manager import *
from navigation_manager import *
from localization_manager import *
from vision_manager import *
import queue

class MainApplication():
  def __init__(self):
    self.last_time = time.time()
    
    self.commandQueue = queue.Queue()
    self.game = GameManager('config.json')
    self.robot = RobotController(simulate=True)
    self.nav = NavigationManager(self.game.path)
    self.local = LocalizationManager(robot=self.robot, game=self.game, start_x=380, start_y=0)
    #self.vision = VisionManager(vertex_callback=self.local.on_vertex_change, direction_callback=self.local.on_direction_change)
    self.vision = VisionManager(vertex_callback=self.local.on_vertex_change, direction_callback=self.direction_callback)

    # UI
    root = tk.Tk()
    self.gui = GuiApplication(master=root, vision=self.vision, game_manager=self.game, robot=self.robot, localization_manager=self.local)
     
    # TEMP
    self.robot.move_raw(200, 200, -200, -200)
    #self.local.subscribe_to_events(self.new_waypoint)
    #self.last_waypoint = None
    
  def direction_callback(self, direction):
    can_update = (time.time() - self.last_time) > 0.4
    if direction < -0.3 and can_update:
      print("GO RIGHT last time")
      self.last_time = time.time()
      self.robot.move_raw(50, 200, -50, -200)
    elif direction > 0.3 and can_update:
      print("GO LEFT")
      self.last_time = time.time()
      self.robot.move_raw(200, 50, -200, -50)
    elif direction > -0.3 and direction < 0.3 and can_update:
       self.robot.move_raw(200, 200, -200, -200)
       self.last_time = time.time()
       print('STRAINGT')
    print(str(direction))
    
  def new_waypoint(self):
    # On new waypoint
    curr = self.local.current_waypoint
      
    if self.last_waypoint is None and curr is not None:
      if curr.id == '15':
        self.robot.stop()
        messagebox.showinfo(message='FUCK YEAH! give us A pls')
        return

      print('Current', curr.id, self.nav.get_route(str(curr.id), '15'))
      self.robot.stop()
      d, p = self.nav.get_route(curr.id, '15')
      print('Path to 15', d, str(p))
      next_point = p[1]
      x, y = self.local.position_x, self.local.position_y
      
      a = self.game.get_bearing_to_coin(next_point, x, y)
      print('Next point', next_point, 'angle is', a)
      self.robot.move(a, 5)

  def start(self):
    self.vision.start()
    self.gui.mainloop()

    # Stop visioning
    self.vision.stop()
    self.robot.stop()