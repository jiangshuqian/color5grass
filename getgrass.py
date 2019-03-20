#!/usr/bin/python2
import weave
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
            if(img(i,j,1) >= 1.09*img(i,j,0) + 20 & img(i,j,2) <= img(i,j,1) - 2)
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

if __name__ == '__main__':
    #images = glob.glob('cut_grass/grass*.png')
    images = glob.glob('demo.png')
    if images == []: print 'no images found.'
    for fname in images:
        img = cv2.imread(fname)
        e1 = cv2.getTickCount()
        outimg = detect(img)
        e2 = cv2.getTickCount()
        print 'detect time:', (e2 - e1)/cv2.getTickFrequency() ,'s'
        kernel = np.ones((3,3),np.uint8)
        cv2.imshow('original thresh',outimg)
        cv2.imwrite('threshimg.png',outimg)
        cv2.imwrite('original.png',img)
        _,thresh = cv2.threshold(outimg,127,255,0)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.dilate(thresh, kernel, iterations=3)
        _, contours, _ = cv2.findContours(thresh,0,1)
        for cnt in contours:
            area=cv2.contourArea(cnt)
            M = cv2.moments(cnt)
            cx,cy = int(M['m10']/M['m00']),int(M['m01']/M['m00'])
            if cy > 240 and cy < 620:
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
                cv2.circle(img,(cx,cy),2,(0,0,255),3)
        cv2.imshow('original image',img)
        cv2.imwrite('resultimg.png',img)
        cv2.imshow('yellowGrass',thresh)
        cv2.waitKey() & 0xFF

    cv2.destroyAllWindows()

