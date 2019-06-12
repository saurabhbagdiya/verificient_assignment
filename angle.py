import cv2
import numpy as np
import math


def get_angle(a,b):
	rad=np.dot(a,b)/(np.linalg.norm(b)*np.linalg.norm(a))
	return math.degrees(math.acos(rad))



def get_orientation(patch):
    try:
        gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges,1,np.pi/180,70)[0:1]
        for line in lines:
            for rho,theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 500*(-b))
                y1 = int(y0 + 500*(a))
                x2 = int(x0 - 500*(-b))
                y2 = int(y0 - 500*(a))
                cv2.line(patch,(x1,y1),(x2,y2),(0,0,240),2)
        a=(patch.shape[1],0)
        b=(x2-x1,y2-y1)
        angle=get_angle(a,b)
    except:
        return ['NA',(0,0),(0,0)]
    return [int(angle),(x1,y1),(x2,y2)]


