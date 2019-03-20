# color5grass
Use color to detect grass.
这个部分是当时S2Box视觉检测时写的测试代码，最近正好重新弄了一下，在这里分享给大家。

--- 
## 安装所需环境
本人所用的系统是Deepin（基于Ubuntu）
``` shell
sudo apt-get install python-opencv #如果你是源码编译安装忽略这个
sudo apt-get install python-matplotlib
pip install weave
```
## cut_grass.py 
读取图片，用鼠标划取图片，然后保存的cut_grass文件夹下。

## get_number.py
通过鼠标点击来提取草或背景的颜色值，然后储存起来，生成Grass_data.npz（草的数据）或bGrass_data.npz（背景的数据），运行时注释其中一个。
``` python 
#np.savez('Grass_data.npz',img_name=img_name,x_coordinate=x_coordinate,y_coordinate=y_coordinate)
np.savez('bGrass_data.npz',img_name=img_name,x_coordinate=x_coordinate,y_coordinate=y_coordinate)
```
## linear_regression.py
用来画出草和背景的数据值，方便观察，并用一条线将他们分开，用于以后的提取。
[观察图1](./doc/Figure_1.svg)
[观察图2](./doc/Figure_2.svg)
