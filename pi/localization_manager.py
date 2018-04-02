import time, math
from threading import Timer
from robot_controller import *

DISTANCE_THRESHOLD = 150
DISTANCE_PER_TICK = 5
ROTATION_PER_TICK = 5

class LocalizationManager():
  def __init__(self, robot=None, game=None, start_x=None, start_y=None):
    self.thread = None
    self.robot = robot
    self.game = game

    # Localization vars
    self.position_x = start_x
    self.position_y = start_y
    self.rotation = 0

    self.listeners = list()
    self.current_waypoint = None
  
    self.robot.subscribe_to_events(self.__robot_changed)
    self.start()
  
  def on_vertex_change(self, on_vertex):
  	print(str(on_vertex))

  def set_position(self, x, y):
    self.position_x = x
    self.position_y = y
  
  def start(self):
    self.thread = Timer(0.1, self.__handle_update)
    self.thread.start()

  def stop(self):
    if self.thread:
      self.thread.cancel()

  def subscribe_to_events(self, listener_event):
    self.listeners.append(listener_event)

  def __robot_changed(self):
    print('LOCALIZATION GOT ROBOT CHANGE')

  def __notify_event(self):
    for e in self.listeners:
      e()
  
  def __handle_update(self):
    # handle estimate
    if self.robot.is_rotating():
      self.rotation += ROTATION_PER_TICK

    elif self.robot.is_moving():
      d = math.radians(self.robot.direction)
      self.position_x += DISTANCE_PER_TICK * math.sin(d)
      self.position_y += DISTANCE_PER_TICK * math.cos(d)
      # if self.robot.direction == 0:
      #   self.position_y -= speed *
      # elif self.robot.direction == 90:
      #   self.position_x += speed
      # elif self.robot.direction == 180:
      #   self.position_y += speed
      # elif self.robot.direction == 270:
      #   self.position_x -= speed

      # Waypoint detection
      if self.current_waypoint is None:
        c, d = self.game.get_closest_coin(self.position_x, self.position_y)
        if d < DISTANCE_THRESHOLD:
          self.current_waypoint = c
          self.__notify_event()
      else:
        d = self.game.get_distance_from_coin(self.current_waypoint.id, self.position_x, self.position_y)
        if d > DISTANCE_THRESHOLD:
          self.current_waypoint = None
          self.__notify_event()

    self.start()