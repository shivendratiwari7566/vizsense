import threading
import time
import cv2
import numpy as np
import os
import imagezmq
import socket
import time
import datetime
import shutil
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


class myliveThread (threading.Thread):
	def __init__(self,Threadid, Jobid, JobName, rtsp_url, model_id, list_lables, Functiontype, camera_name, camera_id, source_id, outpath, port_number):
		print("yyvideothread")
		threading.Thread.__init__(self)
		print("ÿÿess")
		self.threadID = Threadid
		self.streamurl='tcp://*:'+str(port_number) 
		#self.sender = imagezmq.ImageSender(connect_to=self.streamurl, REQ_REP=False)
		print(self.streamurl)
		self.name = camera_name
		self.rtsp_url =rtsp_url
		self.ln=database_function()
		self.labelname=list_lables
		print(self.labelname)
		self.function_type=Functiontype
		print(self.labelname, self.function_type)
		self.WV=writevideo()
		self.JobName=JobName
		self.Jobid=Jobid
		self.processed_video_id=0
		self.source_type="Live"
		self.camera_id=camera_id
		self.source_id=source_id
		self.model_id=model_id
		self.outpath=outpath
		self.util=util()
		self.database_function=database_function()
		self.detectionid=0
		JOBStoragepath=os.path.join(outpath,self.JobName+"_"+str(self.Jobid))
		self.hostname=self.JobName+"_"+str(self.Jobid) 
		self.liveoutpath=os.path.join(JOBStoragepath,self.name)
		print("liveoutpath=======",self.liveoutpath)

		self.directoryone = "history"
		self.directorytwo = "live"
		self.history = os.path.join(self.liveoutpath, self.directoryone)
		self.live = os.path.join(self.liveoutpath, self.directorytwo)
		if not os.path.exists(self.history ):
			os.makedirs(self.history)
		if not os.path.exists(self.live ):
			os.makedirs(self.live)

		self.util.createdir(self.liveoutpath)
		self.size = (800, 800)
		self.det=detectobjects()
		self.ot=objecttracker()


	def vehdet(self):
		print("labelname==============================================", self.labelname)
		print("labelname=",self.labelname)

		rundetection=True
		print("timer startsssss")
		if rundetection==True:
			labelid_startvalue=0
			framecount=0
			capture=None
			cap_url = self.rtsp_url
			print(cap_url)
			capture = cv2.VideoCapture(cap_url)
			count = 0
			colors = [tuple(0xFF * np.random.rand(3)) for i in range(7)]
			capture =cv2.VideoCapture(cap_url)
			colors = [tuple(255 * np.random.rand(3)) for i in range(7)]
			current_date = datetime.datetime.now()
			vid_timestamp = current_date.strftime('%Y%m%d%H%M%S')
			while (capture.isOpened()):
				stime=time.time()
				ret, frame = capture.read()
				if frame is not None:
					framecount+=1
					start=time.time()					
					retclasses,retboxes,retscores, retmodel_label_ids= self.det.object_detection_functionnew(frame,self.model_id)
					#retboxes,retclasses,trackerids,retscores=self.ot.trackingobjects(frame,retboxes,retclasses					print('boxes',retboxes)
					if len(retboxes)>0:
						for retclas,bx,retscore,retmodel_label_id in zip(retclasses,retboxes,retscores, retmodel_label_ids):
							print(retclas,bx,retscore,retmodel_label_id)
							ymin,xmin,ymax,xmax=bx
							print("retclas",retclas)  
							#detectionid=get_log_row_count()
							self.detectionid= self.ln.get_log_row_count()+1
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
							filename=vid_timestamp+".webM"
							totalframes=1000
							
							sub_sourceid=self.camera_id
							sub_souce_name=self.name
							print("accccccccccccccccccccc", retscore)
							camera_name=self.name
							jobid=self.Jobid #1232334 
							sourceid=self.source_id #453465
							cameraid=self.camera_id #453465
							if classname in self.labelname:
								print("clsss", classname, self.labelname)
								frame=cv2.putText(frame,classname, (xmin, ymin-5), cv2.FONT_HERSHEY_TRIPLEX,1,(255, 255, 255),1)
								frame=cv2.rectangle(frame, (xmin,ymin),(xmax,ymax),(0, 255, 0) ,5)
								labelname=classname
								labelname="'%s'" % classname
								print("hey")
								classid= 12341234  #self.ln.get_label_id(labelname)  
								print("--------------------------",classid)

								print("passsssssssssssssssssssssssssss")
								print(self.detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid, sourceid, sub_sourceid, sub_souce_name, retscore, model_label_id)
								self.database_function.log_entry(self.detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid, sourceid, sub_sourceid, sub_souce_name, retscore, model_label_id)
								print(self.detectionid, functiontype, objectid, filename, framecount, totalframes, classid, classname, coordinates, timestamp, jobid, sourceid, sub_sourceid, sub_souce_name, retscore, model_label_id)
							else:
								print("faiedddddddddddddddddddd")


					print("vid_save")
					dirname=self.liveoutpath	
					if count <=1440:
						name = str(count)+".jpg"
						img_fname=os.path.join(self.history,name)
						print(img_fname)
						cv2.imwrite(img_fname, frame)
						count += 1			
					else:
						src_path = self.history
						src_path_delete = self.history
						print("elsepartttt")
						os.chdir(src_path)
						cmd = 'ffmpeg -framerate 25 -f image2 -i "%d.jpg" -c:v libvpx-vp9 -pix_fmt yuva420p ' + str(vid_timestamp) + '.webM'
						os.system(cmd)
						src_path = os.path.join(src_path, str(vid_timestamp) + '.webM')
						filename=str(vid_timestamp) + '.webM'

						print(src_path)
						dst_path = os.path.join(self.live, 'live.webM')
						print(dst_path)
						shutil.copy(src_path, dst_path)
						current_date = datetime.datetime.now()
						vid_timestamp = current_date.strftime('%Y%m%d%H%M%S')
						for f in os.listdir(src_path_delete):
						    if not f.endswith('.jpg'):
						        continue
						    os.remove(os.path.join(src_path_delete, f))
						count = 0
						name = str(count) + '.jpg'
						cv2.imwrite(os.path.join(self.history, name), frame)
						count += 1
						cv2.waitKey(1)
						print ('FPS {:.1f}'.format(1 / (time.time() - stime)))
						sub_sourceid=self.camera_id
						videopath=os.path.join(self.history, filename)
						self.database_function.processed_video_entry(self.processed_video_id, filename, timestamp, videopath, jobid, self.source_type, sub_sourceid)

					if cv2.waitKey(1) & 0xFF == ord('q'):
						break

			capture.release()
			cv2.destroyAllWindows()

		else:

		    # result.release()
		    # filename_video=filename.split('.')[0]+".webM"
		    # filename_video=filename_split+".webM"
		    # videopath=os.path.join(self.videooutpath, filename_video)
		    #self.database_function.processed_video_entry(self.processed_video_id, filename, timestamp, videopath, jobid, self.source_type, sub_sourceid)

		    # self.processed_video_id= self.processed_video_id+1....

		    print ('process failed')


