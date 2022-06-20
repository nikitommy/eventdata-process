import os, cv2, glob
import numpy as np

img_dir_names = sorted(glob.glob(os.path.join('./reblur/img', '*')))
event_dir_names = sorted(glob.glob(os.path.join('./reblur/event', '*')))
# print(img_dir_names[0])
imgs = []

for i in range(len(img_dir_names)):
    img = cv2.imread(img_dir_names[i],cv2.IMREAD_GRAYSCALE)
    imgs.append(img)
imgs = np.array(imgs).astype(np.float64)  
reblur1 = imgs[:4, :, :].mean(0)
reblur2 = imgs[-4:, :, :].mean(0)
# cv2.imwrite('reblur1.png',reblur1,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
# cv2.imwrite('reblur2.png',reblur2,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
# print(reblur1.shape)
#generate event npy files

t,x,y,p = np.loadtxt(event_dir_names[0],unpack=True)
t = np.trunc(t*1e7).astype(int)
for i in range(len(event_dir_names)-1):    
    t1,x1,y1,p1 = np.loadtxt(event_dir_names[i+1],unpack=True)
    
    t1 = np.trunc(t1*1e7).astype(int)

    x = np.concatenate([x, x1], axis=0).astype(int)
    y = np.concatenate([y, y1], axis=0).astype(int)
    p = np.concatenate([p, p1], axis=0).astype(int)
    t = np.concatenate([t, t1], axis=0).astype(int)
events = {'x': x, 'y': y, 'p': p, 't': t}

def filter_events(event_data, start, end):
    ## filter events based on temporal dimension
    x = event_data['x'][event_data['t']>=start]
    y = event_data['y'][event_data['t']>=start]
    p = event_data['p'][event_data['t']>=start]
    t = event_data['t'][event_data['t']>=start]
    
    x = x[t<=end]
    y = y[t<=end]
    p = p[t<=end]
    t = t[t<=end]
    return x,y,p,t

def custombasename(fullname):
    a = os.path.basename(os.path.splitext(fullname)[0])
    a = np.array(a)  
    a = (a.astype(float)*1e7).astype(int)
    return a

def basename(fullname):
    a = os.path.basename(os.path.splitext(fullname)[0])
    return a

start = custombasename(img_dir_names[0])
end = custombasename(img_dir_names[-1])

x, y, p, t =filter_events(events, start, end)
p[p == 0] = -1
# print(p[0:100])
events = {'x': x, 'y': y, 'p': p, 't': t}

exp_start1 = np.trunc(1581815294.767973 * 1e7).astype(int)
exp_end1 = np.trunc(1581815294.974051 * 1e7).astype(int)
exp_start2 = np.trunc(1581815295.056418 * 1e7).astype(int)
exp_end2 = np.trunc(1581815295.262400 * 1e7).astype(int)



# a = np.load('example-hqf.npz', allow_pickle=True)
# blur1 = a['blur1']
# blur2 = a['blur2']

np.savez('HQF1.npz', events = events, blur1 = reblur1, blur2 = reblur2, exp_start1 = exp_start1, \
    exp_end1 = exp_end1, exp_start2 = exp_start2, exp_end2 = exp_end2)

