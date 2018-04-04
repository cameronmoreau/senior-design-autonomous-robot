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
		self.camera = None
		
		if USE_PI:
		  self.camera = PiVideoStream(resolution=(640,480))
		  #camera = PiCamera()
		  #camera.resolution = (640, 480)
		  #raw_capture = PiRGBArray(camera, size=camera.resolution)
		  #self.stream = camera.capture_continuous(raw_capture, format='bgr', use_vido_port=True)
		else:
		  #self.stream = cv2.VideoCapture(0)
		  self.camera = WebcamVideoStream(src=1)
		  
		  # Set width/height
		  self.camera.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		  self.camera.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

		self.frames = []
		self.on_vertex = False
		
		self.vertex_callback = vertex_callback
		self.direction_callback = direction_callback
		
		for i in range(N_SLICES):
			self.frames.append(image.Image())

	def start(self):
		self.camera.start()

		return self

	# Used for tk
	def read_rgb(self, detect_lanes=True):
		frame = self.camera.read()
		(b,g,r) = cv2.split(frame)
		frame = cv2.merge((r, g, b))
		
		if detect_lanes:
			tmp_frame = utils.RemoveBackground(frame)
			
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

		return tmp_frame

	def stop(self):
		self.camera.stop()

		# if self.thread.is_alive():
		# 	self.thread.join()

	# def __exit__(self, exec_type, exec_val, traceback):
	# 	self.stream.release()