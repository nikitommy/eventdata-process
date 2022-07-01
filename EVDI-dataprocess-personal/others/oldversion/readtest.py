import numpy as np
import imageio
import cv2, glob, os



# pic_path = './GoPro/blur/000026.png'
# a = cv2.imread(pic_path)
#t1,x1,y1,p1 = np.loadtxt('./GoPro/out.txt',unpack=True)
a = np.load('reblur0021-reblur0022.npz', allow_pickle=True)
b = a['blur1']
# picgray_dir_names = sorted(glob.glob(os.path.join('./GoPro/blurgray', '*')))
start = a['exp_start1']
end = a['exp_end1']
start2 = a['exp_start2']
end2 = a['exp_end2']
event = a['events'].item()
m = event['t']
blur1 = a['blur1'] 
print(m.shape)
#t1,x1,y1,p1 = np.loadtxt('./GoPro/event/000027.txt',unpack=True)
#a = cv2.imread(picgray_dir_names[0]).astype(np.float64)
#print(b.shape)
# print(m.shape)
def editnpz(filename,name,value):
    filedic = dict(np.load(filename, allow_pickle=True))
    filedic[name] = value
    np.savez(filename, **filedic)
# editnpz('reblur0021-reblur0022.npz')
# c = np.load('reblur0021-reblur0022.npz', allow_pickle=True)
# print(c['exp_start1'])

# arr=np.random.randn(6)*5
# print(arr)
# a,_=np.modf(arr)
# b = (a*1e7).astype(int)
# print(b)

# img_dir_names = sorted(glob.glob(os.path.join('./GoPro/blur', '*')))
# def custombasename(fullname):
#     a = os.path.basename(os.path.splitext(fullname)[0])
#     a = np.array(a)  
#     a = (a.astype(float)*1e7).astype(int)
#     return a

# def basename(fullname):
#     a = os.path.basename(os.path.splitext(fullname)[0])
#     return a

# filename = basename(img_dir_names[0]) + '-' + basename(img_dir_names[1])
# z = custombasename(img_dir_names[-1])
# print(img_dir_names[0].dtype)