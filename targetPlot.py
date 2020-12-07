#!/usr/bin/python
# -*- coding: UTF-8 -*-
# get annotation object bndbox location
import os

# 该函数用于在图片中搜寻特点类别的车辆，并将其画出来，生成一个150*150的照片
'''
家用轿车-Car
翻斗车-Dump_Truck
皮卡-Pickup
面包车-Van  
挖掘机-Excavator
普通货车-Truck
油罐车-Tanker
搅拌车-Agitator truck
公交车-Bus
半挂式货车-Semi-trailer truck
推土机-Bulldozer
吊车-Crane
校车-School bus
警车-Police car
消防车-Fire Truck
救护车-Ambulance
'''
import cv2
try:
    import xml.etree.cElementTree as ET #解析xml的c语言版的模块
except ImportError:
    import xml.etree.ElementTree as ET
import os
import numpy as np

import math

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


def rect_loc(xc, yc, height, width ,angle):
    '''
    height为宽（短边），bottom为长（长边）
    '''

    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    x0 = (width/2)*cos_a - (height / 2) * sin_a +xc
    y0 = -(width/2)*sin_a- height / 2 * cos_a + yc
    x1 = -(width/2)*cos_a - (height / 2) * sin_a +xc
    y1 = (width/2)*sin_a- height / 2 * cos_a + yc
    x2 = -(width/2)*cos_a + (height / 2) * sin_a +xc
    y2 = (width/2)*sin_a + height / 2 * cos_a + yc
    x3 = (width/2)*cos_a + (height / 2) * sin_a +xc
    y3 = -(width/2)*sin_a + height / 2 * cos_a + yc

    return np.array(
        [
            [x0, y0],
            [x1, y1],
            [x2, y2],
            [x3, y3],
        ]
    ).astype(np.int)


def display(objBox,pic,cutWidth):
    img = cv2.imread(pic)

    rect = np.int0(objBox) # 取整

    # 右下角坐标(x1,y1)
    coordinate1 = rect[0]
    # 左下角坐标(x2,y2)
    coordinate2 = rect[1]
    # 左上角坐标(x3,y3)
    coordinate3 = rect[2]
    # 右上角坐标(x4,y4)
    coordinate4 = rect[3]
    centerPoint=list(map(int,[(coordinate1[0]+coordinate3[0])/2,(coordinate1[1]+coordinate3[1])/2]))
    point_size = 1
    point_color = (0, 0, 255) # BGR
    thickness = 4 #  0 、4、8

    # 此处省略得到坐标的过程，coordinates存放坐标
    # 格式为：coordinates=[[x1,y1],[x2,y2],[x3,y3],...,[xn,yn]]


    color=(255, 0, 0)
    thickness=1
    cv2.circle(img, (rect[0][0],rect[0][1]), point_size, point_color, thickness)
    cv2.line(img, tuple(rect[0]), tuple(rect[1]), color, thickness)
    cv2.line(img, tuple(rect[1]), tuple(rect[2]), color, thickness)
    cv2.line(img, tuple(rect[2]), tuple(rect[3]), color, thickness)
    cv2.line(img, tuple(rect[3]), tuple(rect[0]), color, thickness)

    # cv2.rectangle(img, (coordinate1,coordinate2), (coordinate3,coordinate4), (0, 0, 255), 2)
    # cv2.putText(img, key, (objBox[key][i][0],objBox[key][i][1]), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
    # cv2.resizeWindow("enhanced", 300, 400)
    cv2.namedWindow('img',cv2.WINDOW_NORMAL)
    # print([(centerPoint[1]-75),(centerPoint[1]+75),(centerPoint[0]-75),(centerPoint[0]+75)])
    # DJI 3956 5280
    if 0<(centerPoint[1]-cutWidth)<3956 and 0<(centerPoint[1]+cutWidth)<3956 and 0<(centerPoint[0]+cutWidth)<5280 and 0<(centerPoint[0]-cutWidth)<5280:

        img=img[(centerPoint[1]-cutWidth):(centerPoint[1]+cutWidth),(centerPoint[0]-cutWidth):(centerPoint[0]+cutWidth)]
        cv2.imshow('img',img)
        cv2.imwrite('display.jpg',img)
        cv2.waitKey(0) #暂停程序，等待一个按键输入”
    else:
        pass



