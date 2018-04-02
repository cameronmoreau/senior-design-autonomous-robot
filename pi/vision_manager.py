'''
Creds B/C School
https://gist.github.com/allskyee/7749b9318e914ca45eb0a1000a81bf56
'''

import sys
import time
import cv2
import numpy as np
from threading import Thread, Lock
import image
import utils
import statistics

N_SLICES = 8

# Use pi cam or regular cam
if 'pi' in sys.argv:
	from picamera.array import PiRGBArray
	from picamera import PiCamera
else:
	print('Not a pi')

class VisionManager():
	def __init__(self, commandQueue):
		self.stream = cv2.VideoCapture(0)

		# Set width/height
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

		(self.grabbed, self.frame) = self.stream.read()
		self.running = False
		self.read_lock = Lock()
		self.commandQueue = commandQueue
		self.frames = []
		self.onVertex = False
		
		for i in range(N_SLICES):
			self.frames.append(image.Image())

	def start(self):
		if self.running:
			print('Already started capture')
			return None

		self.running = True
		self.thread = Thread(target=self.update, args=())
		self.thread.start()

		return self

	def update(self):
		while self.running:
			(grabbed, frame) = self.stream.read()

			# Lock
			self.read_lock.acquire()
			self.grabbed = grabbed
			self.frame = frame
			self.read_lock.release()

	def read(self):
		self.read_lock.acquire()
		frame = self.frame.copy()
		self.read_lock.release()
		return frame

	# Used for tk
	def read_rgb(self, detect_lanes=True):
		frame = self.read()
		(b,g,r) = cv2.split(frame)
		frame = cv2.merge((r, g, b))
		
		if detect_lanes:
			tmp_frame = utils.RemoveBackground(frame, False)
			
			directions, contours = utils.SlicePart(tmp_frame, self.frames, N_SLICES)
			
			# Check vertex every 2 seconds
			if int(time.time() % 2) == 0:
				vertex = True if statistics.stdev(contours[3:7]) >= 30 else False
				if vertex != self.onVertex:
					# Do callback here
					pass
					
				print('On vertex: ' + str(vertex))
				
				self.onVertex = vertex
					
		return frame

	def stop(self):
		self.running = False

		if self.thread.is_alive():
			self.thread.join()

	def __exit__(self, exec_type, exec_val, traceback):
		self.stream.release()