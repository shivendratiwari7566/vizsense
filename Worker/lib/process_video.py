import threading
import time
import cv2
import numpy as np
import os
import imagezmq
import socket
import time
import datetime
from string import capwords

#from Functions.serving import detectobjects

i=0

from lib.Videowriter import writevideo
from lib.util import util
from Functions.serving import detectobjects
from lib.log_database import database_function
from Functions.tracker import objecttracker

'''try:
    #from VehicleDetection import vehdet
    from lib.Videowriter import writevideo
    from lib.util import util
    from Functions.serving import detectobjects
    from lib.log_database import database_function
    from Functions.tracker import objecttracker
except:
    #from ..VehicleDetection import vehdet
    from ..lib.Videowriter import writevideo
    from ..lib.util import util
    from ..Functions.serving import detectobjects
    from ..Functions.tracker import objecttracker'''

#threadID, Functionid, name,source,JobName,Jobid,outpath, port_number, SourceID


class myvideoThread (threading.Thread):
	def __init__(self,Threadid, Jobid, JobName, sub_source_name,sub_source_path, model_id, list_lables, Functiontype, source_id, sub_source_id, outpath, port_number):
		print("yyvideothread")
		threading.Thread.__init__(self)
		print("ÿÿess")
		self.threadID = Threadid
		self.streamurl='tcp://*:'+str(port_number) 
		self.sender = imagezmq.ImageSender(connect_to=self.streamurl, REQ_REP=False)
		print(self.streamurl)
		self.name = sub_source_name
		self.folderpath =sub_source_path
		self.ln=database_function()
		self.labelname=list_lables
		print(self.labelname)
		self.function_type=Functiontype
		print(self.labelname, self.function_type)
		self.sub_source_paths=[]
		self.WV=writevideo()
		self.JobName=JobName
		self.Jobid=Jobid
		self.processed_video_id=0
		self.source_type="Video"
		self.sub_source_id=sub_source_id
		self.source_id=source_id
		self.model_id=model_id
		self.outpath=outpath
		self.util=util()
		self.database_function=database_function()
		self.detectionid=0
		JOBStoragepath=os.path.join(outpath,self.JobName+"_"+str(self.Jobid))
		self.hostname=self.JobName+"_"+str(self.Jobid) 
		self.videooutpath=os.path.join(JOBStoragepath,self.name)
		print("videopath=======",self.videooutpath)
		self.util.createdir(self.videooutpath)
		self.size = (800, 800)
		self.det=detectobjects()
		self.ot=objecttracker()


	def vehdet(self):
		print("labelname==============================================", self.labelname)
		print("labelname=",self.labelname)
		rundetection=True
		print(self.folderpath)
		print("timer startsssss")
		if rundetection==True:
			if len(os.listdir(self.folderpath)) == 0:
				print("Directory is empty")
			else:
				print("Directory is not empty")
				files=os.listdir(self.folderpath)
				print(files)
				for filename in files :
 					print("---",filename)
 					filename_split=filename.split('.')[0]
 					print("fs",filename_split)					
 					if filename.split('.')[-1]=='mp4':
 						xfname=os.path.join(self.folderpath,filename.split('.')[0]+'.xml')
 						print(xfname)
 						if os.path.exists(xfname)==True:
 							labelid_startvalue=0
 							framecount=0
 							capture=None
 							print(filename)
 							fourcc = cv2.VideoWriter_fourcc(*"vp80")
 							print("fourcc")
 							#out = cv2.VideoWriter("../file.webm", fourcc, 10,(frame_width, frame_height))
 							filenameresult=os.path.join(self.videooutpath, filename_split +'.webm')
 							try:
 								result = cv2.VideoWriter(filenameresult,fourcc , 10, (800,800))
 							except Exception as e:
 								print("resulttttt", e)
 							cap_path=os.path.join(self.folderpath,filename)
 							capture =cv2.VideoCapture(cap_path)
 							totalframes=int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
 							colors = [tuple(255 * np.random.rand(3)) for i in range(7)]
 							while (capture.isOpened()):
 								stime=time.time()
 								ret, frame = capture.read()
 								if frame is not None:
 									framecount+=1
 									start=time.time()					
 									retclasses,retboxes,retscores, retmodel_label_ids= self.det.object_detection_functionnew(frame,self.model_id)
 									#retboxes,retclasses,trackerids,retscores=self.ot.trackingobjects(frame,retboxes,retclasses,retscores)
