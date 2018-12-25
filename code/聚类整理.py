import pickle
import re
import json


android_event_type_value = {
    'TYPE_WINDOW_STATE_CHANGED': '0',
    # Represents the event of a change to a visually distinct section of the user interface. These events should only be dispatched from Views that have accessibility pane titles, and replaces TYPE_WINDOW_CONTENT_CHANGED for those sources. Details about the change are available from getContentChangeTypes().

    'TYPE_WINDOW_CONTENT_CHANGED': '1',
    # Represents the event of changing the content of a window and more specifically the sub-tree rooted at the event's source.

    'TYPE_VIEW_FOCUSED': '2',  # Represents the event of setting input focus of a View.

    'TYPE_VIEW_SCROLLED': '3',
    # Represents the event of scrolling a view. This event type is generally not sent directly.

    'TYPE_VIEW_CLICKED': '4',  # Represents the event of clicking on a View like Button, CompoundButton, etc.

    'TYPE_VIEW_TEXT_SELECTION_CHANGED': '5',  # Represents the event of changing the selection in an EditText.

    'TYPE_VIEW_ACCESSIBILITY_FOCUSED': '6',  # Represents the event of gaining accessibility focus.

    'TYPE_VIEW_TEXT_CHANGED': '7',  # Represents the event of changing the text of an EditText.

    'TYPE_VIEW_SELECTED': '8',  # Represents the event of selecting an item usually in the context of an AdapterView.

    'TYPE_NOTIFICATION_STATE_CHANGED': '9',  # Represents the event showing a Notification.

    'TYPE_ANNOUNCEMENT': 'a',  # Represents the event of an application making an announcement.

    'TYPE_VIEW_ACCESSIBILITY_FOCUS_CLEARED': 'b',  # Represents the event of clearing accessibility focus.

    'TYPE_VIEW_LONG_CLICKED': 'c',  # Represents the event of long clicking on a View like Button, CompoundButton, etc.

    'TYPE_VIEW_HOVER_ENTER': 'd',  # Represents the event of a hover enter over a View.

    'TYPE_VIEW_HOVER_EXIT': 'e',  # Represents the event of a hover exit over a View.

}
android_event_class_type = {
    'android.widget.ImageButton': '1',
    'com.example.myfristandroid.MainActivity': '2',
    'android.widget.RelativeLayout': '3',
    'com.example.myfristandroid.graphWebShow': '4',
    'android.widget.FrameLayout': '5',
    'com.example.myfristandroid.CustomProgressDialog': '6',
    'com.example.myfristandroid.HuzAlertDialog': '7',
    'android.widget.Button': '8',
    'android.widget.ListView': '9',
    'android.widget.TextView': 'a',
    'android.widget.LinearLayout': 'b',
    'android.support.v4.view.ViewPager': 'c',
    'android.widget.EditText': 'd',
    'android.widget.CheckedTextView': 'e',
    'android.widget.ScrollView': 'f',
    'com.android.org.chromium.content.browser.ContentViewCore': 'g',
    'android.view.View': 'h',
    'android.widget.GridView': 'i',
    'android.webkit.WebView': 'j',
    'com.example.myfristandroid.SplashActivity': 'k',
    'org.chromium.content.browser.ContentViewCore': 'l',
    'android.widget.Image': 'm'
}
logcat_file = open('preData_logcat.pickle', "rb")
event_file = open('preData_event.pickle', "rb")
logcat_list = pickle.load(logcat_file)
event_list = pickle.load(event_file)

def re_logcat(time_start,time_end):
    l_start = 0
    l_end = 0
    re_all = []
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
        re_all.append(logcat_list[i]['priority'])
    return re_all




event_sequence_by_time = []
event_little_sequence_by_time = []
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

event_sequence_all = []

