# -*- coding:utf-8 -*-

import time
import re
import pickle
android_event_type = ['TYPE_WINDOW_STATE_CHANGED', 'TYPE_WINDOW_CONTENT_CHANGED', 'TYPE_VIEW_FOCUSED', 'TYPE_VIEW_SCROLLED', 'TYPE_VIEW_CLICKED', 'TYPE_VIEW_TEXT_SELECTION_CHANGED', 'TYPE_VIEW_ACCESSIBILITY_FOCUSED', 'TYPE_VIEW_TEXT_CHANGED', 'TYPE_VIEW_SELECTED', 'TYPE_NOTIFICATION_STATE_CHANGED', 'TYPE_ANNOUNCEMENT', 'TYPE_VIEW_ACCESSIBILITY_FOCUS_CLEARED', 'TYPE_VIEW_LONG_CLICKED', 'TYPE_VIEW_HOVER_ENTER', 'TYPE_VIEW_HOVER_EXIT']

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
files=file_name('D:\Github\S-CAT\code\data\com.example.myfristandroid')

print(android_event_type)

# for f in files:
logcat_file = open('D:\Github\S-CAT\code\data\com.example.myfristandroid\\'+'787_1'+'\logcat.pkl',"rb")
event_file = open('D:\Github\S-CAT\code\data\com.example.myfristandroid\\'+'787_1'+'\event.pkl',"rb")
logcat_list = pickle.load(logcat_file)
event_list = pickle.load(event_file)
print(event_list)
print(logcat_list)
char_zhi = min(event_list[0]['SyscTime'],logcat_list[0]['SyscTime'])

event_time_list = [float(x['SyscTime']-char_zhi) for x in event_list]
logcat_time_list = [float(x['SyscTime']-char_zhi) for x in logcat_list]
#print(event_time_list[0])
print(logcat_time_list)
fig = plt.figure('fig')
plt.scatter(logcat_time_list,[x for x in range(len(logcat_time_list))],c='r',marker='o',label="logcat")
plt.scatter(event_time_list,[x for x in range(len(event_time_list))],c='g',marker='v',label="event")
plt.title("data")
# plt.xlim(110000,125000)
# plt.ylim(0,200)
plt.xlabel("time")
plt.ylabel("count")
plt.legend(loc='lower right')
plt.show()
