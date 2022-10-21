import time

from Functions.log_database import database_function
from os import listdir
from os.path import isfile, join
import os
from PIL import Image
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import cv2
import os
import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    
import tensorflow as tf
tf.compat.v1.enable_eager_execution()
tf.get_logger().setLevel('ERROR') 
import time
from Functions.object_detection.utils import label_map_util
from Functions.object_detection.utils import visualization_utils as viz_utils          

gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
    

class detectobjects():
    def __init__(self):
        self.score_threshold=.5		
        self.ln=database_function()
        export_dir = '/usr/src/app/Worker/Functions'
        self.PATH_TO_LABELS = '/usr/src/app/Worker/Functions/mscoco_label_map.pbtxt'
        self.model = tf.compat.v2.saved_model.load(export_dir , tags=None)
        self.detect_fn = self.model.signatures['serving_default']  
        print("heyyyyinit")

    def object_detection_functionnew(self,image,model_id):
        #export_dir = '/usr/src/app/Worker/Functions'
        #PATH_TO_LABELS = '/usr/src/app/Worker/Functions/mscoco_label_map.pbtxt'
        retclasses=[]
        retboxes=[]
        retscores=[]
        retmodel_label_ids=[]
        category_index = label_map_util.create_category_index_from_labelmap(self.PATH_TO_LABELS,use_display_name=True)
        h,w,c=image.shape
        start=time.time()
        input_tensor = tf.convert_to_tensor(image)            
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = self.detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        key_of_interest = ['detection_classes', 'detection_boxes', 'detection_scores']
        detections = {key: value for key, value in detections.items() if key in key_of_interest}

        boxes =  detections['detection_boxes']   
        scores = detections['detection_scores']
        classes = detections['detection_classes']     

        end=time.time()

        print("TIME FOR EACH FRAME= ", end-start)

        for box,score,cls in zip(boxes,scores,classes):
            #print(box,score,cls)
            if score>self.score_threshold:
                ymin,xmin,ymax,xmax=box
                print("heeeeeeeeeee")
                xmin=int(xmin*w)
                ymin=int(ymin*h)
                xmax=int(xmax*w)
                ymax=int(ymax*h) 
                model_label_id=cls
                print("model_labellllllllllllllllll", model_label_id, model_id)
                classname=self.ln.get_label_name_model(model_label_id, model_id)
                print("clsn",cls, )
                retmodel_label_ids.append(model_label_id)
                retclasses.append(classname)
                retboxes.append([ymin,xmin,ymax,xmax])
                retscores.append(score)
            #print("rrr",retclasses,retboxes,retscores, retmodel_label_ids)
        print("rettttttt", retclasses,retboxes,retscores, retmodel_label_ids)
        return retclasses,retboxes,retscores, retmodel_label_ids



