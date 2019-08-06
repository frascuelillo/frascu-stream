# Get camera images by independ thread
import cv2
from threading import Thread
import time


class CameraStream:

	def __init__(self, source=0, name="CameraStream"):
		# Start camera and read one frame
		self.cap = cv2.VideoCapture(source+cv2.CAP_DSHOW)
		self.ret, self.frame = self.cap.read()
		self.name = name
		self.fps_stream=0
		self.stop = False
		self.finished = False


	def start(self):
		# Start the update trhead
		t = Thread(target=self.update, name=self.name, args=())
		t.start()
		return self

	def update(self):
		# Start de imread loop and measure read FPS every n cicles
		count=0
		cicles=20
		while self.stop == False:
			if count==0:
				inicio=time.clock()
			self.ret, self.frame = self.cap.read()
			if self.ret==False:
				print('No frame received from camera, thread stopped')
				break
			count = count+1
			if count==cicles:

				end=time.clock()
				elapsed=end-inicio

				self.fps_stream=int((1/elapsed)*cicles)
				#print(count, cicles, elapsed,self.fps_stream)
				count=0
		self.cap.release()
		self.finished=True
			
		return			
			
	def read(self):
		# Return last readed frame and "ret" for validate.
		return self.ret,self.frame

	def release(self):
		# Stop the thread
		self.stop = True

	def set(self,prop,value):
		# Property set
		self.cap.set(prop,value)

	def get(self,prop):
		# Property get
		value = self.cap.get(prop)
		return(value)

if __name__ == "__main__":
	#Test
	cap=CameraStream()
	# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	# cap.set(cv2.CAP_PROP_FOURCC, fourcc)
	# cap.set(cv2.CAP_PROP_FPS,60)
	cap.start()
	while True:
		ret,img = cap.read()
		if ret:
			cv2.putText(img,'FPS:'+str(cap.fps_stream),(50,50),cv2.FONT_ITALIC,2,(0,255,0))
			cv2.imshow('Test window, press "q" to close window',img)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break	
		else:
			print('Failed to retrieve frame from camera, exiting.....')
			break
	cap.release()
	print('Test finished')
