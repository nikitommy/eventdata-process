import numpy as np
import cv2, glob, os 

pic_path = './GoPro/blur'
picgray_path = './GoPro/blurgray'
pic_dir_names = sorted(glob.glob(os.path.join(pic_path, '*')))
picgray_dir_names = sorted(glob.glob(os.path.join(picgray_path, '*')))
#pic_dir_names = sorted(glob.glob(os.path.join(event_path, '*')))

def color2gray(color_img):
    size_h, size_w, channel = color_img.shape
    gray_img = np.zeros((size_h, size_w), dtype=np.uint8)
    for i in range(size_h):
        for j in range(size_w):
            gray_img[i, j] = round((color_img[i, j, 0]*29.9 + color_img[i, j, 1]*58.7 +\
                color_img[i, j, 2]*11.4)/100)
    return gray_img

def save_pic(pic_gray,picgray_path,pic_dir_names):
    cv2.imwrite(os.path.join(picgray_path, '', os.path.basename(pic_dir_names)),pic_gray,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])

if __name__ == '__main__':
    pic = cv2.imread(pic_dir_names[0])
    pic_gray = color2gray(pic)
    cv2.imwrite(os.path.join(picgray_path, '', os.path.basename(pic_dir_names[0])),pic_gray,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    #cv2.imwrite('GoPro/blurgray/graypic.png',pic_gray,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    