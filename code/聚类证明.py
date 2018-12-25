import json
import pickle
from collections import Counter
f = open('pre_cluster_all.json')
pre_cluster_all = json.load(f)
f.close()
print(len(pre_cluster_all))
logcat_file = open('preData_logcat.pickle', "rb")
event_file = open('preData_event.pickle', "rb")
logcat_list = pickle.load(logcat_file)
event_list = pickle.load(event_file)

def re_logcat(time_start,time_end):
    l_start = 0
    l_end = 0
    re_all = ''
    for l in range(len(logcat_list)):
        if time_start-logcat_list[l]['SyscTime']<=500 and time_start-logcat_list[l]['SyscTime']>=0:
            l_start = l
            break
        if l == len(logcat_list)-1:
            return re_all
    for l in range(len(logcat_list)):
        if logcat_list[l]['SyscTime']-time_end<=500 and logcat_list[l]['SyscTime']-time_end>=0:
            l_end = l
            break
    for i in range(l_start,l_end+1):
        re_all+=logcat_list[i]['priority']
    return re_all
cluster_all = pre_cluster_all
re_logcat_all = []
for c in range(len(cluster_all)):
    re_logcat_all_little = []
    for sequence in range(len(cluster_all[c])):
        time_start = cluster_all[c][sequence][0]['SyscTime']
        time_end= cluster_all[c][sequence][-1]['SyscTime']
        re_logcat_list = re_logcat(time_start,time_end)
        re_logcat_all_little.append(re_logcat_list)
    re_logcat_all.append(re_logcat_all_little)
for r in re_logcat_all:
    for l in r:
        print(l)
    print()
