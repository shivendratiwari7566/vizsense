import tensorflow as tf
import tensorflow.contrib.tensorrt as trt
import numpy as np
import cv2
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import shutil
import json
import pandas as pd

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from imutils.video import VideoStream
#from Functions.object_detection.utils import label_map_util		 
from IPython.display import Image as DisplayImage
from shapely.geometry import Polygon



class objecttracker():
	def __init__(self):
		self.tracking_classes=[]
		self.tracking_boxes=[]
		self.threshold=0.55
		#self.trackers = cv2.MultiTracker_create()
		self.trackerlist=[]
		self.trackerid=1	
		self.usetracker=False #False
		self.iou_thresh=0.70 # BAsed on this acceptable range for overlapping of boxes are decided
		self.trackingagelimit = 50  # Tracker will only track object for limit mentioned here	



	def Addto_trackerlist(self,frame,box,classname,retscore,trackingage):
		# extract the OpenCV version info
		(major, minor) = cv2.__version__.split(".")[:2]
		tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
		tracker_type = tracker_types[5]

		if int(major) == 3 and int(minor) < 3:
   			tracker = cv2.Tracker_create(tracker_type)

		# otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
		# approrpiate object tracker constructor:
		else:
			# initialize a dictionary that maps strings to their corresponding
			# OpenCV object tracker implementations
			OPENCV_OBJECT_TRACKERS = {
				"csrt": cv2.TrackerCSRT_create,
				"kcf": cv2.TrackerKCF_create,
				"boosting": cv2.TrackerBoosting_create,
				"mil": cv2.TrackerMIL_create,
				"tld": cv2.TrackerTLD_create,
				"medianflow": cv2.TrackerMedianFlow_create,
				"mosse": cv2.TrackerMOSSE_create
			}

			# grab the appropriate object tracker using our dictionary of
			# OpenCV object tracker objects
			tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
		height,width,channel=frame.shape
		xmin,ymin,w,h=int(round(box[0])),int(round(box[1])),int(round(box[2])),int(round(box[3]))
		if box[0]>0 and box[1]>0 and box[2]>0 and box[3]>0 and ymin >5 :
			try:
				tracker.init(frame, tuple(box))
				trkdata={"classname":classname,"track":tracker,"trackid":self.trackerid,"retscore":retscore,"trackingage":trackingage}
				self.trackerlist.append(trkdata)
				self.trackerid+=1

			except Exception as e:
				print("Error in ",box,frame)

		


	def gettrackinglabels(self,frame):
		height,width,channel=frame.shape
		classes=[]
		boxes=[]
		trackerids=[]
		retscores=[]
		j=0
		dellist=[]	
		height,width,channel=frame.shape
		newtracklist=[]
		print("trackerrrr",self.trackerlist)
		for tracker in self.trackerlist:
			trackerobj=tracker["track"]
			classname=tracker["classname"]
			trackid=tracker["trackid"]
			retscore=tracker["retscore"]
			trackingage=int(tracker["trackingage"])
			(success, box)=trackerobj.update(frame)
			print('box from tracker',box)
			xmin,ymin,w,h=int(round(box[0])),int(round(box[1])),int(round(box[2])),int(round(box[3]))
			if ((w/width) <= 0.5 and (h/height) <= 0.5) or (xmin > 40 and ymin>40) or (xmin+w) < (width-10) and (ymin+h) < (height-10) :
				print('tracking age',trackingage)
				if w>0 and h >0  and  xmin >0 and ymin > 0 and trackingage <= self.trackingagelimit :
					tbox=[xmin,ymin,w,h]
					print('tbox',tbox)
					ymax=ymin+h
					xmax=xmin+w
					overlap=self.is_overlap(tbox,boxes)
					if overlap==True:
						dellist.append(j)
					else:	
						ymin=ymin*h
						xmin=xmin*w
						ymax=ymax*h
						xmax=xmax*w				
						boxes.append([int(ymin),int(xmin),int(ymax),int(xmax)])			
						classes.append(classname)
						trackerids.append(trackid)
						retscores.append(retscore)
						newtracklist.append(tracker)
				else:
					print("Not Deleting")
					dellist.append(j)
			else:
				print("Not Deleting")
				dellist.append(j)
			j+=1

		#print("newtrackerlist",newtrackerlist)
		self.trackerlist=newtracklist
		print("from gettracking labels",len(boxes),len(self.trackerlist))
		self.tracking_classes=classes	
		return boxes,classes,trackerids,retscores


		
	def is_overlap(self,tbox,boxes):
		#Delete boxes that are overlapping
		overlap=False
		for dbox in boxes:
			print('check overlap tbox',tbox)
			print('check overlap dbox',dbox)
			iou=self.calculate_iou(tbox,dbox)
			if iou > self.iou_thresh:
				overlap=True
				break	

		return overlap	


	def update_trackingage(self):
		tracklistnew=[]	
		for tracker in self.trackerlist:
			tracker['trackingage']+=1
			tracklistnew.append(tracker)
		self.trackerlist=tracklistnew
		

	def trackingobjects(self,frame,nboxes,nclasses,retscores):
		self.update_trackingage() # To update the age of the tracking objects	
		height,width,channel=frame.shape
		#Track Objects and create bounding box		
		print("INPUT to trackingob", frame,nboxes,nclasses,retscores)
		tboxes,classes,trackerids,retscores = self.gettrackinglabels(frame)
		print("tboxes and labels!!!!",tboxes,classes)
		# loop over the bounding boxes and draw then on the frame
		if len(nboxes) > 0:	
			if len(tboxes) == 0:
				for box,classname,retscore in zip(nboxes,nclasses,retscores):			
					ymin,xmin,ymax,xmax=int(box[0]),int(box[1]),int(box[2]),int(box[3])
					box1=[xmin,ymin,(xmax-xmin),(ymax-ymin)]  #(x,y,w,h)
					trackingage=1
					self.Addto_trackerlist(frame,box1,classname,retscore,trackingage)							
				self.tracking_classes=nclasses

			else:
				i=0  
				for dbox,classname,retscore in zip(nboxes,nclasses,retscores):
					#ymin,xmin,ymax,xmax=int(box[0]),int(box[1]),int(box[2]),int(box[3])
					AppendData=False
					j=0
					for tbox in tboxes:
						iou=self.calculate_iou(tbox,dbox)
						print("IOU Here",iou)
						if iou > self.iou_thresh:
							del self.trackerlist[j]							 
							AppendData=True
							break
						else:
							AppendData=True 
						j=j+1

					if AppendData==True:
						print("lassname in tracker",classname)
						#mainclassid=classname[1]
						ymin,xmin,ymax,xmax=int(dbox[0]),int(dbox[1]),int(dbox[2]),int(dbox[3])
						box=[int(xmin),int(ymin),int(xmax-xmin),int(ymax-ymin)] #(x,y,w,h)
                                                 
						trackingage=1
						self.Addto_trackerlist(frame,box,classname,retscore,trackingage)	

				
		tboxes,classes,trackerids,retscores = self.gettrackinglabels(frame)
		#print("count of tracking objects  boxes t",len(tboxes))
		print("tboxesclassestrackeridsretscores", tboxes,classes,trackerids,retscores)
		return tboxes,classes,trackerids,retscores





	def calculate_iou(self,tbox, dbox):
		#Tbox Input [x,y,w,h]
		#DTbox Input [ymin,xmin,ymax,xmax]

		print('input dbox',dbox)
		print('input tbox',tbox)

		#Detected box
		minx=dbox[1]
		miny=dbox[0]
		maxx=dbox[3]
		maxy=dbox[2]
	
		ptd1 =[minx,miny]
		ptd2=[maxx,miny]		
		ptd3=[maxx,maxy]
		ptd4=[minx,maxy]
		boxD=[ptd1,ptd2,ptd3,ptd4]
		print('Tracking box',tbox)

		#Tracking box 
		xmin,ymin,xmax,ymax=int(tbox[0]),int(tbox[1]),(int(tbox[0])+int(tbox[2])),(int(tbox[1]+int(tbox[3])))

		ptc1 =[xmin,ymin]
		ptc2=[xmax,ymin]		
		ptc3=[xmax,ymax]
		ptc4=[xmin,ymax]
		boxT=[ptc1,ptc2,ptc3,ptc4]
		print("boxD",boxD)
		print("boxT",boxT)
		poly_1 = Polygon(boxD)
		poly_2 = Polygon(boxT)
		iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
		print("iou",iou)		
		return iou
