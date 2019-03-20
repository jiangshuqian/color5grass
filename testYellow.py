#!/usr/bin/python3
import scipy.weave as weave
#import weave
import numpy as np
import cv2,time,glob

def detect(img):
    rows, cols, _ = np.shape(img)
    outimg = np.zeros((rows, cols), np.uint8)
    code = '''
    for(int i = 0; i < rows; i++)
    {
        for(int j = 0; j < cols; j++)
        {
            if(img(i,j,1) >= 0.93*img(i,j,0) + 16 & img(i,j,1) <= 0.93*img(i,j,0) + 108 & img(i,j,2) >= img(i,j,1) - 90 & img(i,j,2) <= img(i,j,1) - 20)
            {
                outimg(i,j) = 255;
            }
        }
    }
    '''
    weave.inline(
        code,['img','outimg','rows','cols'],
        type_converters=weave.converters.blitz,
        compiler = 'gcc')
    return outimg

def contoursCalculate(thresh):
    rows, cols = np.shape(thresh)
    outimg = np.zeros((rows, cols), np.uint8)
    _, contours, _ = cv2.findContours(thresh,0,1)
    x,y = [],[]
    for i in range(len(contours)):
        cnt = contours[i]
        if cv2.contourArea(cnt) > 30:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x.append(cx)
            y.append(cy)
            #outimg[cy,cx] = 255
    return x,y,thresh

images = glob.glob('cut_grass1/grass*.png')
#images = glob.glob('img*.jpg')
for fname in images:
    img = cv2.imread(fname)
    cv2.imshow('original image',img)
    e1 = cv2.getTickCount()
    outimg = detect(img)
    e2 = cv2.getTickCount()
    print ('detect time:', (e2 - e1)/cv2.getTickFrequency() ,'s')
    kernel = np.ones((3,3),np.uint8)
    cv2.imshow('original thresh',outimg)
    _,thresh = cv2.threshold(outimg,127,255,0)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    #cx,cy,thresh = contoursCalculate(thresh)
    cv2.imshow('yellowGrass',thresh)
    #cv2.putText(img, str(angle), (0,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (127,0,255) ,2)
    #print len(cx)
    cv2.waitKey() & 0xFF

cv2.destroyAllWindows()

