import datetime
import pandas as pd
import numpy as np
from picture2gray import color2gray
from imgprocess import gettimelist
from imgprocess import gettimestamp
import cv2, os
from utils import *

# pd_data = pd.read_csv('test.txt')
# event = pd.read_csv('images.csv', names=['t','x'], header=None)
# x = gettimelist('images.csv')
# y = gettimestamp(x,0)
# a,b,c,d = y
# x = np.array(list(event['t'])).astype(int)
# x = np.zeros(10)
#id1=list(poi_data1['ID'])
#visit=list(poi_data1['visit'])
# a = np.zeros((3,1,1))

# color_img = cv2.imread('reblur1.png')
# size_h, size_w, channel = color_img.shape
# start = datetime.datetime.now()
# gray_img = np.zeros((size_h, size_w), dtype=np.uint8)
# for i in range(size_h):
#     for j in range(size_w):
#         gray_img[i, j] = round((color_img[i, j, 0]*29.9 + color_img[i, j, 1]*58.7 +\
#             color_img[i, j, 2]*11.4)/100)
# gray_img = gray_img.astype(np.float64)
# stop = datetime.datetime.now()
# print(stop-start)
# a = color_img
# start = datetime.datetime.now()
# b = np.zeros((size_h, size_w), dtype=np.uint8)
# b = np.round((a[:, :, 0]*29.9 + a[:, :, 1]*58.7 + a[:, :, 2]*11.4)/100)
# stop = datetime.datetime.now()
# print(stop-start)
# print((b==gray_img).all())

# a = color2gray(a).astype(np.float64)
# x, y, p, t = np.loadtxt('test.txt',unpack=True)

# def main(opt):
#     filesname = os.path.join(opt.event_path1, 'out.bag')
#     reader(filesname)

#     csvfiles_dir_names = sorted(glob.glob(os.path.join(opt.event_path2, 'images.csv')))
#     imgnum = 960
#     reblurnum = 15
#     timelist = gettimelist(csvfiles_dir_names, imgnum, reblurnum)
    
#     picgray_dir_names = sorted(glob.glob(os.path.join(opt.picgray_path, '*')))
#     for i in range(len(picgray_dir_names) / 2):
#         time = gettimestamp(timelist, i)
#         data2npz(opt,i,time)


# timelist = []
# pd_data = pd.read_csv('./youtube/images.csv', names=['t','x'], header=None)
# t = np.array(list(pd_data['t']))
# t = np.trunc(t).astype(int)
# a = int(15)
# b = int(960 / a) #images number/ reblur imgs number
# for i in range(b):
#     m, n = i*a, (i+1)*a
#     x = t[m:n]
#     timelist.append(x)
# print(timelist)
path = "youtube/images.csv"
filename = basename(path)
filename = filename.zfill(6)
print(filename)
