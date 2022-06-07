import numpy as np
import imageio
import cv2, glob, os


# pic_path = './GoPro/blur/000026.png'
# a = cv2.imread(pic_path)
# a = np.load('GoPro1.npz', allow_pickle=True)
picgray_dir_names = sorted(glob.glob(os.path.join('./GoPro/blurgray', '*')))
# start = a['exp_start1']
# end = a['exp_end1']
# start2 = a['exp_start2']
# end2 = a['exp_end2']
# event = a['events'].item()
# blur1 = a['blur1'] 
#print(a)
#t1,x1,y1,p1 = np.loadtxt('./GoPro/event/000027.txt',unpack=True)
a = cv2.imread(picgray_dir_names[0]).astype(np.float64)
print(a.shape)
#print(blur1.shape)