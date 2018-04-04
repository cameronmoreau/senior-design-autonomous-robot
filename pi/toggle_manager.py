import RPi.GPIO as GPIO
import time
from threading import Thread

GPIO_TOGGLE = 10

class ToggleManager(Thread):
  def __init__(self, toggle_callback=None):
    Thread.__init__(self)
    
    # Variables
    self.running = False
    self.last_val = False
    self.toggle_callback = toggle_callback
    
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
  def run(self):
    self.running = True
    
    while self.running:
      toggle = GPIO.input(GPIO_TOGGLE)
      
      if not self.last_val and toggle:
        self.toggle_callback()
        
      self.last_val = toggle
      
      time.sleep(0.1)
      
  def stop(self):
    self.running = False
    
    if self.isAlive():      
      self.join()