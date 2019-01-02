# -*- coding:utf-8 -*-

import re
import pickle
import numpy as np
from collections import Counter
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
    'TYPE_WINDOW_STATE_CHANGED':[],#Represents the event of a change to a visually distinct section of the user interface. These events should only be dispatched from Views that have accessibility pane titles, and replaces TYPE_WINDOW_CONTENT_CHANGED for those sources. Details about the change are available from getContentChangeTypes().

    'TYPE_WINDOW_CONTENT_CHANGED':[],#Represents the event of changing the content of a window and more specifically the sub-tree rooted at the event's source.

    'TYPE_VIEW_FOCUSED':[],#Represents the event of setting input focus of a View.

    'TYPE_VIEW_SCROLLED':[],#Represents the event of scrolling a view. This event type is generally not sent directly.

    'TYPE_VIEW_CLICKED':[],#Represents the event of clicking on a View like Button, CompoundButton, etc.

    'TYPE_VIEW_TEXT_SELECTION_CHANGED':[],#Represents the event of changing the selection in an EditText.

    'TYPE_VIEW_ACCESSIBILITY_FOCUSED':[],#Represents the event of gaining accessibility focus.

    'TYPE_VIEW_TEXT_CHANGED':[],#Represents the event of changing the text of an EditText.

    'TYPE_VIEW_SELECTED':[],#Represents the event of selecting an item usually in the context of an AdapterView.

    'TYPE_NOTIFICATION_STATE_CHANGED':[],#Represents the event showing a Notification.

    'TYPE_ANNOUNCEMENT':[],#Represents the event of an application making an announcement.

    'TYPE_VIEW_ACCESSIBILITY_FOCUS_CLEARED':[],#Represents the event of clearing accessibility focus.

    'TYPE_VIEW_LONG_CLICKED':[],#Represents the event of long clicking on a View like Button, CompoundButton, etc.

    'TYPE_VIEW_HOVER_ENTER':[],#Represents the event of a hover enter over a View.

    'TYPE_VIEW_HOVER_EXIT':[],    #Represents the event of a hover exit over a View.
}

android_event_type_value = {
    'TYPE_WINDOW_STATE_CHANGED':0,#Represents the event of a change to a visually distinct section of the user interface. These events should only be dispatched from Views that have accessibility pane titles, and replaces TYPE_WINDOW_CONTENT_CHANGED for those sources. Details about the change are available from getContentChangeTypes().

    'TYPE_WINDOW_CONTENT_CHANGED':1,#Represents the event of changing the content of a window and more specifically the sub-tree rooted at the event's source.

    'TYPE_VIEW_FOCUSED':2,#Represents the event of setting input focus of a View.

    'TYPE_VIEW_SCROLLED':3,#Represents the event of scrolling a view. This event type is generally not sent directly.

    'TYPE_VIEW_CLICKED':4,#Represents the event of clicking on a View like Button, CompoundButton, etc.

    'TYPE_VIEW_TEXT_SELECTION_CHANGED':5,#Represents the event of changing the selection in an EditText.

    'TYPE_VIEW_ACCESSIBILITY_FOCUSED':6,#Represents the event of gaining accessibility focus.

    'TYPE_VIEW_TEXT_CHANGED':7,#Represents the event of changing the text of an EditText.

    'TYPE_VIEW_SELECTED':8,#Represents the event of selecting an item usually in the context of an AdapterView.

    'TYPE_NOTIFICATION_STATE_CHANGED':9,#Represents the event showing a Notification.

    'TYPE_ANNOUNCEMENT':'a',#Represents the event of an application making an announcement.

    'TYPE_VIEW_ACCESSIBILITY_FOCUS_CLEARED':'b',#Represents the event of clearing accessibility focus.

    'TYPE_VIEW_LONG_CLICKED':'c',#Represents the event of long clicking on a View like Button, CompoundButton, etc.

    'TYPE_VIEW_HOVER_ENTER':'d',#Represents the event of a hover enter over a View.

    'TYPE_VIEW_HOVER_EXIT':'e',    #Represents the event of a hover exit over a View.
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

event_sequence_by_time = {}

for f in files:
    logcat_file = open('.\data\com.example.myfristandroid\\'+f+'\logcat.pkl',"rb")
    event_file = open('.\data\com.example.myfristandroid\\'+f+'\event.pkl',"rb")
    logcat_list = pickle.load(logcat_file)
    event_list = pickle.load(event_file)



    for i in range(len(event_list)-1):
        time = event_list[i+1]['SyscTime']-event_list[i]['SyscTime']
        if time in event_sequence_by_time:
            event_sequence_by_time[time] += 1
        else:
            event_sequence_by_time[time] = 1
print(len(event_sequence_by_time))

result = filter(lambda x:x,sorted(zip(event_sequence_by_time.values(),event_sequence_by_time.keys()),reverse=1))
print(list(result))

for i in range(1,25):
    result_min = filter(lambda x:x[0]<=i,sorted(zip(event_sequence_by_time.values(),event_sequence_by_time.keys()),reverse=1))
    result_max = filter(lambda x:x[0]>i,sorted(zip(event_sequence_by_time.values(),event_sequence_by_time.keys()),reverse=1))
    # print(list(result_min))
    # print(list(result_max))
    value_max = max(sorted([x[1] for x in list(result_min)])[0:20])
    value_min = min(sorted([x[1] for x in list(result_max)],reverse=1)[0:20])
    print(i,value_max,value_min,value_max-value_min)
# for e in event_list:
#     android_event_type[e['EventType']].append(e)
# for l in logcat_list:
#     android_logcat_type[l['priority']].append(l)
#
# char_zhi = min(event_list[0]['SyscTime'],logcat_list[0]['SyscTime'])
#
#
# fig = plt.figure('fig')
# i = 200
#
# for a in android_logcat_type:
#     logcat_time_list = [float(x['SyscTime']-char_zhi) for x in android_logcat_type[a]]
#     if len(logcat_time_list)>0:
#         plt.scatter(logcat_time_list,[x for x in range(i,i+len(logcat_time_list))],c=android_logcat_type_c[a],marker='o',label=a)
#         i+=100
# for a in android_event_type:
#     event_time_list = [float(x['SyscTime'] - char_zhi) for x in android_event_type[a]]
#     if len(event_time_list)>0:
#         plt.scatter(event_time_list,[x for x in range(i,i+len(event_time_list))],c=android_event_type_c[a],marker='v',label=a)
#         i+=100
# plt.title("data")
# # plt.xlim(110000,125000)
# # plt.ylim(0,200)
# plt.xlabel("time")
# plt.ylabel("count")
# plt.legend(loc='lower right')
# plt.show()
