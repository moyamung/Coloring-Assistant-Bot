import numpy as np
import cv2
import sys
import math
import Utility as Util
import Image_Processing as IP

def making_path(image_map,image_top,image_bottom):
    now_pen=''
    pen_list=['','B','Y','R']
    x=0
    y=0
    ans=[]
    while(x<image_map.shape[0]):
        if (image_top[x]==image_map.shape[1]+1):
            ans.append('right')
            x+=1
            continue
        image_middle=image_top[x]+image_bottom[x]
        image_middle=int(image_middle/2)
        if (y<image_top[x]):
            for i in range(image_top[x]-y):
                ans.append('down')
            y=image_top[x]
        elif (y<=image_middle):
            for i in range(y-image_top[x]):
                ans.append('up')
            y=image_top[x]
        elif (y<image_bottom[x]):
            for i in range(image_bottom[x]-y):
                ans.append('down')
            y=image_bottom[x]
        elif (y>image_bottom[x]):
            for i in range(y-image_bottom[x]):
                ans.append('up')
            y=image_bottom[x]
        if (y==image_bottom[x]):
            while(y>=image_top[x]):
                if (now_pen!=pen_list[image_map[x][y]]):
                    if (now_pen==''):
                        now_pen=pen_list[image_map[x][y]]
                        ans.append(now_pen+'D')
                    else:
                        ans.append(now_pen+'U')
                        now_pen=pen_list[image_map[x][y]]
                        if (now_pen!=''):
                            ans.append(now_pen+'D')
                ans.append('up')
                y=y-1
        if (y==image_top[x]):
            while(y<=image_bottom[x]):
                if (now_pen!=pen_list[image_map[x][y]]):
                    if (now_pen==''):
                        now_pen=pen_list[image_map[x][y]]
                        #print(now_pen+'pen')
                        ans.append(now_pen+'D')
                    else:
                        ans.append(now_pen+'U')
                        now_pen=pen_list[image_map[x][y]]
                        if (now_pen!=''):
                            ans.append(now_pen+'D')
                ans.append('down')
                y=y+1
        if (now_pen!=''):
            ans.append(now_pen+'U')
            now_pen=''
        ans.append('right')
        x=x+1
    return ans
                
def draw_image(img,path):
    x=0
    y=0
    k=0
    img_cp=img.copy()
    now_pen=''
    pen_list=['','B','Y','R']
    for action in path:
        if (now_pen==''):
            img_cp[y,x]=[0,0,0]
        if (now_pen=='B'):
            img_cp[y,x]=[255,0,0]
        if (now_pen=='Y'):
            img_cp[y,x]=[0,255,0]
        if (now_pen=='R'):
            img_cp[y,x]=[0,0,255]
        if (action=='up'):
            y=y-1
        if (action=='down'):
            y=y+1
        if (action=='right'):
            x=x+1
        if (action=='left'):
            x=x-1
        #try:
        if (action[1]=='U'):
            now_pen=''
        #except IndexError:
#            print(action)
#        try:
        if (action[1]=='D'):
            now_pen=action[0]
            #print(now_pen)
#        except IndexError:
#            print('dd')
        #cv2.imwrite('./image/'+str(k)+'.jpg',img_cp)
        k=k+1
        if (k%400==0):
            print(k)
    return img_cp

def draw_image_dense(img,path):
    x=0
    y=0
    k=0
    img_cp=img.copy()
    now_pen=''
    pen_list=['','B','Y','R']
    for action in path:
        if (now_pen==''):
            img_cp[y,x]=[0,0,0]
        if (now_pen=='B'):
            img_cp[y,x]=[255,0,0]
        if (now_pen=='Y'):
            img_cp[y,x]=[0,255,0]
        if (now_pen=='R'):
            img_cp[y,x]=[0,0,255]
        if (action[0]=='up'):
            y=y-action[1]
        if (action[0]=='down'):
            y=y+action[1]
        if (action[0]=='right'):
            x=x+action[1]
        if (action[0]=='left'):
            x=x-action[1]
        #try:
        if (action[0][1]=='U'):
            now_pen=''
        #except IndexError:
#            print(action)
#        try:
        if (action[0][1]=='D'):
            now_pen=action[0][0]
            #print(now_pen)
#        except IndexError:
#            print('dd')
        #cv2.imwrite('./image/'+str(k)+'.jpg',img_cp)
        k=k+1
        if (k%400==0):
            print(k)
    return img_cp

def path_condense(path):
    ans=[]
    state=''
    cnt=0
    for action in path:
        if (action!=state):
            ans.append((state,cnt))
            state=action
            cnt=1
        else:
            cnt=cnt+1
    del ans[0]
    return ans

def path_numbering(path,torque,period):
    ans=[]
    for action in path:
        act=''
        if (action[0][0]=='B' or action[0][0]=='Y' or action[0][0]=='R'):
            ans.append(action[0])
            continue
        if (action[0]=='up'):
            act='1'
        if (action[0]=='down'):
            act='3'
        if (action[0]=='right'):
            act='4'
        if (action[0]=='left'):
            act='2'
        act=act+torque
        time=period*action[1]
        act=act+str(time)
        ans.append(act)
    return ans

def coloring(image_set,torque,period):
    if len(image_set)==2:
        img,img_colored=image_set
        img_c,img_c_c,img_c_f=IP.Image_Process_data(img,img_colored)
    elif len(image_set)==3:
        img_c,img_c_c,img_c_f=image_set
    #img_c=cv2.resize(img_c,((99,70)),interpolation=cv2.INTER_AREA)
    #img_c_f=cv2.resize(img_c_f,((99,70)),interpolation=cv2.INTER_AREA)
    image_map=np.zeros((img_c.shape[1],img_c.shape[0]),np.int32)
    image_left=np.full((img_c.shape[1]),img_c.shape[0]+1)
    image_right=np.full((img_c.shape[1]),-1)
    for y in range(image_map.shape[1]):
        for x in range(image_map.shape[0]):
            now_pixel=img_c_f[y,x]
            if (np.all(now_pixel==[255,0,0])):
                image_map[x,y]=1
                if (y<image_left[x]):
                    image_left[x]=y
                if (y>image_right[x]):
                    image_right[x]=y
            if (np.all(now_pixel==[0,255,0])):
                image_map[x,y]=2
                if (y<image_left[x]):
                    image_left[x]=y
                if (y>image_right[x]):
                    image_right[x]=y
            if (np.all(now_pixel==[0,0,255])):                                                                                              
                image_map[x,y]=3
                if (y<image_left[x]):
                    image_left[x]=y
                if (y>image_right[x]):
                    image_right[x]=y
    path=making_path(image_map,image_left,image_right)
    #img_cp=draw_image(img_c,path)
    path=path_condense(path)
    path=path_numbering(path,torque,period)
    #img_cp=draw_image_dense(img_c,path)
    #cv2.imshow('asdfs',img_cp)
    return path
    
                



if __name__=="__main__":
    img=cv2.imread("test_7.jpeg")
    img_colored=cv2.imread("test_7_colored.jpeg")
    path=coloring([img,img_colored],'050',100)
    for i in range(20):
        print(path[i])
 
