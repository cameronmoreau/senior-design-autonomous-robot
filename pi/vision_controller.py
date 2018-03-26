#!/usr/bin/python
# -*- coding: utf-8 -*-
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import threading

class VisionController(threading.Thread):
	def __init__(self, thread_queue=None, video_buffer=None):
		threading.Thread.__init__(self)
		if thread_queue:
			self.thread_queue = thread_queue
		if video_buffer:
			self.video_buffer = video_buffer
			
		self.cap = cv2.VideoCapture(0)
			
	def run(self):
		while True:
			_, image = self.cap.read()
			
			self.video_buffer[0] = image
	
	def stop(self):
		self.join()