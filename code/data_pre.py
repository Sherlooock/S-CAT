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

logcat_filter=['E']
r=0
logcat_files=file_name('E:\code\logcats')
event_files=file_name('E:\code\events')
num=0
package={}
for l_root in logcat_files:
    if l_root in event_files:
        logcat_all_list = []
        for lfiles in logcat_files[l_root]:
            logcat_context = open(lfiles,"rb").readlines()
            r+=1
            for i in range(len(logcat_context)):
                logcat_context[i]=str(logcat_context[i])
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
                logcat_dic['message'] = ''
                j = i+1
                while len(logcat_context[j])>2:
                    logcat_dic['message']+=str(logcat_context[j])
                    j+=1
                if logcat_dic not in logcat_all_list:
                    logcat_all_list.append(logcat_dic)

        #print logcat_all_list
        event_all_list = []
        for lfiles in event_files[l_root]:
            event_all = open(lfiles,'rb').readlines()
            for event in event_all:
                event=str(event)
                if len(re.findall("SyscTime: (\d+)",event))==0:
                    continue
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
                    if event_dict['PackageName'] not in package:
                        package[event_dict['PackageName']] = 0
                    else:
                        package[event_dict['PackageName']] += 1
                    event_all_list.append(event_dict)
        #print event_all_list
        package_name=''
        if len(event_all_list)>0 and len(logcat_all_list)>0:
            package_name = event_all_list[0]['PackageName']
            file_root='data/'+str(package_name)+'/'+str(l_root)+'/event.pkl'
            f=open(file_root,'wb')
            pickle.dump(event_all_list,f)
            f.close()
            file_root = 'data/' + str(package_name) + '/' + str(l_root) + '/logcat.pkl'
            f = open(file_root, 'wb')
            pickle.dump(logcat_all_list, f)
            f.close()
            print (file_root)
    else:
        num+=1


