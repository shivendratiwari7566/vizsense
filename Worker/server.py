import cv2
import imagezmq
image_hub = imagezmq.ImageHub(open_port='tcp://192.168.0.105:5555', REQ_REP=False)

#image_hub.connect('tcp://192.168.0.105:5553')
#image_hub.connect('tcp://192.168.0.105:5554')
#worker_streams=['tcp://192.168.32.1:5553','tcp://192.168.32.1:5554']
#worker_streams=['tcp://master-node:5553','tcp://master-node:5554']
#worker_streams=['tcp://master-node:5553','tcp://master-node:5554']
worker_streams=['tcp://master-node:5553','tcp://master-node:5554']





for workerstream in worker_streams:
	image_hub.connect(workerstream)

while True:
  Framedetails, image = image_hub.recv_image()
  cv2.imshow(Framedetails, image) # 1 window for each RPi
  cv2.waitKey(1)
