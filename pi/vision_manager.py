#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import cv2
import threading
import numpy as np

# Use pi cam or regular cam
if 'pi' in sys.argv:
	from picamera.array import PiRGBArray
	from picamera import PiCamera
else:
	print('Not a pi')

class VisionManager():
	def __init__(self):
		self.capture = cv2.VideoCapture(0)
		self.running = False

		# Set width/height
		self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	
	def start(self):
		self.running = True
		while self.running:
			ret, frame = self.capture.read()

			cv2.imshow('frame', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				self.stop()

	def stop(self):
		self.running = False
		self.capture.release()
		cv2.destroyAllWindows()

# class VisionController():
# 	def __init__(self, thread_queue=None, video_buffer=None):
# 		self.active = False

# 		threading.Thread.__init__(self)
# 		if thread_queue:
# 			self.thread_queue = thread_queue
# 		if video_buffer:
# 			self.video_buffer = video_buffer
			
# 		self.cap = cv2.VideoCapture(0)
			
# 	def run(self):
# 		self.active = True
# 		while self.active:
# 			_, image = self.cap.read()
			
# 			self.video_buffer[0] = image
	
# 	def stop(self):
# 		self.active = False
# 		if self.is_alive():
# 			self.join()