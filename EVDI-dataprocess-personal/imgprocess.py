import os, cv2, glob
import numpy as np
import pandas as pd
import argparse
from utils import *

def getsharpframe(opt, imgnum, reblurnum, loop):
    img_dir_names = sorted(glob.glob(os.path.join(opt.pic_path_orginal, '*')))
    imgs = []
    for i in range(len(img_dir_names)):
        img = cv2.imread(img_dir_names[i])
        imgs.append(img)
    imgs = np.array(imgs).astype(np.float64) 
    m =  int((reblurnum - 1) / 2)
    n = int(imgnum / loop)
    c = int((m + 1) / 2)
    for i in range(loop):
        a, b = i * n, (i + 1) * n
        imgsloop = imgs[a:b,:,:]
        sharp1 = imgsloop[c, :, :]
        sharp2 = imgsloop[-c, :, :]
        cv2.imwrite(os.path.join(opt.pic_path3,'sharp{}.png'.format('%04d'%(i*2+1))),sharp1,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        cv2.imwrite(os.path.join(opt.pic_path3,'sharp{}.png'.format('%04d'%(i*2+2))),sharp2,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    print("successful get the sharp frame!")


def gettimelist(csvfiles, imgnum, reblurnum, loop):
    #reblur image use sharp image
    timelist = []
    time = pd.read_csv(csvfiles, names=['t','x'], header=None)
    t = np.array(list(time['t']))
    t = np.trunc(t).astype(int)
    a = int(imgnum / loop)
    b = int(loop) #number of timelists
    for i in range(b):
        m, n = i*a, (i+1)*a
        x = t[m:n]
        timelist.append(x)

    return timelist

def gettimestamp(timelist, idx, num):
    #Get the timestamp
    time = np.array(timelist[idx])
    
    exp_start1 = time[0]
    exp_end1 = time[num-1]
    exp_start2 = time[-num]
    exp_end2 = time[-1]

    return exp_start1, exp_end1, exp_start2, exp_end2

def reblur(opt, imgnum, reblurnum, loop):
    img_dir_names = sorted(glob.glob(os.path.join(opt.pic_path, '*')))
    imgs = []
    for i in range(len(img_dir_names)):
        img = cv2.imread(img_dir_names[i])
        imgs.append(img)
    imgs = np.array(imgs).astype(np.float64) 

    m = reblurnum
    n = int(imgnum / loop)

    if opt.color == 1:
        blur_savepath = opt.pic_path1
    else:
        blur_savepath = opt.pic_path2

    if not os.path.exists(blur_savepath):
        os.mkdir(blur_savepath)
    loop = int(loop / opt.origin)
    for i in range(loop):
        a, b = i * n, (i + 1) * n
        imgsloop = imgs[a:b,:,:]
        reblur1 = imgsloop[:m, :, :].mean(0)
        reblur2 = imgsloop[-m:, :, :].mean(0)
        cv2.imwrite(os.path.join(blur_savepath,'reblur{}.png'.format('%04d'%(i*2+1))),reblur1,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        cv2.imwrite(os.path.join(blur_savepath,'reblur{}.png'.format('%04d'%(i*2+2))),reblur2,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    print("reblur processing over!")

def color2gray(color_img):
    size_h, size_w, channel = color_img.shape
    gray_img = np.zeros((size_h, size_w), dtype=np.uint8)
    gray_img = np.round((color_img[:, :, 0]*29.9 + color_img[:, :, 1]*58.7 + color_img[:, :, 2]*11.4)/100)
    return gray_img

def save_pic(pic_gray,picgray_path,pic_dir_names):
    cv2.imwrite(os.path.join(picgray_path, os.path.basename(pic_dir_names)),pic_gray,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])

def grayimg(opt,color):
    if opt.color == 1:
        blurimg_dir_names = sorted(glob.glob(os.path.join(opt.pic_path1, '*')))

        if not os.path.exists(opt.pic_path2):
            os.mkdir(opt.pic_path2)

        for i in range(len(blurimg_dir_names)):
            pic = cv2.imread(blurimg_dir_names[i])
            blur = color2gray(pic).astype(np.float64)
            save_pic(blur, opt.pic_path2, blurimg_dir_names[i])
        print("color2gray processing over!")
    else:
        print("it's gray img, do not need to convert!")

def picdown(opt, x, y):
    #读取原始图像的信息
    img_dir_names = sorted(glob.glob(os.path.join(opt.pic_path, '*')))
    imgs = []
    for i in range(len(img_dir_names)):
        img = cv2.imread(img_dir_names[i])
        imgs.append(img)
    imgs = np.array(imgs).astype(np.float64)
    
    if not os.path.exists(opt.down_path):
        os.mkdir(opt.down_path)
    
    for i in range(len(imgs)):
        img1 = cv2.resize(imgs[i], fx = x, fy = y, dsize = None)  #调整图像大小
 
        img2 = cv2.pyrDown(img1)
        save_pic(img2,opt.down_path,img_dir_names[i])
    print("picture down sample complete!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="imgprocess")
    parser.add_argument("--pic_path_orginal", type=str, default="./test/test", help="path of orginal frames")
    parser.add_argument("--pic_path", type=str, default="./test/test", help="path of sharpframes")
    parser.add_argument("--pic_path1", type=str, default="./test/colorblur", help="path of colorblur picture")
    parser.add_argument("--pic_path2", type=str, default="./test/grayblur", help="path of grayblur picture")
    parser.add_argument("--pic_path3", type=str, default="./test/sharp", help="path of sharp picture")
    parser.add_argument("--down_path", type=str, default="./test/sharp", help="path of down sample picture")
    parser.add_argument("--origin", type=int, default=8, help="the fps frame ratio")
    parser.add_argument("--imgnum", type=int, default=3960, help="the origin frame of video")
    parser.add_argument("--setnum", type=int, default=360, help="the origin reblur frame of video")
    parser.add_argument("--color", type=int, default=0, help="img type:color(1) or gray(0)")

    opt = parser.parse_args()

    imgnum, reblurnum, loop = calculatenum(opt.imgnum, opt.setnum, opt.origin)
    reblur(opt, imgnum, reblurnum, loop)
    # getsharpframe(opt, imgnum, reblurnum, loop)
    grayimg(opt,opt.color)
    # picdown(opt, 0.5, 0.5)
