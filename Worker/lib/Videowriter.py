import cv2


class writevideo ():
	def __init__(self):
		self.fourcc = cv2.VideoWriter_fourcc(*'MP4V')		
        	

	def Createwriter(self,filename,frame_width,frame_height):
		self.out = cv2.VideoWriter(filename,self.fourcc, 10, (frame_width,frame_height))

				
	def writeframe(self,frame):
		self.out.write(frame)


	def releasevideo(self):
		self.out.release()




			

