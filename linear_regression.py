#!/usr/bin/python2
import numpy as np
import cv2,sys,glob
import pylab as pl

with np.load('Grass_data.npz') as data:
    img_name,x_coordinate,y_coordinate = [data[i] for i in ('img_name','x_coordinate','y_coordinate')]


with np.load('bGrass_data.npz') as data:
    bac_name,xb_coordinate,yb_coordinate = [data[i] for i in ('img_name','x_coordinate','y_coordinate')]

def plot_dot(c1,c2,c3,b1,b2,b3):
    pl.figure(1)
    pl.plot(c1, c2,'or')
    pl.plot(b1, b2,'og')
    pl.plot([0,200], [24,238],'b')
    #pl.plot([0,255], [16,255],'y')
    #pl.plot([0,145], [116,261],'y')
    pl.xlabel('channal1')
    pl.ylabel('channal2')
    pl.figure(2)
    pl.plot(c2, c3,'or')
    pl.plot(b2, b3,'og')
    pl.plot([20,255], [18,254],'b')
    #pl.plot([20,255], [0,254],'y')
    #pl.plot([90,255], [0,184],'y')
    pl.xlabel('channal2')
    pl.ylabel('channal3')
    #pl.figure(3)
    #pl.plot(c1, c3,'or')
    #pl.plot(b1, b3,'og')
    #pl.xlabel('channal1')
    #pl.ylabel('channal3')
    pl.show()
    return

images = glob.glob('cut_grass/grass*.png')
fname = 'none'
for count in range(len(img_name)):
    if img_name[count] != fname:
        for fname in images:
            if img_name[count] == fname:
                img = cv2.imread(fname)
                break
        else:
            print 'waring: Image not found! The grass data maybe have error.'
    ix = x_coordinate[count]
    iy = y_coordinate[count]
    sys.stdout.write('count:%003d c1:%003d c2:%003d c3:%003d\r' %(count,img[iy,ix,0],img[iy,ix,1],img[iy,ix,2]))
    sys.stdout.flush()
    if count == 0:
        c1,c2,c3 = [img[iy,ix,0]],[img[iy,ix,1]],[img[iy,ix,2]]
    else:
        c1.append(img[iy,ix,0])
        c2.append(img[iy,ix,1])
        c3.append(img[iy,ix,2])
print
for count in range(len(bac_name)):
    if bac_name[count] != fname:
        for fname in images:
            if bac_name[count] == fname:
                img = cv2.imread(fname)
                break
        else:
            print 'waring: Image not found! The background data maybe have error.'
    ix = xb_coordinate[count]
    iy = yb_coordinate[count]
    sys.stdout.write('count:%003d c1:%003d c2:%003d c3:%003d\r' %(count,img[iy,ix,0],img[iy,ix,1],img[iy,ix,2]))
    sys.stdout.flush()
    if count == 0:
        b1,b2,b3 = [img[iy,ix,0]],[img[iy,ix,1]],[img[iy,ix,2]]
    else:
        b1.append(img[iy,ix,0])
        b2.append(img[iy,ix,1])
        b3.append(img[iy,ix,2])
print
plot_dot(c1,c2,c3,b1,b2,b3)
