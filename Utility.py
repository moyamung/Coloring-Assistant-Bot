import numpy as np
import cv2

img=cv2.imread('test_7.jpeg')
img_colored=cv2.imread("test_7_colored.jpeg")

def image_size_reduce(img,n):
    dim=((int)(img.shape[1]/n),(int)(img.shape[0]/n))
    img=cv2.resize(img,dim,interpolation=cv2.INTER_AREA)
    return img

def Bright(img,x):
    b=np.ones(img.shape,np.uint8)*x
    add=cv2.add(img,b)
    return add

def Contrast_and_Bright(img,a,b):
    output=img.copy()
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            for z in range(img.shape[2]):
                output[x,y][z]=a*img[x,y][z]+b
    return output

def HDR(img):
    img_list=[img]

if __name__=="__main__":
    img=image_size_reduce(img,8)
    img_colored=image_size_reduce(img_colored,8)

    add=Bright(img,30)
    bdd=Contrast_and_Bright(img,0.7,60)

    cv2.imshow('before',img)
    cv2.imshow('after',add)
    cv2.imshow('bdd',bdd)
