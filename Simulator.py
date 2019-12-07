import numpy as np
import cv2
import sys
import Image_Processing as IP
import Coloring as C
import Coloring_2 as C2

def path_length(path,c_c_t):
    time=0
    for action in path:
        if action[0]=='R' or action[0]=='Y' or action[0]=='B':
            time+=c_c_t
        else:
            time+=int(''.join(action[4:len(action)]))
    return time

def draw(img,img_colored,torque,period,color_change_time):
    #cv2.imshow("adsf",img)
    img_c,img_c_c,img_c_f=IP.Image_Process_data(img,img_colored)
    image_set=[img_c,img_c_c,img_c_f]
    path_1=C.coloring(image_set,torque,period)
    path_2=C2.coloring(image_set,torque,period)
    path_1_time=path_length(path_1,color_change_time)
    path_2_time=path_length(path_2,color_change_time)
    if (path_1_time>path_2_time):
        print('path_2')
        return path_2
    else:
        print('path_1')
        return path_1


if __name__=="__main__":
    img=cv2.imread("test_7.jpeg")
    img_colored=cv2.imread("test_7_colored.jpeg")
    path=draw(img,img_colored,'050',100,100)
