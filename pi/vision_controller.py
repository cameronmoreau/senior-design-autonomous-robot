def VisionController(thread_queue = None):
	result = 0
	
	for i in range(10000):
		thread_queue.put(i)