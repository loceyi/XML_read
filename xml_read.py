#!/usr/bin/python
# -*- coding: UTF-8 -*-
# get annotation object bndbox location
import os
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
def GetAnnotBoxLoc(ObjBndBoxSet,AnotPath):#AnotPath VOC标注文件路径
    '''
    AnotPath:路径
    ObjBndBoxSet：包含各个类和相应位置的字典的数据
    '''
    tree = ET.ElementTree(file=AnotPath) #打开文件，解析成一棵树型结构
    root = tree.getroot()#获取树型结构的根
    ObjectSet=root.findall('object')#找到文件中所有含有object关键字的地方，这些地方含有标注目标
     #以目标类别为关键字，目标框为值组成的字典结构
    for Object in ObjectSet:
        ObjName=Object.find('name').text
        BndBox=Object.find('robndbox')
        # if className in ObjName:

        cx = int(float(BndBox.find('cx').text))#-1 #-1是因为程序是按0作为起始位置的
        cy = int(float(BndBox.find('cy').text))#-1
        w  = int(float(BndBox.find('w').text))#-1
        h  = int(float(BndBox.find('h').text))#-1
        angle =float(BndBox.find('angle').text)#-1
        BndBoxLoc=[cx,cy,w,h,angle]
        if ObjName in ObjBndBoxSet:
            ObjBndBoxSet[ObjName].append(BndBoxLoc)#如果字典结构中含有这个类别了，那么这个目标框要追加到其值的末尾
        else:
            ObjBndBoxSet[ObjName]=[BndBoxLoc]#如果字典结构中没有这个类别，那么这个目标框就直接赋值给其值吧
    return ObjBndBoxSet
    ##get object annotation bndbox loc end

#需要遍历的目录
ShowDir = 'D:/CV数据集/DJI精简数据集_result_750_20201201/DJI精简数据集B'

#定义listdir函数
def listdir(path):
    list_name=[]
    #遍历目录下文件，添加到list，并返回
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        list_name.append(file_path)
    return list_name


if __name__== '__main__':
    #获取ShowDir中所有的文件
    list_dir = listdir(ShowDir)
    list_dir_xml=[]
    ObjBndBoxSet={}
    #包含xxCOMxx字符，且后缀名为.csv的文件
    for i in range(len(list_dir)):
        if list_dir[i].find(".xml") > 0 :
            # 读取文件夹中的xml文件
            list_dir_xml.append(list_dir[i])
    for file in list_dir_xml:

        ObjBndBoxSet=GetAnnotBoxLoc(ObjBndBoxSet,file)
#         保存了路径下所有xml里面各个类别的车辆名称，及其对应的旋转框信息。



##get object annotation bndbox loc start

def display(objBox,pic):
    img = cv2.imread(pic)
    for key in objBox.keys():
        for i in range(len(objBox[key])):
            cv2.rectangle(img, (objBox[key][i][0],objBox[key][i][1]), (objBox[key][i][2], objBox[key][i][3]), (0, 0, 255), 2)
        cv2.putText(img, key, (objBox[key][i][0],objBox[key][i][1]), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
        cv2.imshow('img',img)
        cv2.imwrite('display.jpg',img)
        cv2.waitKey(0)


# if __name__== '__main__':
#     pic = r"./VOCdevkit/VOC2007/JPEGImages/000282.jpg"
# ObjBndBoxSet=GetAnnotBoxLoc(r"./VOCdevkit/VOC2007/Annotations/000282.xml")
# print(ObjBndBoxSet)
# display(ObjBndBoxSet,pic)