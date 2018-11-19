# -*- coding:utf-8 -*-

import time
import datetime
import re
import sys

import os

def file_name(file_dir):
    file_names ={}
    for root, dirs, files in os.walk(file_dir):
        if len(files)!=0:
            for f in files:
                if len(re.findall('txt',f))!=0:
                    fname=root+'\\'+f
                    froot=re.findall('\d+_\d+',fname)[0]
                    file_names[froot]=fname  #当前目录路径
    return file_names
        #print(dirs) #当前路径下所有子目录
        #print(files) #当前路径下所有非目录子文件

logcat_filter=['E']
r=0

eventType={}
eventCount=[]


logcat_context = open('logcat.txt').readlines()
logcat_all_list=[]
r+=1;
for i in range(len(logcat_context)):
    logcat_dic={}
    if len(re.findall('\[ \d{2}-\d{2} \d{2}:\d{2}:\d{2}', logcat_context[i]))==0:
        continue
    bug_time = re.findall('\d{2}-\d{2} \d{2}:\d{2}:\d{2}', logcat_context[i])[0]
    bug_time = '2015-' + bug_time
    #print bug_time
    timeArray = time.strptime(bug_time, "%Y-%m-%d %H:%M:%S")
    bug_time = time.mktime(timeArray)
    #print logcat_context[i]
    wei_time = re.findall('\d{2}-\d{2} \d{2}:\d{2}:\d{2}.(\d{3})', logcat_context[i])[0]
    logcat_dic['SyscTime'] = int(str(int(bug_time))+str(wei_time))
    # print logcat_context[i]
    ID = re.findall('(\w+):( *\w+) ([V,D,I,W,E,F,S])/(.+) ]', logcat_context[i])[0]
    logcat_dic['processID'] = ID[0]
    logcat_dic['threadID'] = ID[1]
    logcat_dic['priority'] = ID[2]
    logcat_dic['tag'] = ID[3]
    logcat_dic['message'] = logcat_context[i+1]
    logcat_all_list.append(logcat_dic)


event_all_list = []
event_all = open('event.txt').readlines()
for event in event_all:
    if len(re.findall("SyscTime: (\d+)",event))==0:
        continue
    Systime = re.findall("SyscTime: (\d+)",event)[0]
    event = re.findall("(\w+): \d (\[.+\]);|(\w+): (.+?);",event)
    event_dict = {}
    for e in event:
        if len(e[0])==0:
            event_dict[e[2]]=e[3]
        else:
            event_dict[e[0]]=e[1]

        event_dict['SyscTime']=int(Systime)
    if 'EventType' in event_dict:
        event_all_list.append(event_dict)

processID={}

for l in logcat_all_list:
    if l['priority'] in logcat_filter:
        if l['processID'] in processID:
            processID[l['processID']]['count']+=1
            if l['threadID'] in processID[l['processID']]['thread']:
                processID[l['processID']]['thread'][l['threadID']]+=1
            else:
                processID[l['processID']]['thread'][l['threadID']] = 1
        else:
            processID[l['processID']]={}
            processID[l['processID']]['count'] = 1
            processID[l['processID']]['thread'] = {}
            processID[l['processID']]['thread'][l['threadID']] = 1

for p in processID:
    print ('processID:',p,processID[p]['count'])
    for t in processID[p]['thread']:
        print ('threadID:',t,processID[p]['thread'][t])

