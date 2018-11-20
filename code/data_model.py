# -*- coding:utf-8 -*-

import re
import pickle
android_event_type_c = {
    'TYPE_WINDOW_STATE_CHANGED':'g',
    'TYPE_WINDOW_CONTENT_CHANGED':'b',
    'TYPE_VIEW_FOCUSED':[0.8,0.1,0.8],
    'TYPE_VIEW_SCROLLED':'k',
    'TYPE_VIEW_CLICKED':'c',
    'TYPE_VIEW_TEXT_SELECTION_CHANGED':[0.4,0.4,0.4],
    'TYPE_VIEW_ACCESSIBILITY_FOCUSED':[0.1,0.8,0.1],
    'TYPE_VIEW_TEXT_CHANGED':[0.4,0.1,0.1],
    'TYPE_VIEW_SELECTED':[0.1,0.1,0.4],
    'TYPE_NOTIFICATION_STATE_CHANGED':'y',
    'TYPE_ANNOUNCEMENT':[0.8,0.8,0.8],
    'TYPE_VIEW_ACCESSIBILITY_FOCUS_CLEARED':[0.8,0.4,0.8],
    'TYPE_VIEW_LONG_CLICKED':[0.5,0,0.5],
    'TYPE_VIEW_HOVER_ENTER':[0.8,0.1,0.1],
    'TYPE_VIEW_HOVER_EXIT':[0.8,0.8,0.1],
}

android_event_type = {
    'TYPE_WINDOW_STATE_CHANGED':[],
    'TYPE_WINDOW_CONTENT_CHANGED':[],
    'TYPE_VIEW_FOCUSED':[],
    'TYPE_VIEW_SCROLLED':[],
    'TYPE_VIEW_CLICKED':[],
    'TYPE_VIEW_TEXT_SELECTION_CHANGED':[],
    'TYPE_VIEW_ACCESSIBILITY_FOCUSED':[],
    'TYPE_VIEW_TEXT_CHANGED':[],
    'TYPE_VIEW_SELECTED':[],
    'TYPE_NOTIFICATION_STATE_CHANGED':[],
    'TYPE_ANNOUNCEMENT':[],
    'TYPE_VIEW_ACCESSIBILITY_FOCUS_CLEARED':[],
    'TYPE_VIEW_LONG_CLICKED':[],
    'TYPE_VIEW_HOVER_ENTER':[],
    'TYPE_VIEW_HOVER_EXIT':[]
}

android_logcat_type_c = {
    'V':'g',
    'D':'r',
    'I':'c',
    'W':'y',
    'E':'k',
    'F':'w',
    'S':'m'
}

android_logcat_type = {
    'V':[],
    'D':[],
    'I':[],
    'W':[],
    'E':[],
    'F':[],
    'S':[]
}

import os
import matplotlib.pyplot as plt
import numpy as np

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
files=file_name('.\data\com.example.myfristandroid')


# for f in files:
logcat_file = open('.\data\com.example.myfristandroid\\'+'695_1'+'\logcat.pkl',"rb")
event_file = open('.\data\com.example.myfristandroid\\'+'695_1'+'\event.pkl',"rb")
logcat_list = pickle.load(logcat_file)
event_list = pickle.load(event_file)

for e in event_list:
    android_event_type[e['EventType']].append(e)
for l in logcat_list:
    android_logcat_type[l['priority']].append(l)

char_zhi = min(event_list[0]['SyscTime'],logcat_list[0]['SyscTime'])

fig = plt.figure('fig')
i = 200

for a in android_logcat_type:
    logcat_time_list = [float(x['SyscTime']-char_zhi) for x in android_logcat_type[a]]
    if len(logcat_time_list)>0:
        plt.scatter(logcat_time_list,[100 for x in range(i,i+len(logcat_time_list))],c=android_logcat_type_c[a],marker='o',label=a)
        i+=100
for a in android_event_type:
    event_time_list = [float(x['SyscTime'] - char_zhi) for x in android_event_type[a]]
    if len(event_time_list)>0:
        plt.scatter(event_time_list,[x for x in range(i,i+len(event_time_list))],c=android_event_type_c[a],marker='v',label=a)
        i+=100
plt.title("data")
# plt.xlim(110000,125000)
# plt.ylim(0,200)
plt.xlabel("time")
plt.ylabel("count")
plt.legend(loc='lower right')
plt.show()
