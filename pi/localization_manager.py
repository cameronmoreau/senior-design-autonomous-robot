from threading import Timer
import time
from robot_controller import *

class LocalizationManager():
  def __init__(self, robot=None, game=None, start_x=None, start_y=None):
    self.thread = None
    self.robot = robot
    self.game = game

    # Localization vars
    self.position_x = start_x
    self.position_y = start_y
    self.rotation = 0

    self.current_waypoint = None

    self.robot.subscribe_to_events(self.__robot_changed)
    self.start()

  def set_position(self, x, y):
    self.position_x = x
    self.position_y = y
  
  def start(self):
    self.thread = Timer(0.1, self.__handle_update)
    self.thread.start()

  def stop(self):
    if self.thread:
      self.thread.cancel()

  def __robot_changed(self):
    print('LOCALIZATION GOT ROBOT CHANGE')

  
  def __handle_update(self):
    # handle estimate
    if self.robot.is_moving():
      speed = 5
      if self.robot.direction == 0:
        self.position_y -= speed
      elif self.robot.direction == 90:
        self.position_x += speed
      elif self.robot.direction == 180:
        self.position_y += speed
      elif self.robot.direction == 270:
        self.position_x -= speed

      # Waypoint detection
      if self.current_waypoint is None:
        c, d = self.game.get_closest_coin(self.position_x, self.position_y)
        if d < 150:
          print('IM CURRENTLY AT THE COIN', c.id)
          self.current_waypoint = c
      else:
        d = self.game.get_distance_from_coin(self.current_waypoint.id, self.position_x, self.position_y)
        print("IM AT WAYPOINT", self.current_waypoint.id, "away", d)

    self.start()