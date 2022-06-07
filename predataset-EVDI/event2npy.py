import numpy as np
import glob
import os

def event2npy(opt):
    event_dir_names = sorted(glob.glob(os.path.join(opt.event_path, '*')))
    
    t1,x1,y1,p1 = np.loadtxt(event_dir_names[0],unpack=True)
    t2,x2,y2,p2 = np.loadtxt(event_dir_names[1],unpack=True)
    # t3,x3,y3,p3 = np.loadtxt(event_dir_names[2],unpack=True)
    t1 = np.trunc(t1*1e9).astype(int)
    t2 = np.trunc((t2 * 1e9) + t1[-1]).astype(int)
    # t3 = np.trunc((t3 + 2)*1e9).astype(int)
    
    exp_start1 = t1[0]
    exp_end1 = t1[-1]
    exp_start2 = t2[0]
    exp_end2 = t2[-1]

    x = np.concatenate([x1, x2], axis=0).astype(int)
    y = np.concatenate([y1, y2], axis=0).astype(int)
    p = np.concatenate([p1, p2], axis=0).astype(int)
    t = np.concatenate([t1, t2], axis=0).astype(int)
    
    # x = np.concatenate([x1, x2, x3], axis=0).astype(int)
    # y = np.concatenate([y1, y2, y3], axis=0).astype(int)
    # p = np.concatenate([p1, p2, p3], axis=0).astype(int)
    # t = np.concatenate([t1, t2, t3], axis=0).astype(int)
    z = {'x': x, 'y': y, 'p': p, 't': t}
    #np.save('./event2.npy', z)
    return z, exp_start1, exp_end1, exp_start2, exp_end2

#t1,x1,y1,p1 = np.loadtxt(event_dir_names[0],unpack=True)
#print(t2)