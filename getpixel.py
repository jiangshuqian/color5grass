#/usr/bin/python2
import cv2

def get_num(event,x,y,flags,param):
    #global ix,iy,buttondown
    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x,y
        print ix,iy
cv2.namedWindow('picture')
cv2.setMouseCallback('picture',get_num)

if __name__=='__main__':
    img = cv2.imread('demo.png')
    img[:,199,0]=255
    img[:,441,0]=255
    outimg=img[:,200:400,:]
    cv2.imshow('picture',img)
    cv2.imshow('picture2',outimg)
    cv2.waitKey() & 0xFF
    cv2.destroyAllWindows()