for event_sequence_by_time_list in event_sequence_by_time:
    if len(event_sequence_by_time_list) >= 3:
        event_sequence = []
        for e in event_sequence_by_time_list:
            try:
                action_class = re.findall("ClassName: (.+?);", e['Action'])[0]
                event_sequence.append(
                    [android_event_type_value[e['EventType']] + android_event_class_type[action_class], e])
            except TypeError:
                print(e)
            except KeyError:
                event_sequence.append([android_event_type_value[e['EventType']] + '0', e])
        event_sequence_all.append(event_sequence)

parsedDat = event_sequence_all
littleList = []
for middleDat in [x for x in parsedDat]:
    littleList_item = []
    for i in range(0, len(middleDat)):
        if middleDat[i][0] == '02':
            littleList.append(littleList_item)
            littleList_item = []
            littleList_item.append(middleDat[i][1])
        else:
            littleList_item.append(middleDat[i][1])

parsedDat = [x for x in littleList if len(x) >= 2 and len(x) <= 38]

cluster_index_all = [[39, 208, 215, 278, 659, 763, 780], [122, 153, 240, 271, 290, 294, 309, 339, 389, 411, 424, 461, 549, 562, 569, 625, 650, 724], [100, 116, 120, 121, 245, 246, 250, 259, 263, 300, 302, 314, 325, 365, 414, 418, 437, 458, 567, 579, 599, 633, 716, 725], [201, 202, 203, 220, 324, 510, 661, 685], [2, 64, 112, 213, 280, 281, 406, 420, 537, 551, 576, 588, 590, 732], [33, 34, 44, 71, 106, 118, 239, 252, 261, 275, 282, 304, 306, 380, 407, 538, 623, 636, 706, 713], [127], [188, 354], [0, 107, 604, 690, 698, 709, 786], [795], [67, 168, 197, 237, 254, 265, 321, 371, 523, 525, 526, 555, 593, 653, 705], [38, 45, 85, 89, 204, 230, 233, 296, 496, 506, 553, 580, 592, 673, 704, 758, 766, 767, 782], [398, 586], [96, 97, 226, 421, 735], [18, 54, 211, 381], [311, 331, 351, 606, 681, 692, 695, 746, 757, 800], [41, 52, 68, 243, 303, 707], [69, 72, 77, 98, 104, 313, 459, 497, 616, 726, 743, 756], [329, 355, 563], [317], [618], [47, 48, 55, 74, 83, 186, 189, 333, 377, 378, 383, 384, 387, 450, 453, 511, 512, 514, 596, 635, 639, 643, 644, 647, 649, 676, 761, 794], [136, 137, 147, 192, 334, 345, 492, 495, 513, 515, 610, 779], [36, 357, 359, 360, 361, 362, 363, 364, 426, 427, 428, 431, 433, 434, 463, 499, 500, 503, 504, 541, 542, 543, 544, 545, 546, 547, 548, 608, 628, 629, 630, 631, 632, 696, 752], [6, 10, 27, 29, 32, 40, 53, 62, 86, 99, 108, 174, 182, 183, 232, 235, 238, 256, 279, 316, 348, 350, 366, 370, 388, 402, 438, 462, 487, 488, 524, 529, 531, 535, 573, 575, 591, 617, 626, 634, 654, 667, 691, 700, 710, 719, 727, 747, 751, 771, 784, 809, 812], [3, 16, 46, 51, 63, 80, 105, 124, 169, 179, 198, 205, 207, 241, 249, 262, 270, 301, 319, 401, 403, 404, 412, 423, 443, 460, 471, 498, 527, 550, 556, 561, 568, 611, 648, 729, 736, 759, 762, 789], [70, 73, 123, 181, 187, 253, 292, 295, 307, 322, 417, 674, 714, 721, 731, 744, 750, 770], [129, 266, 267, 269, 390, 393, 394, 395, 474, 475, 476, 479, 481, 482, 483, 485, 570, 702, 793], [5, 8, 9, 30, 31, 49, 75, 76, 82, 84, 87, 88, 91, 172, 175, 177, 178, 185, 227, 268, 343, 368, 374, 376, 379, 382, 386, 391, 451, 452, 454, 455, 456, 472, 473, 477, 478, 480, 484, 489, 517, 518, 519, 522, 571, 595, 597, 598, 600, 601, 602, 605, 609, 638, 640, 642, 645, 646, 668, 669, 670, 671, 672, 677, 678, 679, 684, 688, 760, 772, 773, 774, 796, 802, 803, 805, 806, 807], [56, 114, 115, 223, 318, 332, 397, 399, 400, 405, 416, 439, 446, 447, 448, 574, 583, 656, 801], [413], [195, 342, 409, 657, 686, 781], [7, 92, 93, 94, 95, 171, 196, 212, 221, 251, 260, 285, 286, 287, 373, 375, 410, 587, 658, 683, 689, 701, 722, 798], [28, 534, 539, 603, 748, 783, 808], [180, 787], [449], [184, 326, 327, 533], [367, 385, 641, 675], [26, 228, 248, 509, 520, 560, 687], [79, 352, 516, 521, 637], [81, 117, 372, 425, 680, 804], [214], [274], [655], [42, 58, 699], [244, 305, 442, 557, 577, 622, 730, 769, 785], [441], [126, 299, 776, 797], [14, 25], [392, 612], [444], [66, 173, 206, 216, 218, 231, 234, 236, 257, 276, 330, 396, 457, 507, 558, 589, 620, 711, 717], [50, 59, 60, 255, 464, 465, 466, 467, 468, 469, 470, 693, 694, 708, 749, 775, 811], [320, 440, 572, 607], [101], [4, 19, 61, 125, 156, 158, 162, 199, 200, 283, 284, 288, 337, 346, 422, 662, 738, 739, 742, 790], [35, 190, 264, 273, 624, 723, 737, 740, 788], [113, 242, 308, 323, 813], [119, 258, 272, 277, 291, 297, 298, 315, 328, 349, 369, 445, 528, 532, 536, 554, 565, 578, 581, 585, 660, 733, 745, 810], [152, 167], [209, 210, 224, 663], [11, 12, 13, 15, 20, 128, 130, 132, 138, 146, 150, 154, 155, 157, 161, 163, 164, 165, 222, 247, 289, 336, 338, 340, 341, 344, 347, 408, 419, 490, 613, 614, 615, 619, 651, 664, 665, 764, 765, 768, 777, 791, 792, 799], [65, 90, 109, 229, 356, 415, 508, 552, 566, 712, 734], [225, 293, 353, 530, 559, 584, 715, 718], [217, 621, 682], [133, 134, 135, 139, 140, 141, 142, 143, 144, 145, 148, 149, 159, 160, 166], [17, 21, 22, 23, 24, 131, 151, 170, 219, 491, 494, 652, 666, 703, 741, 778], [1, 57, 78, 310, 312, 540, 564, 594, 720], [37, 43, 102, 103, 110, 111, 176, 191, 193, 194, 335, 358, 429, 430, 432, 435, 436, 486, 493, 501, 502, 505, 582, 627, 697, 728, 753, 754, 755]]

cluster_all = []
for cluster in cluster_index_all:
    cluster_all_little = []
    for c in cluster:
        cluster_all_little.append(parsedDat[c])
    cluster_all.append(cluster_all_little)
delete_all = []
for c in range(len(cluster_all)):
    for sequence in range(len(cluster_all[c])):
        time_start = cluster_all[c][sequence][0]['SyscTime']
        time_end= cluster_all[c][sequence][-1]['SyscTime']
        re_logcat_list = re_logcat(time_start,time_end)
        if len(re_logcat_list)==0:
            delete_all.append([c,sequence])
for d in delete_all:
    cluster_all[d[0]][d[1]] = -1

pre_cluster_all = []
for c in cluster_all:
    pre_cluster_all_little = []
    for sequence in c:
        if sequence != -1:
            pre_cluster_all_little.append(sequence)
    if len(pre_cluster_all_little) != 0:
        pre_cluster_all.append(pre_cluster_all_little)
f = open("pre_cluster_all.json","w")
json.dump(pre_cluster_all,f)
f.close()