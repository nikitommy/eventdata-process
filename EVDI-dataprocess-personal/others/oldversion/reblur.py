import os, cv2, glob
import numpy as np

img_dir_names = sorted(glob.glob(os.path.join('./reblur2/img', '*')))
event_dir_names = sorted(glob.glob(os.path.join('./reblur2/event', '*')))
# print(img_dir_names[0])
imgs = []

for i in range(len(img_dir_names)):
    img = cv2.imread(img_dir_names[i],cv2.IMREAD_GRAYSCALE)
    imgs.append(img)
imgs = np.array(imgs).astype(np.float64)  
reblur1 = imgs[:6, :, :].mean(0)
reblur2 = imgs[-6:, :, :].mean(0)
# cv2.imwrite('reblur1.png',reblur1,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
# cv2.imwrite('reblur2.png',reblur2,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
# print(reblur1.shape)
#generate event npy files

t,x,y,p = np.loadtxt(event_dir_names[0],unpack=True)
t, _ = np.modf(t)
t = (t*1e7).astype(int)
for i in range(len(event_dir_names)-1):    
    t1,x1,y1,p1 = np.loadtxt(event_dir_names[i+1],unpack=True)
    
    t1, _ = np.modf(t1)
    t1 = (t1*1e7).astype(int)

    x = np.concatenate([x, x1], axis=0).astype(int)
    y = np.concatenate([y, y1], axis=0).astype(int)
    p = np.concatenate([p, p1], axis=0).astype(int)
    t = np.concatenate([t, t1], axis=0).astype(int)

exp_start1, _ = np.modf(1581815294.767973)
exp_start1 = (exp_start1*1e7).astype(int)
exp_end1, _ = np.modf(1581815294.974051)
exp_end1 = (exp_end1*1e7).astype(int)
exp_start2, _ = np.modf(1581815295.056418)
exp_start2 = (exp_start2*1e7).astype(int)
exp_end2, _ = np.modf(1581815295.262400)
exp_end2 = (exp_end2*1e7).astype(int)

events = {'x': x, 'y': y, 'p': p, 't': t}

np.savez('HQF1.npz', events = events, blur1 = reblur1, blur2 = reblur2, exp_start1 = exp_start1, \
    exp_end1 = exp_end1, exp_start2 = exp_start2, exp_end2 = exp_end2)

