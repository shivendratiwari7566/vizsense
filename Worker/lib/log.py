import pandas as pd
from Functions.utils import util
import datetime 
import os
from Functions.colordetection import ColorDetection
from Functions.frequency import frequence
from Functions.lighttypeclass import lightsclassify
from Functions.motion import car_in_motion
from Functions.srpred import pred_coord

class logdetails():
	def __init__(self):		
		self.PATH_TO_Clssconfig="./config/signnames.csv"
		self.ut=util()
		self.classesnames=self.ut.getpbtxt(self.PATH_TO_Clssconfig)
		#self.fullview_x=2048 
		#self.fullview_y= 1156 
		self.fullview_x=3996 #,3840 ,4096
		self.fullview_y= 2160 #1716
		self.wideview_x= 1664 
		self.wideview_y=640 
		self.farview_x=1280
		self.farview_y=640
		self.cd=ColorDetection()
		self.freq=frequence()
		self.ltclassify=lightsclassify()
		self.motion=car_in_motion()
		self.cordpred=pred_coord()	



	def create_new_log(self,Vfilename,basepath):
		self.filename=Vfilename
		filerootpath=os.path.join("./processed",basepath)
		if os.path.exists(filerootpath)==False:
			os.makedirs(filerootpath)			
		self.logfile=os.path.join(filerootpath,Vfilename.split("/")[-1].split(".")[0]+'.csv')
		print("logfilepath",self.logfile)
		self.df=pd.DataFrame(columns =['LabelId','filename','zonetime','FrameNo','Classid','TotalFrames','LabelName','Type','Light','LeftLight','RightLight','Motion','visibility','color','Arrow','Frequency','IsExclusion','UL_XP','UL_YP','UL_ZP','LR_XP','LR_YP','LR_ZP','LC_XP','LC_YP','LC_ZP','uUL_XP','uUL_YP','uUL_ZP','uLR_XP','uLR_YP','uLR_ZP','uLC_XP','uLC_YP','uLC_ZP'])

		self.wiiteblackthresh=50  #Threshold to idenify day and night frames

		
	def add_entry(self,frame,framecount,classid,boundingbox,labelid,totalframes):
		h,w,c=frame.shape
		#print(self.classesnames)
		classnmelist=self.classesnames[int(classid)]
		classnme=classnmelist[2]
		mainclassid=classnmelist[1]
		x1=boundingbox[1]
		y1=boundingbox[0]
		x2=boundingbox[3]
		y2=boundingbox[2]
		ztime=datetime.datetime.now().strftime("%s")
		box=[x1,y1,x2,y2]
		Type,Light,LeftLight,RightLight,Motion,visibility,color,Arrow,Frequency,IsExclusion=self.feature_extraction(frame,classid,box,labelid)

		newx1=(int(boundingbox[1])/w)*self.fullview_x
		newy1=(int(boundingbox[0])/h)*self.fullview_y
		newx2=(int(boundingbox[3])/w)*self.fullview_x
		newy2=(int(boundingbox[3])/w)*self.fullview_x
		w=newx2-newx1
		h=newy2-newy1

		#Commenting coordinate prediction for model
		#newx1=self.cordpred.predxp(newx1)	
		#newy1=self.cordpred.predyp(newy1)
		#newx2=newx1+w
		#newy2=newy1+h

		# Predict new x coordinates							

		UL_XP =newx1
		UL_YP =newy1
		UL_ZP =0

		LR_XP =newx2
		LR_YP =newy2
		LR_ZP =0

		LC_XP  =newx1
		LC_YP  =newy1
		LC_ZP  =0

		uUL_XP =newx1
		uUL_YP =newy1
		uUL_ZP =0

		uLR_XP =newx2
		uLR_YP =newy2
		uLR_ZP =0

		uLC_XP  =newx1
		uLC_YP  =newy1
		uLC_ZP  =0



		newdata={'LabelId':labelid ,'filename':self.filename,'zonetime':ztime,'FrameNo':str(framecount) ,'Classid':int(mainclassid),'LabelName':str(classnme),"TotalFrames":totalframes,"Type":Type,"LeftLight":LeftLight,"RightLight":RightLight,"Motion":Motion,"visibility":visibility,"color":color,"Arrow":Arrow,"Frequency":Frequency,"IsExclusion":IsExclusion,"UL_XP":UL_XP,"UL_YP":UL_YP,"UL_ZP":UL_ZP,"LR_XP":LR_XP,"LR_YP":LR_YP,"LR_ZP":LR_ZP,"uUL_XP":uUL_XP,"uUL_YP":uUL_YP,"uUL_ZP":uUL_ZP,"uLR_XP":uLR_XP,"uLR_YP":uLR_YP,"uLR_ZP":uLR_ZP}
		self.df=self.df.append(newdata,ignore_index=True)
		return newdata


	def feature_extraction(self,frame,subclassid,box,labelid):

		classnmelist=self.classesnames[int(subclassid)]
		classid=classnmelist[1]
		print("rinting Class Names list",classnmelist)
		[xmin,ymin,xmax,ymax]=box
		print("Printing box",box)	
		if int(classid)==1:

			Type=classnmelist[0]  #[Featurename,mainclassid,mainclassname]'motorcycle'

			#Light Type classification
			subframe=frame[ymin:ymax,xmin:xmax]
			label,cid=self.ltclassify.classifyLTComponents(subframe)
			Light=label   #'blinking_light'
			print("Light Type",label)		
			#Light Type classification Ends here

			LeftLight='NA'
			RightLight='NA'
			#Motion identification
			try:	
				self.motion.ROIContains(labelid,frame,box)
				id,movingstatus=self.motion.get_frequence_status(labelid)
				Motion=movingstatus
			except:
				Motion='uncertain'
			print("Motion VAlue",Motion)
			#Motion identification ends here

			visibility='clearly'
			color='NA'
			Arrow='NA'
			Frequency='NA'
			IsExclusion='NA'

		elif int(classid)==2:
			Type=classnmelist[0]
			Light='NA'

			#Light Type classification
			subframe=frame[ymin:ymax,xmin:xmax]
			label,cid=self.ltclassify.classifyLTComponents(subframe)
			Light=label   
			LeftLight=label#'brake_light'
			RightLight=label#'brake_light'
			#Light Type classification Ends here

			#Motion identification
			try:	
				self.motion.ROIContains(labelid,frame,box)
				id,movingstatus=self.motion.get_frequence_status(labelid)
				Motion=movingstatus
			except:
				Motion='uncertain'
			print("Motion VAlue",Motion)
			#Motion identification ends here

			visibility='clearly'
			color='NA'
			Arrow='NA'
			Frequency='NA'
			IsExclusion='NA'

		elif int(classid)==3:
			Type=classnmelist[0]
			Light='NA'
			LeftLight='NA'
			RightLight='NA'
			Motion='NA'
			visibility='clearly'
			try:
				color=self.cd.get_dominant_color(frame[ymin:ymax,xmin:xmax])#'white'
				print("Color Detected",color)
			except:
				color='white'
				
			Arrow='NA'
			Frequency='NA'
			IsExclusion='NA'

		elif int(classid)==4:
			Type='NA'
			Light='NA'
			LeftLight='NA'
			RightLight='NA'
			Motion='NA'
			visibility='clearly'
			try:
				color=self.cd.get_dominant_color(frame[ymin:ymax,xmin:xmax])#'white'
				print("Color Detected",color)
			except:
				color='white'
				
			Arrow='left'
			#Frequency calculation	
			try:
				self.freq.frequence_tracking(labelid, frame, box)
				Frequency=self.freq.get_frequence_status(labelid)  #'constant'
			except:
				Frequency='constant'
			IsExclusion='FALSE'

		elif int(classid)==5:
			Type=classnmelist[0]  #'cross'
			Light='NA'
			LeftLight='NA'
			RightLight='NA'
			Motion='NA'
			visibility='clearly'
			try:
				color=self.cd.get_dominant_color(frame[ymin:ymax,xmin:xmax])#'white'
				print("Color Detected",color)
			except:
				color='white'
				
			Arrow='NA'
			Frequency='NA'
			IsExclusion='NA'

		elif int(classid)==6:
			Type=classnmelist[0]  #'cross'
			Light='NA'
			LeftLight='NA'
			RightLight='NA'
			Motion='NA'
			visibility='clearly'
			try:
				color=self.cd.get_dominant_color(frame[ymin:ymax,xmin:xmax])#'white'
				print("Color Detected",color)
			except:
				color='white'
				
			print("Color Detected",color)
			Arrow='NA'
			Frequency='NA'
			IsExclusion='NA'


		return	Type,Light,LeftLight,RightLight,Motion,visibility,color,Arrow,Frequency,IsExclusion
		

	def save_to_file(self):		
		self.df.to_csv(self.logfile,index = False)
		del self.df

		