#add match function

 									#print(retclasses,retboxes,retscores, retmodel_label_ids)
 									#frame=cv2.putText(frame,"Frame"+str(framecount) , (w-100, h+30), cv2.FONT_HERSHEY_TRIPLEX,0.5,(200, 200, 200), 1)
 									print('boxes',retboxes)
 									if len(retboxes)>0:
 										for retclas,bx,retscore,retmodel_label_id in zip(retclasses,retboxes,retscores, retmodel_label_ids):
	 										print(retclas,bx,retscore,retmodel_label_id)
	 										ymin,xmin,ymax,xmax=bx
	 										print("retclas",retclas)  

	 											

											#detectionid=get_log_row_count()
	 										self.detectionid=self.ln.get_log_row_count()+1
	 										self.processed_video_id=self.ln.get_log_row_count_processed_video()+1
											 
	 										print(self.detectionid)
	 										functiontype=self.function_type # "detection"
	 										print("=====================",functiontype)

	 										model_label_id=int(retmodel_label_id)
	 										print(model_label_id)
	 										
	 										objectid=1
	 										current_date = datetime.datetime.now()
	 										timestamp = current_date.strftime("%Y-%m-%d %H:%M:%S")
	 										#timestamp='2016-06-22 19:10:25-07' 
	 										print(timestamp)
	 										classname=retclas
	 										print("beforeeeeeeeeeeee",classname)
	 										#classname=classname.capitalize()
	 										print("afterrrrrrrr",classname)
	 										print("retscoreeee=====================",retscore)
	 										coordinates=str(bx) 
	 										accuracy=round(retscore,2)
	 										print("retscoreeee=====================",accuracy)
	 										accuracy=retscore*100
	 										accuracy=round(accuracy)
	 										retscore=int(accuracy)

	 										print("accccccccccccccccccccc", retscore)
	 										sub_souce_name=self.name
	 										jobid=self.Jobid #1232334 
	 										sourceid=self.source_id #453465
	 										sub_sourceid=self.sub_source_id #453465
	 										if classname in self.labelname:
	 											frame=cv2.putText(frame,classname, (xmin, ymin-5), cv2.FONT_HERSHEY_TRIPLEX,1,(255, 255, 255),1)
	 											frame=cv2.rectangle(frame, (xmin,ymin),(xmax,ymax),(0, 255, 0) ,5)
	 											labelname=classname
	 											labelname="'%s'" % classname
	 											classid= self.ln.get_label_id(labelname)  
	 											print("--------------------------",classid)

	 											print("passsssssssssssssssssssssssssss")
	 											print(self.detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid, sourceid, sub_sourceid, sub_souce_name, retscore, model_label_id)
	 											self.database_function.log_entry(self.detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid, sourceid, sub_sourceid, sub_souce_name, retscore, model_label_id)
	 											print(self.detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid, sourceid, sub_sourceid, sub_souce_name, retscore, model_label_id)
	 										else:
	 											print("faiedddddddddddddddddddd")
                                                    
 									frameresized=cv2.resize(frame,(800,800)) 									
 									#result.write(frameresized)

 									self.sender.send_image(self.hostname, frameresized)
										#cv2.imshow('RSRV Automation -' +filename, frame)
 									cv2.waitKey(1)
 									print("hry")
 									print('FPS {:.1f}'.format(1 / (time.time() - stime)))
 									if cv2.waitKey(1) & 0xFF == ord('q'):
 										break
 								else:
	 								capture.release()
    
	 								cv2.destroyAllWindows()
	 								break
    
 							capture.release()
 							#result.release() 
 							#filename_video=filename.split('.')[0]+".webM"
 							filename_video=filename_split+".webM"
 							videopath=os.path.join(self.videooutpath, filename_video)
 							self.database_function.processed_video_entry(self.processed_video_id, filename, timestamp, videopath, jobid, self.source_type, sub_sourceid)

 							self.processed_video_id= self.processed_video_id+1	

								
 						else:
    
 							print("XML Schema file is missing for "+filename)	

 					
    		#xmlgen.process_intermediate()
			cv2.destroyAllWindows()




	#vehdet()

