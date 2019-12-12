import numpy as np
import cv2
import sys
import math
import Utility as Util
import queue

sys.setrecursionlimit(80000)

def Image_Detection(img):
    img_0=img.copy()
    
    #print(img.shape[0])
    #print(img.shape[1])

    k=720/img.shape[0]

    w=(int)(img.shape[1]*k)
    h=720
    
    #w=(int)(img.shape[1]/8)
    #h=(int)(img.shape[0]/8)
    
    dim=((int)(img.shape[1]/8),(int)(img.shape[0]/8))
    img=cv2.resize(img,dim,interpolation=cv2.INTER_AREA)

    img_0_small=img.copy()

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),0)
    edged=cv2.Canny(blur,50,130)

    #cv2.imshow("a",edged)
    cv2.imwrite('./process/edge.jpg',edged)

    (_,cnts,_)=cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(cnts)
    cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:5]
    #print(cnts)

    #img_0=img.copy()
    #cv2.drawContours(img_0,[cnts[1]],-1,(255,0,0),2)
    #cv2.imwrite('./process/drawContours.jpg',img_0)
    #cv2.imshow("c",img_0)


    for c in cnts:
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.03*peri,True)
        if (len(approx)==4):
            screenCnt=approx
            break

    cv2.drawContours(img,[screenCnt],-1,(0,255,0),2)
    cv2.imwrite('./process/draw.jpg',img)
    #cv2.imshow("b",img)

    def points(pts):
        rect=np.zeros((4,2),dtype="float32")

        s=np.sum(pts,axis=1)

        rect[0]=pts[np.argmin(s)]
        rect[2]=pts[np.argmax(s)]

        d=np.diff(pts,axis=1)

        rect[1]=pts[np.argmin(d)]
        rect[3]=pts[np.argmax(d)]

        return rect

    rect=points(screenCnt.reshape(4,2))
    (topLeft,topRight,bottomRight,bottomLeft)=rect
    w1=abs(bottomRight[0]-bottomLeft[0])
    w2=abs(topRight[0]-topLeft[0])
    h1=abs(topRight[1]-bottomRight[1])
    h2=abs(topLeft[1]-bottomLeft[1])
    width=max([w1,w2])
    height=max([h1,h2])

    new_cord=np.float32([[0,0],[width-1,0],[width-1,height-1],[0,height-1]])
    M=cv2.getPerspectiveTransform(rect,new_cord)
    image_crop=cv2.warpPerspective(img_0_small,M,(width,height))
    #cv2.imshow("d",image_crop)

    return image_crop

def on_mouse(event,y,x,flags,param):
    global clicked, click_point
    if (event==cv2.EVENT_LBUTTONDOWN):
        click_point=(x,y)
        clicked=1
        print(click_point)

#cv2.setMouseCallback("d",on_mouse)

'''
while(clicked==0):
    cv2.waitKey(30)
    if (clicked==1):
        break
'''

'''
print(image_crop.shape[0])
print(image_crop.shape[1])
'''

def is_blue(img,x,y):
    return (img[x,y][0]>200 and img[x,y][2]<150)

def is_red(img,x,y):
    return (img[x,y][1]<150 and img[x,y][2]>200)

def is_green(img,x,y):
    return (img[x,y][1]>200 and img[x,y][0]<100)

def is_black(img,x,y):
    return (img[x,y][0]<160 and img[x,y][1]<160 and img[x,y][2]<160)

#pixel=0
#a=np.zeros((300,300))

def pixel_simillar(a,b):
    #print(a)
    #print(b)
    return (abs(int(a[0])-int(b[0]))<10.0 and abs(int(a[1])-int(b[1]))<10.0 and abs(int(a[2])-int(b[2]))<10.0)

def floodfill(img,img_output,x,y,color,visit):
    global pixel
    if (a[x][y]==1):
        return
    w=img.shape[0]
    h=img.shape[1]
    #print(str(w)+" "+str(h))
    #cv2.imwrite('./image/'+str(pixel)+'.jpg',img_output)
    pixel+=1
    a[x][y]=1
    #print(img[x,y])
    if (x>0 and pixel_simillar(img[x,y],img[x-1,y]) and visit[x-1][y]!=1):
        img_output=floodfill(img,img_output,x-1,y,color,visit)
    if (x<w-1 and pixel_simillar(img[x,y],img[x+1,y]) and visit[x+1][y]!=1):
        img_output=floodfill(img,img_output,x+1,y,color,visit)
    if (y>0 and pixel_simillar(img[x,y],img[x,y-1]) and visit[x][y-1]!=1):
        img_output=floodfill(img,img_output,x,y-1,color,visit)
    if (y<h-1 and pixel_simillar(img[x,y],img[x,y+1]) and visit[x][y+1]!=1):
        img_output=floodfill(img,img_output,x,y+1,color,visit)
    img_output[x,y]=color
    return img_output

def floodfill_region(img,xx,yy,visit,cnt):
    w=img.shape[0]
    h=img.shape[1]
    visit_orig=visit
    q=queue.Queue()
    q.put((xx,yy))
    k=1
    while not q.empty():
        x,y=q.get()
        if (visit[x][y]!=0):
            continue
        visit[x][y]=cnt
        if (x>0 and pixel_simillar(img[x,y],img[x-1,y]) and visit[x-1][y]==0):
            q.put((x-1,y))
            #print(str(x-1)+" "+str(y))
        if (x<w-1 and pixel_simillar(img[x,y],img[x+1,y]) and visit[x+1][y]==0):
            q.put((x+1,y))
            #print(str(x+1)+" "+str(y))
        if (y>0 and pixel_simillar(img[x,y],img[x,y-1]) and visit[x][y-1]==0):
            q.put((x,y-1))
        if (y<h-1 and pixel_simillar(img[x,y],img[x,y+1]) and visit[x][y+1]==0):
            q.put((x,y+1))
        k+=1
    return visit,k

