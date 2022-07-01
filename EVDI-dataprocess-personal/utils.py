#!/usr/bin/env python
import rosbag
from tqdm import tqdm
import pandas as pd
import os
import numpy as np

def basename(fullname):
    a = os.path.basename(os.path.splitext(fullname)[0])
    return a

def reader(filesname,save_path):
    #Read events in filesname.bag
    bag=rosbag.Bag(filesname)
    with open(save_path+'/{}.txt'.format(basename(filesname)),'w') as f: 
        for i,(topic,msgs,t) in enumerate(bag.read_messages(topics=['/cam0/events'])):
            for single_event in tqdm(msgs.events):  
                f.write(str(single_event.ts.secs+single_event.ts.nsecs*1.0/1000000000)+' ')         
                f.write(str(single_event.x)+' ')
                f.write(str(single_event.y)+' ')
                if(single_event.polarity==True):        
                    f.write("1")
                else:
                    f.write("-1")
                f.write('\n')  
            print("Writing events between two pic, now is "+ str(i)+'!')
    print("Writing is over!")
    bag.close()

def event2array(eventfilename):
    #Read events and convert events to dict
    event = pd.read_csv(eventfilename, names=['t','x','y','p'], header=None, sep=' ')
    
    t = np.array(list(event['t']))
    t = np.trunc(t * 1e9).astype(int)
    x = np.array(list(event['x'])).astype(int)
    y = np.array(list(event['y'])).astype(int)
    p = np.array(list(event['p'])).astype(int)
    
    event = {'x': x, 'y': y, 'p': p, 't': t}
    return event

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

    event = {'x': x, 'y': y, 'p': p, 't': t}
    return event

def custombasename(fullname):
    a = os.path.basename(os.path.splitext(fullname)[0])
    a = np.array(a)  
    a = (a.astype(float)*1e7).astype(int)
    return a

def editnpz(filename,name,value):
    filedic = dict(np.load(filename, allow_pickle=True))
    filedic[name] = value
    np.savez(filename, **filedic)

def calculatenum(imgnum, setnum, origin):
    if origin == 1:
        print("now processing original video!")
        if setnum % 2 == 0:
            reblurnum = (setnum / 2) - 1
        else:
            reblurnum = (setnum - 1) / 2
        imgnum = int(imgnum)
        reblurnum = int(reblurnum)
    else:
        print("now processing up-convert video!")
        if setnum % 2 == 0:
            reblurnum = ((setnum / 2) - 1) * origin
        else:
            reblurnum = ((setnum - 1) / 2) * origin
        imgnum = int(imgnum * origin)
        reblurnum = int(reblurnum)
    loop = int(imgnum / setnum)
    return imgnum, reblurnum, loop
# def get_PSNR_SSIM(self, output, gt, crop_border=4):
#         cropped_output = output[crop_border:-crop_border, crop_border:-crop_border, :]
#         cropped_GT = gt[crop_border:-crop_border, crop_border:-crop_border, :]
#         psnr = self.calc_PSNR(cropped_GT, cropped_output)
#         ssim = self.calc_SSIM(cropped_GT, cropped_output)
#         return psnr, ssim

#     def calc_PSNR(self, img1, img2):
#         '''
#         img1 and img2 have range [0, 255]
#         '''
#         img1 = img1.astype(np.float64)
#         img2 = img2.astype(np.float64)
#         mse = np.mean((img1 - img2) ** 2)
#         if mse == 0:
#             return float('inf')
#         return 20 * math.log10(255.0 / math.sqrt(mse))

#     def calc_SSIM(self, img1, img2):
#         '''calculate SSIM
#         the same outputs as MATLAB's
#         img1, img2: [0, 255]
#         '''

#         def ssim(img1, img2):
#             C1 = (0.01 * 255) ** 2
#             C2 = (0.03 * 255) ** 2

#             img1 = img1.astype(np.float64)
#             img2 = img2.astype(np.float64)
#             kernel = cv2.getGaussianKernel(11, 1.5)
#             window = np.outer(kernel, kernel.transpose())

#             mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
#             mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
#             mu1_sq = mu1 ** 2
#             mu2_sq = mu2 ** 2
#             mu1_mu2 = mu1 * mu2
#             sigma1_sq = cv2.filter2D(img1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
#             sigma2_sq = cv2.filter2D(img2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq
#             sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

#             ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
#                                                                     (sigma1_sq + sigma2_sq + C2))
#             return ssim_map.mean()

#         if not img1.shape == img2.shape:
#             raise ValueError('Input images must have the same dimensions.')
#         if img1.ndim == 2:
#             return ssim(img1, img2)
#         elif img1.ndim == 3:
#             if img1.shape[2] == 3:
#                 ssims = []
#                 for i in range(3):
#                     ssims.append(ssim(img1, img2))
#                 return np.array(ssims).mean()
#             elif img1.shape[2] == 1:
#                 return ssim(np.squeeze(img1), np.squeeze(img2))
#         else:
#             raise ValueError('Wrong input image dimensions.')

# # psnr, ssim = self.get_PSNR_SSIM(output_img, gt)