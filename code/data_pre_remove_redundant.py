# -*- coding:utf-8 -*-

import time
import re
import pickle

import os

def file_name(file_dir):
    file_names ={}
    for root, dirs, files in os.walk(file_dir):
        if len(files)!=0:
            froot = re.findall('\d+_\d+', root)[0]
            file_names[froot]=[]
            for f in files:
                if len(re.findall('txt',f))!=0:
                    fname=root+'\\'+f
                    file_names[froot].append(fname)  #当前目录路径
    return file_names
        #print(dirs) #当前路径下所有子目录
        #print(files) #当前路径下所有非目录子文件

r=0
logcat=[]
event = []
files=file_name('E:\code\data\com.example.myfristandroid')

# for f in files:

logcat = pickle.load(open('E:\code\data\com.example.myfristandroid\\'+'950_1'+'\logcat.pkl'))
for l in logcat:
    print l['SyscTime'],l