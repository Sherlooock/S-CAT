import json
import Levenshtein

with open("e_event_sequence_find.json") as f:
    sequence_list = json.load(f)
print(sequence_list)

with open('slice-event.json') as f:
    event_slice = json.load(f)

with open('logcat.json') as f:
    logcat_list = json.load(f)

result = []
for s in sequence_list:
    result_error = {}
    for key, value in s.items():
        result_error[key] = []
        for v in value:
            result_little = []
            for event in event_slice:
                sim = Levenshtein.ratio(str(event_slice[v]), str(event))
                if sim > 0.98:
                    result_little.append([event_slice.index(event), sim])

                    print(sim)
            result_error[key].append(result_little)
    result.append(result_error)

with open('sim_event_sequence_98_name.json', 'w') as f:
    json.dump(result, f, indent=4)
