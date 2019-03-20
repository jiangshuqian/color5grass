import numpy as np
import cv2
import sys,glob

buttondown = False
def get_num(event,x,y,flags,param):
    global ix,iy,buttondown
    if event == cv2.EVENT_LBUTTONDOWN:
	ix,iy = x,y
	buttondown = True

cv2.namedWindow('picture',0)
cv2.setMouseCallback('picture',get_num)
images = glob.glob('cut_grass/grass*.png')
count = 1
for fname in images:
    img = cv2.imread(fname)
    cv2.imshow('picture',img)
    while True:
	if buttondown:
	    buttondown = False
	    sys.stdout.write('count:%003d c1:%003d c2:%003d c3:%003d\r' %(count,img[iy,ix,0],img[iy,ix,1],img[iy,ix,2]))
	    sys.stdout.flush()
	    if count == 1:
		c1,c2,c3 = [img[iy,ix,0]],[img[iy,ix,1]],[img[iy,ix,2]]
		img_name,x_coordinate,y_coordinate = [fname],[ix],[iy]
	    else:
		c1.append(img[iy,ix,0])
		c2.append(img[iy,ix,1])
		c3.append(img[iy,ix,2])
		img_name.append(fname)
		x_coordinate.append(ix)
		y_coordinate.append(iy)
	    count +=1
	key = cv2.waitKey(20) & 0xFF
	if key == ord('n') or key == ord('q'):  #if you press the key of n, it will jump next picture.
	    break
    if key == ord('q'):
	break
print
#np.savez('Grass_data.npz',img_name=img_name,x_coordinate=x_coordinate,y_coordinate=y_coordinate)    #get grass data
np.savez('bGrass_data.npz',img_name=img_name,x_coordinate=x_coordinate,y_coordinate=y_coordinate)    #get background data

cv2.destroyAllWindows()