def floodfill_visit(img,x,y,visit,comp):
    if (visit[x][y]):
        return
    visit[x][y]=True;
    w=img.shape[0]
    h=img.shape[1]
    if (x>0 and comp(img,x-1,y) and not visit[x-1][y]):
        visit=np.bitwise_or(visit,floodfill_visit(img,x-1,y,visit,comp))
    if (x<w-1 and comp(img,x+1,y) and not visit[x+1][y]):
        visit=np.bitwise_or(visit,floodfill_visit(img,x+1,y,visit,comp))
    if (y>0 and comp(img,x,y-1) and not visit[x][y-1]):
        visit=np.bitwise_or(visit,floodfill_visit(img,x,y-1,visit,comp))
    if (y<h-1 and comp(img,x,y+1) and not visit[x][y+1]):
        visit=np.bitwise_or(visit,floodfill_visit(img,x,y+1,visit,comp))
    return visit
    

def color_finding(img):
    visit=np.zeros((300,300),bool)
    ans=[]
    for xx in range(img.shape[0]):
        for yy in range(img.shape[1]):
            if (is_blue(img,xx,yy) and not visit[xx][yy]):
                visit=floodfill_visit(img,xx,yy,visit,is_blue)
                ans.append((xx,yy,(255,0,0)))
            if (is_red(img,xx,yy) and not visit[xx][yy]):
                visit=floodfill_visit(img,xx,yy,visit,is_red)
                ans.append((xx,yy,(0,0,255)))
            if (is_green(img,xx,yy) and not visit[xx][yy]):
                visit=floodfill_visit(img,xx,yy,visit,is_green)
                ans.append((xx,yy,(0,255,0)))
    return ans

def region_counting(img):
    visit=np.zeros((img.shape[0],img.shape[1]),np.int32)
    cnt=1
    size=img.shape[0]*img.shape[1]
    black=0
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if (is_black(img,x,y)):
                #visit[x][y]=10000
                #black+=1
                continue
            if (visit[x][y]==0 and not is_black(img,x,y)):
                #print(str(x)+" "+str(y))
                visit_temp=visit
                visit_temp,temp=floodfill_region(img,x,y,visit,cnt)
                if (temp<300):
                    continue
                visit=visit_temp
                #print("region"+str(cnt)+"found")
                #print(visit)
                cnt=cnt+1
    print(cnt)
    return visit

def Image_Process_data(img,img_colored):
    image_crop=Image_Detection(img)
    image_crop_colored=Image_Detection(img_colored)

    #image_crop=Util.Bright(image_crop,20) #Change this value
    #image_crop_colored=Util.Bright(image_crop_colored,40)
    image_crop=Util.Contrast_and_Bright(image_crop,1.25,-40)
    image_crop_colored=Util.Contrast_and_Bright(image_crop_colored,1.25,-40)

    clicked=0
    click_point=(0,0)

    colors=color_finding(image_crop_colored)
    print(colors)
    image_crop_fullcolor=image_crop.copy()
    for color in colors:
        cv2.floodFill(image_crop_fullcolor,None,(color[1],color[0]),color[2],(20,)*3,(20,)*3,0)
    cv2.imwrite('./process/img_c.jpg',image_crop)
    cv2.imwrite('./process/img_c_C.jpg',image_crop_colored)
    cv2.imwrite('./process/img_c_f.jpg',image_crop_fullcolor)
    return image_crop,image_crop_colored,image_crop_fullcolor
    
def temp_region():
    visit=region_counting(image_crop)
    img_print=image_crop.copy()
    for xx in range(img_print.shape[0]):
        for yy in range(img_print.shape[1]):
            try:
                img_print[xx,yy]=list[visit[xx][yy]]
            except IndexError:
                print(visit[xx][yy])
            #img_print[xx,yy]=(visit[xx][yy]/25,visit[xx][yy]%25*4,0)
            #if (visit[xx][yy]==10000):
                #img_print[xx,yy]=(0,0,255)
    cv2.imshow("img_print",img_print)


if __name__=="__main__":
    img=cv2.imread("i1.jpg")
    img_colored=cv2.imread("i2.jpg")
    image_crop,image_crop_colored,image_crop_fullcolor=Image_Process_data(img,img_colored)
    cv2.imwrite('./process/img_c.jpg',image_crop)
    cv2.imwrite('./process/img_c_C.jpg',image_crop_colored)
    cv2.imwrite('./process/img_c_f.jpg',image_crop_fullcolor)
    cv2.imshow("aa",image_crop)
    cv2.imshow("f",image_crop_fullcolor)
    i_c_f_s=cv2.resize(image_crop_fullcolor,((99,70)),interpolation=cv2.INTER_AREA)
    cv2.imshow("asdf",i_c_f_s)
    
    
    
    
          
'''
print(click_point[1])
print(is_blue(image_crop,click_point[0],click_point[1]))
print(is_green(image_crop,click_point[0],click_point[1]))
print(is_red(image_crop,click_point[0],click_point[1]))
'''



'''
image_diff=np.zeros((image_crop.shape[0],image_crop.shape[1],3),np.uint8)
for xx in range(image_diff.shape[0]):
    for yy in range(image_diff.shape[1]):
        if (image_crop[xx][yy]!=img_crop_copy_2[xx][yy]):
            image_diff[xx][yy]=[255,255,255]
        else:
            image_diff[xx][yy]=[0,0,0]

cv2.imshow("diff",image_diff)
'''
