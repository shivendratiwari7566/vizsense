import cv2
import os

class util ():
	def __init__(self):
		self.Genvalu = None		
        	

	def createdir(self,dirpath):
		if not os.path.exists(dirpath):
			try:
				os.makedirs(dirpath)
			except:
				print("unable to create dorectory",dirpath)



			

