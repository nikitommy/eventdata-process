import os, cv2, glob
import numpy as np
import pandas as pd
import argparse

def getsharpframe(opt, imgnum, reblurnum):
    img_dir_names = sorted(glob.glob(os.path.join(opt.pic_path, '*')))
    imgs = []
    for i in range(len(img_dir_names)):
        img = cv2.imread(img_dir_names[i])
        imgs.append(img)
    imgs = np.array(imgs).astype(np.float64) 
    
    m =  int((reblurnum - 1) / 2)
    n = int(imgnum / reblurnum)
    c = int((m + 1) / 2)
    for i in range(n):
        a, b = i*reblurnum, (i+1)*reblurnum
        imgsloop = imgs[a:b,:,:]
        sharp1 = imgsloop[c, :, :]
        sharp2 = imgsloop[-c, :, :]
        cv2.imwrite(os.path.join(opt.pic_path3,'sharp{}.png'.format('%04d'%(i*2+1))),sharp1,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        cv2.imwrite(os.path.join(opt.pic_path3,'sharp{}.png'.format('%04d'%(i*2+2))),sharp2,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    print("successful get the sharp frame!")


def gettimelist(csvfiles, imgnum, reblurnum):
    #reblur image use 11 sharp image
    timelist = []
    time = pd.read_csv(csvfiles, names=['t','x'], header=None)
    t = np.array(list(time['t']))
    t = np.trunc(t).astype(int)
    a = int(reblurnum)
    b = int(imgnum / a) #images number/ reblur imgs number
    for i in range(b):
        m, n = i*a, (i+1)*a
        x = t[m:n]
        timelist.append(x)

    return timelist

def gettimestamp(timelist, idx):
    #Get the timestamp
    time = np.array(timelist[idx])
    
    exp_start1 = time[0]
    exp_end1 = time[4]
    exp_start2 = time[-5]
    exp_end2 = time[-1]

    return exp_start1, exp_end1, exp_start2, exp_end2

def reblur(opt, imgnum, reblurnum):
    img_dir_names = sorted(glob.glob(os.path.join(opt.pic_path, '*')))
    # print(len(img_dir_names))
    imgs = []
    for i in range(len(img_dir_names)):
        img = cv2.imread(img_dir_names[i])
        imgs.append(img)
    imgs = np.array(imgs).astype(np.float64) 

    m =  int((reblurnum - 1) / 2)
    n = int(imgnum / reblurnum)
    for i in range(n):
        a, b = i*reblurnum, (i+1)*reblurnum
        imgsloop = imgs[a:b,:,:]
        reblur1 = imgsloop[:m, :, :].mean(0)
        reblur2 = imgsloop[-m:, :, :].mean(0)
        cv2.imwrite(os.path.join(opt.pic_path2,'reblur{}.png'.format('%04d'%(i*2+1))),reblur1,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        cv2.imwrite(os.path.join(opt.pic_path2,'reblur{}.png'.format('%04d'%(i*2+2))),reblur2,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    print("reblur processing over!")

def color2gray(color_img):
    size_h, size_w, channel = color_img.shape
    gray_img = np.zeros((size_h, size_w), dtype=np.uint8)
    gray_img = np.round((color_img[:, :, 0]*29.9 + color_img[:, :, 1]*58.7 + color_img[:, :, 2]*11.4)/100)
    return gray_img

def save_pic(pic_gray,picgray_path,pic_dir_names):
    cv2.imwrite(os.path.join(picgray_path, os.path.basename(pic_dir_names)),pic_gray,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])

def grayimg(opt):
    blurimg_dir_names = sorted(glob.glob(os.path.join(opt.pic_path2, '*')))
    for i in range(len(blurimg_dir_names)):
        pic = cv2.imread(blurimg_dir_names[i])
        blur = color2gray(pic).astype(np.float64)
        save_pic(blur, opt.picgray_path, blurimg_dir_names[i])
    print("color2gray processing over!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="imgprocess")
    parser.add_argument("--pic_path", type=str, default="./GOPR0854_11_00/GOPR0854_11_00", help="path of raw picture")
    parser.add_argument("--pic_path2", type=str, default="./GOPR0854_11_00/blur", help="path of blur picture")
    parser.add_argument("--pic_path3", type=str, default="./GOPR0854_11_00/sharp", help="path of blur picture")
    parser.add_argument("--picgray_path", type=str, default="./GOPR0854_11_00/blurgray", help="path of gray picture")

    opt = parser.parse_args()
    imgnum = 1100
    reblurnum = 11
    reblur(opt, imgnum, reblurnum)
    getsharpframe(opt, imgnum, reblurnum)
    grayimg(opt)

