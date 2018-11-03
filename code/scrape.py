# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import pickle

import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
file = open('Android.txt','r')
f = file.read()
# f=f.replace('\n','')
# open('Android.txt','w').write(f)
Android_dic={}
all = re.findall('<h3 class="api-name" id="\w+">(\w+)</h3>.+?<pre class="api-signature no-pretty-print">(.+?)</pre>              <p>(.+?)</p>.+?Constant Value:.+?(\d+)',f)

android_file = open('android_event_type.pkl','w+')


for a in all:
    title = a[0]
    Android_dic[title]={}
    public_discribe = a[1]
    rep = re.findall("(<.+?>)",a[2])
    describe = a[2]
    Constant_Value = a[3]
    for r in rep:
        describe=describe.replace(r,'')
    Android_dic[title]['public']=public_discribe
    Android_dic[title]['constant']=Constant_Value
    Android_dic[title]['describe']=describe

pickle.dump(Android_dic,android_file)
#
# for a in e_d:
#     print a, ';public:',Android_dic[a]['public'], ';constant value:', Android_dic[a]['constant'], ';decribe:', Android_dic[a]['describe']
#     print ''