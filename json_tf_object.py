'''
Read the json file in the default 'json' direcory and save a csv file 
that combines all json file data in the format

"filename","class","xmin","ymin","xmax","ymax"

'''


import argparse
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", default = 'test',
	help=" directory containing the json file ")
ap.add_argument("-o", "--output", default = 'tf_object_format.csv',
	help=" output file name")
args = vars(ap.parse_args())

import cv2,os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

os.chdir(args['dir'])

print("\t\t json to TF object detection Notation")
print("filename","class","xmin","ymin","xmax","ymax")

def minify(x1,x2,y1,y2):
    if x1 < x2:
        if y1 < y2:
            return (x1,y1,x2,y2)
        else:
            return (x1,y2,x2,y1)
    else:
        if y1 < y2 :
            return (x2,y1,x1,y2)
        return (x2,y2,x1,y1)

li = []
for j in os.listdir('.'):
    if j.split('.')[-1]=="json":
        name = j
        f = open(name) 
        data = json.load(f)
        for i in data["shapes"]:
            x1,y1 = i['points'][0]
            x2,y2 = i['points'][1]
            
            x1,y1,x2,y2 = map(int,(x1,y1,x2,y2))
            x1,y1,x2,y2 = minify(x1,x2,y1,y2)
            li.append([data["imagePath"],i["label"],x1,y1,x2,y2])
        f.close()

df = pd.DataFrame(li)
print(df.head(3))
# reaname columns

df.columns = ["filename","class","xmin","ymin","xmax","ymax"]
os.chdir("..")
df.to_csv(args['output'],index = False)
print("total files read %d "%(len(df.groupby('filename'))))