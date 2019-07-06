'''
TF object detection format to darknet format 
annotation converter

TF object detection format =>  

filename, class1,xmin,ymin,xmax,ymax
filename, class2,xmin,ymin,xmax,ymax
.
.
.
filename, class5,xmin,ymin,xmax,ymax


Darknet format =>

filename  xmin,ymin,xmax,ymax,class1  xmin,ymin,xmax,ymax,class2  . . .  xmin,ymin,xmax,ymax,class5  


** NOTE **
Provide the appropriate mapping of classes with numbers.
all output images should in common format thus using 'jpg'


'''



import argparse
 
    
import cv2,os
import json
import pandas as pd
import numpy as np
    
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", default = 'tf_object_format.csv',
	help=" directory containing the json file ")

ap.add_argument("-im", "--input_image", default = 'images',
	help=" input the images directory ")

ap.add_argument("-io", "--output_image", default = 'output_images',
	help=" output iamges sequential format in common extension ")

ap.add_argument("-o", "--output", default = 'darknet_anno.txt',
	help=" output file name")
args = vars(ap.parse_args())

if not os.path.exists(args['output_image']):
    os.mkdir(args['output_image'])

    
df =  pd.read_csv(args['input'])

fnames = df.filename.unique()

# mapping of class with numbers

dic = {"figure":1, "legend":2,"title":3,"x_label":4,"y_label":5,"x_title":6,"y_title":0}

ll = []
cc = 0
qq = []
for i in fnames:
    gg = df[i == df.filename]
    li = []
    
    li.append( args['output_image']+"/"+str(cc)+".jpg")
    img = cv2.imread(args['input_image']+"/"+i)
    cv2.imwrite(args['output_image']+"/"+str(cc)+".jpg",img)
    
    for h in range(len(gg)):
        
        t = gg.iloc[h]
#         oo = []
        li.append(str(t.xmin)+","+str(t.ymin)+","+str(t.xmax)+","+str(t.ymax)+","+ str(dic[t['class']]))
        
        # tf_format
#         oo.append(args['output_image']+"/"+str(cc)+".jpg")
#         oo.append(t['class'])
#         for q in [t.xmin,t.ymin,t.xmax , t.ymax]:
#             oo.append(q)
        
#         qq.append(oo)
    ll.append(li)
    cc+=1
    
# generate dataset for yolo network

pp = pd.DataFrame(ll)
pp.columns = np.arange(0,len(pp.columns))
pp.to_csv(args['output'],index=False,header=False,sep=" ")