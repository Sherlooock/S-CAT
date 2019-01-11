import json

with open("e_finish_cluser_timestamp.json") as f:
	time_list = json.load(f)
print(time_list)

with open('slice-event.json') as f:
	event_slice = json.load(f)

with open('logcat.json') as f:
	logcat_list = json.load(f)


finish_event = []

for E_time in time_list:
	for key,item in E_time.items():
		finish_event_little = {}
		finish_event_little[key] = []
		for time_stamp in item:
			for event_sequence in event_slice:
				time_start = event_sequence[0]["SyscTime"]
				time_finish = event_sequence[-1]["SyscTime"]
				if time_start<time_stamp<time_finish:
					if event_slice.index(event_sequence) not in finish_event_little[key]:
						finish_event_little[key].append(event_slice.index(event_sequence))
					break
		finish_event.append(finish_event_little)
print(finish_event)
with open('e_event_sequence_find.json','w') as f:
	json.dump(finish_event,f,indent=4)

