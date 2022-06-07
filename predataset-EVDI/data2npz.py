import os, cv2 
import glob
import numpy as np
import argparse
from event2npy import event2npy
from picture2gray import color2gray, save_pic

def data2npz(opt):
    pic_dir_names = sorted(glob.glob(os.path.join(opt.pic_path, '*')))
    picgray_dir_names = sorted(glob.glob(os.path.join(opt.picgray_path, '*')))
    
    events, exp_start1, exp_end1, exp_start2, exp_end2 = event2npy(opt)

    pic1 = cv2.imread(pic_dir_names[0])
    blur1 = color2gray(pic1).astype(np.float64)
    #blur1 = blur1.astype(np.float64)
    save_pic(blur1, opt.picgray_path, pic_dir_names[0])
    
    pic2 = cv2.imread(pic_dir_names[1])
    blur2 = color2gray(pic2).astype(np.float64)
    #blur2 = blur2.astype(np.float64)
    save_pic(blur2, opt.picgray_path, pic_dir_names[1])

    # exp_start1 = np.trunc(3.35500000e+03).astype(int)
    # exp_end1 = np.trunc(9.99997598e+08).astype(int)
    # exp_start2 = np.trunc(1.00000023e+09).astype(int)
    # exp_end2 = np.trunc(1.99999925e+09).astype(int)
    
    np.savez(os.path.join(opt.save_path, '','GoPro1.npz'), events = events, blur1 = blur1, blur2 = blur2, exp_start1 = exp_start1, exp_end1 = exp_end1, exp_start2 = exp_start2, exp_end2 = exp_end2)

if __name__ == '__main__':
    ## parameters
    parser = argparse.ArgumentParser(description="data2npz")
    parser.add_argument("--pic_path", type=str, default="./GoPro/blur", help="path of picture")
    parser.add_argument("--picgray_path", type=str, default="./GoPro/blurgray", help="path of gray picture")
    parser.add_argument("--event_path", type=str, default="./GoPro/event", help="path of event txt data")
    parser.add_argument("--save_path", type=str, default="./GoPro/npzdata", help="saving path")
    parser.add_argument("--test_ts", type=float, default=0.5, help="test timestamp in [0,1]")

    opt = parser.parse_args()
    data2npz(opt)
