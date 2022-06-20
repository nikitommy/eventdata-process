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


def main(opt):
    # filesname = os.path.join(opt.event_path1, 'out.bag')
    # reader(filesname)

    csvfiles = os.path.join(opt.csv_path, 'images.csv')
    imgnum = 1100
    reblurnum = 11
    timelist = gettimelist(csvfiles, imgnum, reblurnum)
    
    picgray_dir_names = sorted(glob.glob(os.path.join(opt.picgray_path, '*')))
    loop = int(len(picgray_dir_names) / 2)
    
    eventtxt = os.path.join(opt.event_path2, 'out.txt')
    events = event2array(eventtxt)
    
    for i in tqdm(range(loop)):
        time = gettimestamp(timelist, i)
        print(time)
        print("Writing npzfiles between two pic, now is "+ str(i+1)+'!')
        data2npz(opt,i,time,events)
    print("data2npz complicate!")
        

def data2npz(opt,x,time,events):
    pic_dir_names = sorted(glob.glob(os.path.join(opt.pic_path, '*')))
    picgray_dir_names = sorted(glob.glob(os.path.join(opt.picgray_path, '*')))
    
    exp_start1, exp_end1, exp_start2, exp_end2 = time
    events = filter_events(events, exp_start1, exp_end2)
    blur1 = cv2.imread(picgray_dir_names[x*2],cv2.IMREAD_GRAYSCALE)
    blur2 = cv2.imread(picgray_dir_names[x*2+1],cv2.IMREAD_GRAYSCALE)

    filename = basename(picgray_dir_names[x]) + '-' + basename(picgray_dir_names[x+1]) + '.npz'
    print(len(picgray_dir_names[x+1]))
    np.savez(os.path.join(opt.save_path, filename), events = events, blur1 = blur1,\
         blur2 = blur2, exp_start1 = exp_start1, exp_end1 = exp_end1, exp_start2 = exp_start2, exp_end2 = exp_end2)

if __name__ == '__main__':
    ## parameters
    parser = argparse.ArgumentParser(description="data2npz")
    parser.add_argument("--pic_path", type=str, default="./GOPR0854_11_00/blur", help="path of picture")
    parser.add_argument("--picgray_path", type=str, default="./GOPR0854_11_00/blurgray", help="path of gray picture")
    parser.add_argument("--event_path1", type=str, default="./GOPR0854_11_00", help="path of event bag data")
    parser.add_argument("--save_path", type=str, default="./GOPR0854_11_00/train", help="saving path")
    parser.add_argument("--event_path2", type=str, default="./GOPR0854_11_00", help="path of event txt data")
    parser.add_argument("--csv_path", type=str, default="./GOPR0854_11_00", help="path of img csv data")

    opt = parser.parse_args()

    main(opt)
