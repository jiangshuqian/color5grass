import numpy
import cv2
import glob

def select_grass(event,x,y,flags,param):
    global ix,iy,fx,fy
    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        fx,fy = x,y
        crop_grass = img[iy:fy,ix:fx]
        cv2.imshow('watermark',crop_grass)
cv2.namedWindow('grass',0)
cv2.setMouseCallback('grass',select_grass)
images = glob.glob('*.png')
i = 1
for picture in images:
    img = cv2.imread(picture)
    cv2.imshow('grass',img)
    while True:
        key = cv2.waitKey() & 0xFF
        if key == ord('w'):
            crop_grass = img[iy:fy,ix:fx]
            gname = 'cut_grass/grass%02d.png' %i
            i +=1
            cv2.imwrite(gname,crop_grass)
            print 'save grass_crop.png seccess! press any key to continue'
        elif key == ord('n'):
            break
        elif key == ord('q'):
            break
    if key == ord('q'):
        break

cv2.destroyAllWindows()
