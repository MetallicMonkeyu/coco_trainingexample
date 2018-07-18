import json
import os
import re
import string
import cv2
import numpy as np
#people category_id:1

img_path_string = '/home/data/MyData/train2017/'
pics=os.listdir('/home/data/shengjia/new_output')
def array_two(list1,step):
    new_list = []
    for i in range(0,len(list1)):
        list1[i] = int(list1[i])
    for i in range(0, len(list1),step):
        new_list.append(tuple(list1[i:i+step]))
    return new_list

def addzero(num):
    length = 12-len(str(num))
    string = str(0)*length+str(num)
    new_string = string + '.jpg'
    return new_string.strip('\'')

def convert_contours(contour_list):
    image_contour = contour_list
    output_numpy = []
    outter_list = []
    for i in range(0, len(image_contour)):
        for j in range(0, len(image_contour[i])):
           # print (image_474[i][j])
            image_contour[i][j] = [list(image_contour[i][j])]
            output_numpy.append(image_contour[i][j])
        outter_list.append(output_numpy)
    numpy_array = np.array(outter_list)
    return numpy_array

def load_annotation_first(path):
    f = open(path)
    loaded = json.load(f)
    annotations = loaded["annotations"]
    #print ("opened json")    
    for i in range(0, len(annotations)):
        dic = {}    
        id_num = annotations[i]["image_id"]
        contours_num = len(annotations[i]["segmentation"])
        category_id = annotations[i]["category_id"]
       # src = cv2.imread(img_path_string+addzero(id_num))
        if (category_id == 1)and("segmentation" in (annotations[i]))and(isinstance(annotations[i]["segmentation"],list)): 
            output_list = []
            for j in range (0, contours_num):
                coordi = (annotations[i]["segmentation"])[j]
                output_list.append(array_two(coordi,2))
            dic[addzero(id_num)] = convert_contours(output_list)
            for key,value in dic.items():
         #      src = cv2.imread(img_path_string+addzero(id_num))
               # dst = src.copy()
                
                
                contours = value
                src = cv2.imread(img_path_string+addzero(id_num))
                if os.path.exists('/home/data/shengjia/new_output/'+key):
                    con = cv2.imread('/home/data/shengjia/new_output/'+key)
                    h,w = con.shape[:2]
                else:
                    h,w = src.shape[:2]
                    con = np.zeros((h,w,3), np.uint8)
                    con = ~con
                xMin = 99999
                yMin = 99999
                xMax = 0
                yMax = 0
                for k in range(0,len(contours)):
                    (x_,y_,w_,h_)=cv2.boundingRect(contours[k])
                    if xMin>x_:
                        xMin = x_
                    if yMin>y_:
                        yMin = y_
                    if xMax<x_+w_:
                        xMax = x_+w_
                    if yMax<y_+h_:
                        yMax = y_+h_
                seg_h = yMax-yMin
                seg_w = xMax-xMin
                if float(seg_h)*float(seg_w)>float(0.2)*float(h)*float(w):
                    #print(float(seg_h)*float(seg_w),(0.2)*float(h)*float(w))
                    for z in range(0,len(contours)):
                        cv2.drawContours(con, contours,z, (0,0,0),thickness=-1)
                        #cv2.circle(con,(xMin,yMin),5,(0,0,255),-1)
                        #cv2.circle(con,(xMax,yMax),5,(0,255,0),-1)
                        #cv2.drawContours(dst,contours,-1,(255,0,0)
                    #cv2.imshow('window1',con)
                    #cv2.imshow('window2',src)
                    #cv2.waitKey(0)
                    cv2.imwrite('/home/data/shengjia/new_output/'+key,con)
                    cv2.imwrite('/home/data/shengjia/human_output/'+key,src)
                    print(key)

load_annotation_first('/home/data/MyData/instances_train2017.json')
'''
def draw_contours(output_path):
    new_dict = return_list()
    for k,v in new_dict.items():
        src = cv2.imread(img_path_string+k)
        dst = src.copy()
        contours = v
   # print(contours)
        stencil = np.zeros(dst.shape).astype(dst.dtype)
        cv2.fillPoly(stencil,contours,(255,255,255))
        cv2.drawContours(dst, contours,-1, (255,0,0),3)
        cv2.fillPoly(dst, contours, color = (128,128,192))
        result = cv2.bitwise_and(dst, stencil)
        cv2.imwrite(output_path+k,result)

'''
#draw_contours('/home/data/shengjia/contoured_human/') 

#load_annotation_first('/home/data/MyData/instances_train2017.json')
