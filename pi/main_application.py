import tkinter as tk
from tkinter import messagebox
import time, threading

from game_manager import *
from gui import *
from robot_controller import *
from localization_manager import *
from navigation_manager import *
from localization_manager import *
from vision_manager import *
from toggle_manager import *

USE_SERIAL = False
USE_GUI = True

if 'serial' in sys.argv:
  USE_SERIAL = True

if 'nogui' in sys.argv:
  USE_GUI = False

TOP_SPEED = 500
MIN_SPEED = 300

class MainApplication():
  def __init__(self, gui=True):
    self.last_time = time.time()
    self.show_gui = gui

    # TEMP
    self.reached_vertex = True
    self.started = True
    
    # REAL STUFF
    self.game = GameManager('config.json')
    self.robot = RobotController(simulate=not USE_SERIAL)
    self.nav = NavigationManager(self.game.path)
    self.local = LocalizationManager(robot=self.robot, game=self.game, start_x=380, start_y=0)
    self.vision = VisionManager(vertex_callback=self.local.on_vertex_change, direction_callback=self.local.on_direction_change)
    self.toggle = ToggleManager(toggle_callback=self.toggle_callback)
    
    # UI
    if self.show_gui:
      root = tk.Tk()
      self.gui = GuiApplication(master=root, vision=self.vision, game_manager=self.game, robot=self.robot, localization_manager=self.local)
     
    # TEMP
    #self.robot.move_raw(-TOP_SPEED, -TOP_SPEED, -TOP_SPEED, -TOP_SPEED)
    #self.local.subscribe_to_events(self.new_waypoint)
    #self.last_waypoint = None
    # self.robot.move_raw(800, -800, -800, 800)
    # threading.Timer(4.6, self.stop_robot).start()
    
  def stop_robot(self):
    print('stopping')
    self.robot.stop()
  
  def toggle_callback(self):
    print('toggled press')

    if self.started:
      self.robot.stop()
    else:
      self.robot.move_raw(800, -800, -800, 800)
    
    self.started = not self.started

  def direction_callback(self, direction):
    if self.reached_vertex:
      return

    can_update = (time.time() - self.last_time) > 0.4
    if direction < -0.3 and can_update:
      print("GO RIGHT")
      self.last_time = time.time()
      self.robot.move_raw(-TOP_SPEED, -MIN_SPEED, -TOP_SPEED, -MIN_SPEED)
    elif direction > 0.3 and can_update:
      print("GO LEFT")
      self.last_time = time.time()
      self.robot.move_raw(-MIN_SPEED, -TOP_SPEED, -MIN_SPEED, -TOP_SPEED)
    elif direction > -0.3 and direction < 0.3 and can_update:
       self.robot.move_raw(-TOP_SPEED, -TOP_SPEED, -TOP_SPEED, -TOP_SPEED)
       self.last_time = time.time()
       print('GO STRIAGHT')
    
  def vertex_callback(self, vertex):
    print('AT VERTEX!')
    return
    if self.reached_vertex:
      return
      
    self.reached_vertex = True
    self.robot.stop()

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
    self.toggle.start()
    
    if self.show_gui:
      self.gui.mainloop()
    else:
      while True:
        self.vision.read_rgb()

    self.vision.stop()
    self.robot.stop()
    self.toggle.stop()