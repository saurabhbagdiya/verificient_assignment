import imutils
import cv2
import numpy as np
import uuid
from tqdm import tqdm
import os
from angle import get_orientation
import copy
import glob
from config import *


class detect_card:
	def __init__(self,Image_Path=None,Directory_Path=None):
		self.Image_Path=Image_Path
		self.Directory_Path=Directory_Path
		self.job_id=str(uuid.uuid4())[0:4]
		self.net=self.load_model()
		self.output_dir='./output_result/'

	def load_model(self):
		try:
			net = cv2.dnn.readNetFromTensorflow(tensorflow_pb, tensorflow_pbtxt)
		except Exception as e:
			print(e)
			return
		return net


	def draw_bounding_box(self,img,angle,box):
		#(240,90,100)
		cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(20,190,100),2)

		# overlay=img.copy()
		# output=img.copy()
		# cv2.rectangle(overlay, (box[0],box[1]), (180, 21),(128, 255, 128), -1)
		# cv2.addWeighted(overlay, 0.6, output, 1 - 0.6,0, output)

		# img=output.copy()
		label = "Angle>> " +str(angle)+" degree"
		labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
		cv2.rectangle(img, (box[0], box[1] - labelSize[1]),
						(box[0] + labelSize[0], box[1] + baseLine),
					(255, 255, 255), cv2.FILLED)
		cv2.putText(img,label ,(box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 0, 0))
		return img

	def forward_pass(self,img):
		rows = img.shape[0]
		cols = img.shape[1]
		self.net.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
		Out = self.net.forward()
		for detection in Out[0,0,:,:]:
			score = float(detection[2])
			if score > 0.4:
				left = int(detection[3] * cols)
				top = int(detection[4] * rows)
				right = int(detection[5] * cols)
				bottom = int(detection[6] * rows)
				angle,pt1,pt2=get_orientation(img[top:bottom,left:right])
				img=self.draw_bounding_box(img,angle,[left,top,right,bottom])

		return img


	def get_cards(self):
		if not os.path.exists(self.output_dir):
			os.makedirs(self.output_dir)

		if self.Image_Path:
			try:
				img=cv2.imread(self.Image_Path)
				if img.shape[-1]:
					processed_img=self.forward_pass(img)
					cv2.imwrite(self.output_dir+self.Image_Path.split('/')[-1].split('.')[0] \
						+'_'+self.job_id+'.jpg',processed_img)
				else:
					raise Exception('Image is None!!')
			except Exception as e:
				print('!!!!!something went wrong!!!!!')
				print(e)
		
		if self.Directory_Path:
			if self.Directory_Path[-1]=='/':
				images=glob.glob(self.Directory_Path+'*')
			else:
				raise Exception('Please Enter Directory_Path Ending with:/ ')

			if len(images)==0:
				raise Exception('Directory does not contain any images')

			for file in tqdm(images):
				try:
					img=cv2.imread(file)
					if img.shape[-1]:
						processed_img=self.forward_pass(img)
						cv2.imwrite(self.output_dir+file.split('/')[-1].split('.')[0] \
						      	 +'_'+self.job_id+'.jpg',processed_img)
					else:
						raise Exception('Image is None!!')
				except Exception as e:
					print('!!!!!something went wrong!!!!')
					print(e)







