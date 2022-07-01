import os, cv2 
import glob
import numpy as np
import argparse
import pandas as pd
from imgprocess import gettimelist
from imgprocess import gettimestamp
from utils import *
from tqdm import tqdm

import multiprocessing
multiprocessing.set_start_method('spawn',True)

def main(opt, imgnum, reblurnum, loop):
    # read the bag event
    filesname = os.path.join(opt.event_path1, '011.bag')
    eventtxt_path = opt.event_path1
    reader(filesname, eventtxt_path)

    csvfiles = os.path.join(opt.csv_path, 'images.csv')
    timelist = gettimelist(csvfiles, imgnum, reblurnum, loop)
    
    # pic_dir_names = sorted(glob.glob(os.path.join(opt.pic_path, '*'))) #for color picture
    # loop = int(len(pic_dir_names) / 2)
    picgray_dir_names = sorted(glob.glob(os.path.join(opt.picgray_path, '*'))) #for gray picture
    loop = int(len(picgray_dir_names) / 2)
    
    eventtxt = os.path.join(opt.event_path2, '{}.txt'.format(basename(filesname)))
    events = event2array(eventtxt)

    if not os.path.exists(opt.save_path):
        os.mkdir(opt.save_path)

    for i in tqdm(range(loop)):
        time = gettimestamp(timelist, i, reblurnum)
        print(time)
        print("Writing npzfiles between two pic, now is "+ str(i+1)+'!')
        data2npz(opt,i,time,events)
    print("data2npz complicate!")

def data2npz(opt,x,time,events):
    if color == 1:
        pic_dir_names = sorted(glob.glob(os.path.join(opt.pic_path, '*'))) #for color picture
    else:
        pic_dir_names = sorted(glob.glob(os.path.join(opt.picgray_path, '*'))) #for gray picture
    
    exp_start1, exp_end1, exp_start2, exp_end2 = time
    events = filter_events(events, exp_start1, exp_end2)
    blur1 = cv2.imread(pic_dir_names[x*2])
    blur2 = cv2.imread(pic_dir_names[x*2+1])

    filename = basename(pic_dir_names[x*2]) + '-' + basename(pic_dir_names[x*2+1]) + '.npz'
    np.savez(os.path.join(opt.save_path, filename), events = events, blur1 = blur1,\
         blur2 = blur2, exp_start1 = exp_start1, exp_end1 = exp_end1, exp_start2 = exp_start2, exp_end2 = exp_end2)

if __name__ == '__main__':
    ## parameters
    parser = argparse.ArgumentParser(description="data2npz")
    parser.add_argument("--pic_path1", type=str, default="./test/colorblur", help="path of color blur picture")
    parser.add_argument("--pic_path2", type=str, default="./test/grayblur", help="path of gray blur picture")
    parser.add_argument("--event_path1", type=str, default="./test", help="path of event bag data")
    parser.add_argument("--event_path2", type=str, default="./test", help="path of event txt data")
    parser.add_argument("--csv_path", type=str, default="./test", help="path of img csv data")
    parser.add_argument("--save_path", type=str, default="./test/train", help="npz save path")
    parser.add_argument("--origin", type=int, default=1, help="the fps frame ratio")
    parser.add_argument("--imgnum", type=int, default=495, help="the origin frame of video")
    parser.add_argument("--setnum", type=int, default=15, help="the origin reblur frame of video")
    parser.add_argument("--color", type=int, default=1, help="img type")

    opt = parser.parse_args()

    imgnum, reblurnum, loop = calculatenum(opt.imgnum, opt.setnum, opt.origin)
    main(opt, imgnum, reblurnum, loop)
