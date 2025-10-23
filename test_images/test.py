# import cv2
# img = cv2.imread("1.jpg", 1)
#
# # cv2.namedWindow('image',cv2.WINDOW_AUTOSIZE)
# # cv2.imshow('image', img)
# # if cv2.waitKey(5000) == ord('0'):
# #     cv2.imwrite("back.png",img)
# # cv2.destroyAllWindows()
# # print(img.shape[0])
# # print(img.shape[1])
# # print(img.shape[2])
#
# img = cv2.line(img, (0,0), (100,100), (0,255,0), 3)
# cv2.imshow('img', img)
# # while 1:
# #     if cv2.waitKey(0) == ord('q'):
# #         break
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
# # img = cv2.imread('1.jpg')
# # img = cv2.ellipse(img, (100, 100),(100,80),90,0,180, (0, 255, 255), -1)
# # cv2.imshow('img', img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# cap = cv2.VideoCapture(0)
# print(type(cap))
# cap.release()

# import numpy
# import cv2
# cap=cv2.VideoCapture(2)
# while cap.isOpened():
#     ret,frame=cap.read()
#     cv2.imshow('img',frame)
#     if cv2.waitKey(1)==ord('q'):
#         break
# cv2.destroyAllWindows()
# cap.release()
#
# import cv2
# img=cv2.imread('1.jpg')
# img1=cv2.flip(img,-1) #-1 水平垂直翻转
# img2=cv2.flip(img,0) #垂直翻转
# img3=cv2.flip(img,2) #水平翻转
# cv2.imshow('img1',img1)
# cv2.imshow('img2',img2)
# cv2.imshow('img3',img3)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# '''
# BGR2GRAY
# '''
# from colorsys import hsv_to_rgb
#
# import cv2
# img=cv2.imread('1.jpg')
# gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# hsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
# cv2.imshow('img',img)
# cv2.imshow('gray',gray)
# cv2.imshow('hsv',hsv)
# print(img.shape)
# print(gray.shape)
# print(hsv.shape)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np
cap=cv2.VideoCapture(0)
while 1:
    ret,frame=cap.read() #读取一帧图像(ret:是否成功,frame:画面数据)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # 将BGR2hsv
    lower_blue=np.array([0,20,40]) #H通道(78-99):对应蓝色的色调范围,S通道(43-255):排除低饱和度(接近灰色)的区域,V通道(46-255):排除过暗区域
    upper_blue=np.array([25,160,255])
    mask=cv2.inRange(hsv,lower_blue,upper_blue)
    res=cv2.bitwise_and(frame,frame,mask=mask) #使用逻辑与操作将掩膜应用在原来的图像上,构成res图像
    cv2.imshow('frame',frame) #原图
    cv2.imshow('mask',mask)  #掩码,(蓝色为白色)
    cv2.imshow('res',res)   #提取蓝色区域
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows() #撕毁窗口
cap.release() #释放摄像头