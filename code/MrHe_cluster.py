import json

import Levenshtein

if __name__ == '__main__':
	with open('slice-event.json') as f:
		event_slice = json.load(f)

	with open('logcat.json') as f:
		logcat_list = json.load(f)


	def time_compare(first_time, second_time):
		return abs(first_time - second_time) < 10


	print(logcat_list[0].keys(), logcat_list[0]['priority'], logcat_list[0]['SyscTime'])
	print(len(event_slice))
	logcat_E_time_dic = {}
	logcat_W_time_dic = {}
	for logcat in logcat_list:
		if logcat['priority'] == 'E':
			logcat_E_time_dic[logcat['SyscTime']] = logcat
		elif logcat['priority'] == 'W':
			logcat_W_time_dic[logcat['SyscTime']] = logcat
	E_event_list = []
	for E, logcat in logcat_E_time_dic.items():
		for little_list in event_slice:
			for event in little_list:
				if time_compare(event['SyscTime'], E):
					E_event_list.append([little_list, logcat])
	print(len(E_event_list))
	cluster_list = []
	for item in E_event_list:
		print(item[1]['tag'] + ' ' + item[1]['message'])
		cluster_list.append(item[1]['message'])
	print(len(list(set([x[1]['tag'] for x in E_event_list]))))

	# finish_cluster = [
	# 	[2, 3, 7, 8, 11, 13, 14, 15, 16, 18, 20, 21, 22, 23, 25, 28, 31, 32, 33, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57,
	# 	 58, 59, 60, 62, 63, 64, 78, 79, 80, 87, 88, 89, 107, 108, 109, 110, 121, 122, 123, 124, 125, 126, 127, 128,
	# 	 129, 130, 131, 132, 133, 134, 135], [65, 66, 67, 68], [10, 12, 24, 34, 36],
	# 	[9, 17, 19, 26, 27, 29, 30, 35, 38, 39, 40, 41, 42, 43, 46, 47],
	# 	[71, 72, 73, 74, 75, 76, 77, 115, 116, 117, 118, 119, 120], [136, 137, 138], [1, 61], [69, 70], [37], [0],
	# 	[84, 85, 86, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106],
	# 	[4, 5, 6, 48, 49, 81, 82, 83, 90, 91, 92, 111, 112, 113, 114]]
	# finish_cluster = [[28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103], [12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 47], [10, 43, 64, 65], [8, 9], [11], [21], [0, 1, 2, 3, 4, 7, 41, 42, 44, 46, 63, 104, 105, 108, 109], [62], [106, 107], [5, 45], [6, 20, 25], [27], [26]]
	#
	#
	# dic_list = []
	#
	# for cluster in finish_cluster:
	# 	dic_little = {}
	# 	for i in cluster:
	# 		name = E_event_list[i][1]['tag']
	# 		if name in dic_little:
	# 			dic_little[name].append(E_event_list[i][1]['SyscTime'])
	# 		else:
	# 			dic_little[name] = []
	# 			dic_little[name].append(E_event_list[i][1]['SyscTime'])
	# 	dic_list.append(dic_little)
	# with open('e_finish_cluser_timestamp.json', 'w') as f:
	# 	json.dump(dic_list, f, indent=4)

	# cl = []
	# for i in cluster_list:
	# 	cl_little = []
	# 	for j in cluster_list:
	# 		cl_little.append(1-Levenshtein.ratio(i,j))
	# 	cl.append(cl_little)
	# with open('e_cluster.json','w') as f:
	# 	json.dump(cl,f,indent=4)
