


from openpyxl import Workbook
import numpy as np


mat = np.empty([40,50], dtype = float)
list=[]
with open("C:/Users/lenovo/Desktop/1.txt", "r") as f:  # 打开文件
    for line in f.readlines():

        line=line.strip('\n')  # 读取文件

        if line  != '' and line != '\n':

            list.append(line)

k=0
m=0
for i in list:

    if 'the row is' in i:
        row=k
        k+=1
        col=m
        if row==39:

            k=0
            m+=1

        print(row,col)

    mat[row][col] = 0

    if 'vcomp hi' in i:

        element=int(i[-2:], 16)*5.62
        mat[row][col] =element

    else:

        pass




shujuzhongsu=120
tezhengshu=2
def save(data,path):
    wb = Workbook()
    ws = wb.active # 激活 worksheet
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        row = []
        for j in range(l):
            row.append(data[i,j])
        ws.append(row)
    wb.save(path)

data = mat

save(data,"888.xlsx")





print(list)