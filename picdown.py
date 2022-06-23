#调用所需的包
import cv2
from imgprocess import save_pic
 
#读取原始图像的信息
img0 = cv2.imread('GOPR0854_11_00/GOPR0854_11_00/000001.png')   #读取图像
img1 = cv2.resize(img0, fx = 0.9, fy = 0.9, dsize = None)  #调整图像大小
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)              #将图像转化为灰度图像
 
img12 = cv2.pyrDown(img1)
print(img12.shape)                                  #高斯滤波下采样得到高斯金字塔
cv2.imwrite('down12.png',img12,[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
