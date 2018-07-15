import json
import os
import re
import string
import cv2
import numpy as np
#people category_id:1
pics=os.listdir('/home/data/MyData/train2017')
img_path_string = '/home/data/MyData/train2017/'

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

def load_annotation_first(path):
    f = open(path)
    loaded = json.load(f)
    annotations = loaded["annotations"]

    for i in range(0, len(annotations)):
        dic = {}
        id_num = annotations[i]["image_id"]
        contours_num = len(annotations[i]["segmentation"])
        category_id = annotations[i]["category_id"]
        src = cv2.imread(img_path_string+addzero(id_num))
        h,w = src.shape[:2]
        if ("segmentation" in (annotations[i]))and((category_id == 1))and(isinstance(annotations[i].get("segmentation"),list)):
            output_list = []
            #print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            #print(annotations[i])
            #print(annotations[i]["segmentation"])
                #print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                #print(img_path_string+addzero(id_num))				
            for j in range (0, contours_num):
                  #  print(type(annotations[i].get("segmentation")))
                coordi = (annotations[i].get("segmentation"))[j]
                output_list.append(array_two(coordi,2))
                   # print (category_id,contours_num,annotations[i]["segmentation"])
            dic[addzero(id_num)] = output_list 
            for key,value in dic.items():
                dic[key] = convert_contours(value,key)
            for k,v in dic.items():        
                dst = src.copy()
                contours = v
                con = np.zeros((h, w,3), np.uint8)
                threArea = []
                xMin = 99999
                yMin = 99999
                xMax = 0
                yMax = 0
                for i in range(0,len(contours)):
                    (x,y,w,h)=cv2.boundingRect(contours[i])
                    threArea.append(x,y,w,h)
		    if xMin>x:
                        xMin = x
                    if yMin>Y:
                        yMin = y
                    if xMax<x+w:
                        xMax = x+w
                    if yMax<y+h:
                        yMax = y+h
                seg_h = yMax-yMin
                seg_w = xMax=xMin
				if seg_h*seg_w>0.05*h*w:
                    for i in range(0,len(contours)):
                        cv2.drawContours(con, contours,i, (255,255,255),thickness=-1)
                        cv2.imshow('con',con)
                        cv2.waitKey(0)

                    #cv2.floodFill(con,mask,seed_point,(255,255,255))
                    #cv2.imshow('confill',con)
                    #cv2.waitKey(0)
                #cv2.drawContours(dst, contours,-1, (255,0,0),3)
                #cv2.imshow('mask',mask)
                #cv2.imshow('dst',dst)
                #cv2.waitKey(0)
    return dic              
# print (output_list)
#load_annotation_first('/home/data/MyData/instances_train2017.json')


#converting each contours into numpy array
def convert_contours(contour_list,key):
    image_contour = contour_list
    #print('image_contour: ',image_contour)
    #print('image_contour!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    output_numpy = []
    outter_list = []
    print('len(image_contour): ',len(image_contour))
    for i in range(0, len(image_contour)):
        for j in range(0, len(image_contour[i])):
            image_contour[i][j] = [list(image_contour[i][j])]
            output_numpy.append(image_contour[i][j])
        outter_list.append(output_numpy)
    numpy_array = np.array(outter_list)
    #print(len(numpy_array))
    return numpy_array


#Contouring method-2
'''
def drawlines(path,coordinates):
    strPath = path
    coor_list = coordinates
    img = cv2.imread(strPath) 
	
    for i in range(0, len(coor_list)-1):		
        cv2.line(img, coor_list[i],coor_list[i+1],(255,0,0),10)
    cv2.imwrite('./output/000000000474.jpg',img) 
#drawlines()	
'''
#test version 1 for filling color
'''
def return_list():
    image_contour = load_annotation_first('/home/data/MyData/instances_train2017.json')
    for key,value in image_contour.items():
        image_contour[key] = convert_contours(value,key)
    return image_contour
        src = cv2.imread(img_path_string+key)
        dst = src.copy()
        cv2.drawContours(dst, image_contour[key],-1, (255,0,0),3)
        cv2.imshow('test',dst)
        cv2.waitKey()

def get_image_size(img_path):
    src  = cv2.imread(img_path)
    area = src.cols*src.rows
    return area

def draw_contours(output_path):
    new_dict = return_list()
    area = 0
    #for k,v in new_dict.items():        
        # for i in range(0,len(v)):
        #     area = area + cv2.contourArea(list[i])
        #src = cv2.imread(img_path_string+k)
        #dst = src.copy()
        #contours = v
        #print('length: ',len(contours[0]))
        #print(contours,'\n')
        #stencil = np.zeros(dst.shape).astype(dst.dtype)
        #cv2.drawContours(dst, contours,-1, (255,0,0),3)
        #for i in range(0,len(contours)):
        #print(list(contours[i]))
        #cv2.fillPoly(stencil,contours,(255,255,255))
        #cv2.fillPoly(dst, contours, color = (128,128,192))
        #cv2.imshow('test',dst)
        #cv2.waitKey(0)
        #result = cv2.bitwise_and(dst, stencil)
        #cv2.imwrite(output_path+k,result)
        #cv2.imshow('test1',result)
        
return_list()
#draw_contours('/home/data/shengjia/contoured_human/')
'''
