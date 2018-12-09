import os
import re
import operator
import pickle

only_event_time= []
only_logcat_time = []

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

files=file_name('.\data\com.example.myfristandroid')

event_all_to_one = []
logcat_all_to_one = []
for f in files:
    logcat_file = open('.\data\com.example.myfristandroid\\'+f+'\logcat.pkl',"rb")
    event_file = open('.\data\com.example.myfristandroid\\'+f+'\event.pkl',"rb")
    logcat_list = pickle.load(logcat_file)
    event_list = pickle.load(event_file)
    print(f)
    for e in event_list:
        flag = 0
        for q in event_all_to_one:
            if operator.eq(e, q) == True:
                flag = 1
                break
        if flag == 0:
            event_all_to_one.append(e)

    for l in logcat_list:
        flag = 0
        for q in logcat_all_to_one:
            if operator.eq(l, q) == True:
                flag = 1
                break
        if flag == 0:
            logcat_all_to_one.append(l)

print(len(event_all_to_one),len(logcat_all_to_one))
f = open('preData_event.pickle','wb')
pickle.dump(event_all_to_one,f)
f.close()

f = open('preData_logcat.pickle','wb')
pickle.dump(logcat_all_to_one,f)
f.close()