def GetAnnotBoxLoc(AnotPath,className):#AnotPath VOC标注文件路径
    '''
    AnotPath:路径
    ObjBndBoxSet：包含各个类和相应位置的字典的数据
    '''
    tree = ET.ElementTree(file=AnotPath) #打开文件，解析成一棵树型结构
    root = tree.getroot()#获取树型结构的根
    ObjectSet=root.findall('object')#找到文件中所有含有object关键字的地方，这些地方含有标注目标
    ObjBndBoxSet={}
    #以目标类别为关键字，目标框为值组成的字典结构
    for Object in ObjectSet:
        ObjName=Object.find('name').text
        BndBox=Object.find('robndbox')
        if className in ObjName:

            cx = int(float(BndBox.find('cx').text))#-1 #-1是因为程序是按0作为起始位置的
            cy = int(float(BndBox.find('cy').text))#-1
            w  = int(float(BndBox.find('w').text))#-1
            h  = int(float(BndBox.find('h').text))#-1
            angle =float(BndBox.find('angle').text)#-1
            BndBoxLoc=[cx,cy,w,h,angle]
            BndBoxLoc_4point=rect_loc( BndBoxLoc[0],  BndBoxLoc[1], BndBoxLoc[2], BndBoxLoc[3],BndBoxLoc[4])
            if ObjName in ObjBndBoxSet:
                ObjBndBoxSet[ObjName].append(BndBoxLoc_4point)#如果字典结构中含有这个类别了，那么这个目标框要追加到其值的末尾
            else:
                ObjBndBoxSet[ObjName]=[BndBoxLoc_4point]#如果字典结构中没有这个类别，那么这个目标框就直接赋值给其值吧

    return ObjBndBoxSet
    ##get object annotation bndbox loc end

#需要遍历的目录
ShowDir = 'D:\CV_DATASET\DJI_result_750_20201201\DJIB'

#定义listdir函数
def listdir(path):
    list_name=[]
    #遍历目录下文件，添加到list，并返回
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        list_name.append(file_path)
    return list_name

'''
家用轿车-Car
翻斗车-Dump_Truck
皮卡-Pickup
面包车-Van  
挖掘机-Excavator
普通货车-Truck
油罐车-Tanker
搅拌车-Agitator truck
公交车-Bus
半挂式货车-Semi-trailer truck
推土机-Bulldozer
吊车-Crane
校车-School bus
警车-Police car
消防车-Fire Truck
救护车-Ambulance
'''
if __name__== '__main__':
    # 在图片中找某一类车型
    classname='吊车-Crane'
    list_dir = listdir(ShowDir)
    list_dir_xml=[]
    cutWidth=int(300/2) #设置切出来含目标的图片大小，150为正方形长度

    #读取文件夹中xml文件的目录
    for i in range(len(list_dir)):
        if list_dir[i].find(".xml") > 0 :
            # 读取文件夹中的xml文件
            list_dir_xml.append(list_dir[i])
    for file in list_dir_xml:
        # 获取各个xml里面对应类别目标的坐标
        ObjBndBoxSet=GetAnnotBoxLoc(file, classname)
        #获取该图片中全部包含classname的label
        if classname in ObjBndBoxSet:
            # 判断该图片是否有该类型的目标，如果没有则去下一个图找
            for i in range(len(ObjBndBoxSet[classname])):

                ObjBndBox=ObjBndBoxSet[classname][i] #取每张图片第一个目标作为展示，该函数只返回特定类别的信息
                # display(ObjBndBox,file.replace('.xml','_effect.JPG'),cutWidth)
                display(ObjBndBox,file.replace('xml','JPG'),cutWidth)

        else:

            pass
#         保存了路径下所有xml里面各个类别的车辆名称，及其对应的旋转框信息。


##get object annotation bndbox loc start




# if __name__== '__main__':
#     pic = r"./VOCdevkit/VOC2007/JPEGImages/000282.jpg"
# ObjBndBoxSet=GetAnnotBoxLoc(r"./VOCdevkit/VOC2007/Annotations/000282.xml")
# print(ObjBndBoxSet)
# display(ObjBndBoxSet,pic)