import time, sys
from threading import Thread

GPIO_TOGGLE = 10
USE_PI = False

if 'pi' in sys.argv:
  USE_PI = True

if USE_PI:
  import RPi.GPIO as GPIO

class ToggleManager(Thread):
  def __init__(self, toggle_callback=None):
    Thread.__init__(self)
    
    # Variables
    self.running = False
    self.last_val = False
    self.toggle_callback = toggle_callback
    
    # Set up GPIO
    if USE_PI:
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(GPIO_TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
  def run(self):
    self.running = True
    
    while self.running:
      if USE_PI:
        toggle = GPIO.input(GPIO_TOGGLE)
      else:
        toggle = False
      
      if not self.last_val and toggle:
        self.toggle_callback()
        
      self.last_val = toggle
      
      time.sleep(0.1)
      
  def stop(self):
    self.running = False
    
    if self.isAlive():      
      self.join()