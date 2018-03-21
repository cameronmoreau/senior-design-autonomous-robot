import serial

class Robot():
  def __init__(self, simulate=False):
    if simulate:
      self.serial = dict()
    else:
      self.serial = serial.Serial('/dev/ttyACM0', 9600)

    # Robot localization
    # self.position = (380, 700)
    self.position = (380, 0)
    self.rotation = 0
    self.speed = 0

    # temp
    self.direction = 0

  def set_position(self, x, y):
    self.position = (x, y)

  def move(self, direction, speed):
    print("moving robot", direction, speed)
    self.direction = direction
    self.speed = speed

    # Send serial
    s = 'm ' + str(direction) + ' ' + str(speed)
    self.serial.write(s.encode())

  def set_speed(self, speed):
    self.move(self.direction, speed)
  