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
USE_PI = False

if 'pi' in sys.argv:
  USE_PI = True

# Use pi cam or regular cam
if USE_PI:
	from picamera.array import PiRGBArray
	from picamera import PiCamera
	from imutils.video.pivideostream import PiVideoStream
else:
  from imutils.video.webcamvideostream import WebcamVideoStream
  print('Not a pi')

class VisionManager():
	def __init__(self, vertex_callback=None, direction_callback=None):
		self.stream = None
		
		if USE_PI:
		  self.stream = PiVideoStream(resolution=(640,480))
		  #camera = PiCamera()
		  #camera.resolution = (640, 480)
		  #raw_capture = PiRGBArray(camera, size=camera.resolution)
		  #self.stream = camera.capture_continuous(raw_capture, format='bgr', use_vido_port=True)
		else:
		  self.stream = cv2.VideoCapture(0)
		  
		  # Set width/height
		  self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		  self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

		(self.grabbed, self.frame) = self.stream.read()
		self.running = False
		self.read_lock = Lock()
		self.frames = []
		self.on_vertex = False
		
		self.vertex_callback = vertex_callback
		self.direction_callback = direction_callback
		
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
				vertex = True if statistics.stdev(contours[0:5]) >= 30 else False
				if vertex != self.on_vertex and self.vertex_callback:
					self.vertex_callback(vertex)
					
				self.on_vertex = vertex
			
			if not self.on_vertex:	
				m = statistics.mean(directions[0:6])
				self.direction_callback(m/250)
				
				#if m >= 80 or m <= -80:
					#self.direction_callback(m / 250)
		return frame

	def stop(self):
		self.running = False

		if self.thread.is_alive():
			self.thread.join()

	def __exit__(self, exec_type, exec_val, traceback):
		self.stream.release()