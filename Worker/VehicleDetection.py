import cv2
import numpy as np
import time
import numpy as np
import os
import shutil
from Functions.serving import detectobjects


counter=0
i=0
count=0


det=detectobjects()

def vehdet():
	rundetection=True
	if rundetection==True:
		if len(os.listdir('./Input')) == 0:
			print("Directory is empty")
		else:
			print("Directory is not empty")
			files=os.listdir("./Input")
			for filename in files :
				#print(filename)
				if filename.split('.')[-1]=='mp4':
					xfname='./Input/' + filename.split('.')[0]+'.xml'
					if os.path.exists(xfname)==True:
						labelid_startvalue=0

						framecount=0
						capture=None
						print(filename)
						capture =cv2.VideoCapture('./Input/'+filename)
						totalframes=int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
						fileout="./output_video/"+filename   
						colors = [tuple(255 * np.random.rand(3)) for i in range(7)]
						while (capture.isOpened()):
							stime = time.time()
							ret, frame = capture.read()
							if frame is not None:
								framecount+=1
								frame=cv2.resize(frame,(800,800))
								h,w,c=frame.shape							
								retclasses,retboxes,retscores=det.object_detection_functionnew(frame)
								frame=cv2.putText(frame,"Frame"+str(framecount) , (w-100, h+30), cv2.FONT_HERSHEY_TRIPLEX,0.5,(200, 200, 200), 1)
								print('boxes',retboxes)
								if len(retboxes)>0:
									for retclass,bx,retscore in zip(retclasses,retboxes,retscores):
										ymin,xmin,ymax,xmax=bx
										#newdata=logs.add_entry(frame,framecount,classid,bx,labelid,totalframes)  #update log entry
										frame=cv2.putText(frame,retclass , (xmin, ymin-5), cv2.FONT_HERSHEY_TRIPLEX,0.5,(200, 200,200),1)
										frame=cv2.rectangle(frame, (xmin,ymin),(xmax,ymax),(0, 255, 0) ,5)

								cv2.imshow('RSRV Automation -' +filename, frame)
								cv2.waitKey(1)
								print('FPS {:.1f}'.format(1 / (time.time() - stime)))
								if cv2.waitKey(1) & 0xFF == ord('q'):
									break
							else:
								capture.release()
								cv2.destroyAllWindows()
								break

						capture.release()


					else:

						print("XML Schema file is missing for "+filename)	
	#xmlgen.process_intermediate()
	cv2.destroyAllWindows()

vehdet()
