import serial
from enum import Enum

class RobotController():
  def __init__(self, simulate=False):
    self.simulate = simulate

    if simulate:
      self.serial = dict()
    else:
      self.serial = serial.Serial('/dev/ttyACM0', 9600)

    self.speed = 0
    self.direction = 0 # Direction in degrees
    self.rotating_direction = 0 # Direction 1 clockwise, -1 counter, 0 nothing

    self.listeners = list()

  def subscribe_to_events(self, listener_event):
    self.listeners.append(listener_event)

  def __notify_event(self):
    for e in self.listeners:
      e()

  def is_moving(self):
    return self.speed > 0

  def is_rotating(self):
    return self.rotating_direction != 0 and self.speed > 0

  def move(self, direction, speed):
    print("moving robot", direction, speed)
    self.direction = direction
    self.speed = speed

    # Send serial
    if not self.simulate:
      s = 'm ' + str(direction) + ' ' + str(speed)
      self.serial.write(s.encode())
    
    # Send event
    self.__notify_event()

  def rotate(self, direction, speed):
    self.rotating_direction = direction
    self.speed = speed

    # Send event
    self.__notify_event()

  def stop(self):
    self.direction = 0
    self.rotating_direction = 0
    self.set_speed(0)

  def set_speed(self, speed):
    self.move(self.direction, speed)
  