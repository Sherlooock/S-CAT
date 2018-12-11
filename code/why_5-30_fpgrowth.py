# -*- coding:utf-8 -*-

import re
import pickle
import numpy as np
from collections import Counter
import fpgrowth
import time
import chardet

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
    'TYPE_WINDOW_STATE_CHANGED':'0',#Represents the event of a change to a visually distinct section of the user interface. These events should only be dispatched from Views that have accessibility pane titles, and replaces TYPE_WINDOW_CONTENT_CHANGED for those sources. Details about the change are available from getContentChangeTypes().

    'TYPE_WINDOW_CONTENT_CHANGED':'1',#Represents the event of changing the content of a window and more specifically the sub-tree rooted at the event's source.

    'TYPE_VIEW_FOCUSED':'2',#Represents the event of setting input focus of a View.

    'TYPE_VIEW_SCROLLED':'3',#Represents the event of scrolling a view. This event type is generally not sent directly.

    'TYPE_VIEW_CLICKED':'4',#Represents the event of clicking on a View like Button, CompoundButton, etc.

    'TYPE_VIEW_TEXT_SELECTION_CHANGED':'5',#Represents the event of changing the selection in an EditText.

    'TYPE_VIEW_ACCESSIBILITY_FOCUSED':'6',#Represents the event of gaining accessibility focus.

    'TYPE_VIEW_TEXT_CHANGED':'7',#Represents the event of changing the text of an EditText.

    'TYPE_VIEW_SELECTED':'8',#Represents the event of selecting an item usually in the context of an AdapterView.

    'TYPE_NOTIFICATION_STATE_CHANGED':'9',#Represents the event showing a Notification.

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
android_event_class_type = {
'android.widget.ImageButton':'1',
'com.example.myfristandroid.MainActivity':'2',
'android.widget.RelativeLayout':'3',
'com.example.myfristandroid.graphWebShow':'4',
'android.widget.FrameLayout':'5',
'com.example.myfristandroid.CustomProgressDialog':'6',
'com.example.myfristandroid.HuzAlertDialog':'7',
'android.widget.Button':'8',
'android.widget.ListView':'9',
'android.widget.TextView':'a',
'android.widget.LinearLayout':'b',
'android.support.v4.view.ViewPager':'c',
'android.widget.EditText':'d',
'android.widget.CheckedTextView':'e',
'android.widget.ScrollView':'f',
'com.android.org.chromium.content.browser.ContentViewCore':'g',
'android.view.View':'h',
'android.widget.GridView':'i',
'android.webkit.WebView':'j',
'com.example.myfristandroid.SplashActivity':'k',
'org.chromium.content.browser.ContentViewCore':'l',
'android.widget.Image':'m'
}

r=0
logcat=[]
event = []

event_sequence_by_time = []

logcat_all = {}
event_sequence = []
logcat_file = open('preData_logcat.pickle',"rb")
event_file = open('preData_event.pickle',"rb")
logcat_list = pickle.load(logcat_file)
event_list = pickle.load(event_file)
event_little_sequence_by_time = []

for l in logcat_list:
    if l['SyscTime'] in logcat_all:
        logcat_all[l['SyscTime']].append(l['priority'])
    else:
        logcat_all[l['SyscTime']]=[]

for i in range(len(event_list) - 1):
    time = event_list[i + 1]['SyscTime'] - event_list[i]['SyscTime']
    if time < 10000:
        event_little_sequence_by_time.append(event_list[i])
    else:
        event_little_sequence_by_time.append(event_list[i])
        event_sequence_by_time.append(event_little_sequence_by_time)
        event_little_sequence_by_time = []
        continue
event_little_sequence_by_time.append(event_list[len(event_list) - 1])
event_sequence_by_time.append(event_little_sequence_by_time)
print(len([x for x in event_sequence_by_time if len(x)>= 3]))
event_sequence_all = []

for event_sequence_by_time_list in event_sequence_by_time:
    if len(event_sequence_by_time_list) >= 3:
        event_sequence = []
        for e in event_sequence_by_time_list:
            try:
                action_class = re.findall("ClassName: (.+?);", e['Action'])[0]
                event_sequence.append([android_event_type_value[e['EventType']] + android_event_class_type[action_class],e])
            except TypeError:
                print(e)
            except KeyError:
                event_sequence.append([android_event_type_value[e['EventType']] + '0',e])
        event_sequence_all.append(event_sequence)



parsedDat = event_sequence_all
## print(Counter([len(x) for x in parsedDat]))
# print(len([x for x in parsedDat if len(x)<=10]))

littleList = []
for middleDat in [x for x in parsedDat ]:
    littleList_item = []
    for i in range(0,len(middleDat)):
        if middleDat[i][0] == '02':
            littleList.append(littleList_item)
            littleList_item = []
            littleList_item.append(middleDat[i][1])
        else:
            littleList_item.append(middleDat[i][1])
print(len(littleList))
num = 0
for event_sequence_by_time_list in littleList:
    if len(event_sequence_by_time_list) < 2:
        num+=1
        for e in event_sequence_by_time_list:
            time = [x for x in range(e['SyscTime'],e['SyscTime']+5)]
            for t in time:
                try:
                    if 'E' in logcat_all[t] or 'W' in logcat_all[t]:
                        print(logcat_all[t],t,end='')
                        print(event_sequence_by_time_list)
                        break
                except:
                    pass
print(num)


#2-38



