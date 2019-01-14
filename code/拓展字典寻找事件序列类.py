import json
import Levenshtein
import re

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
                e_words = ''
                error_words = ''
                for e in event:
                    e_words += e['PackageName']+' '+ e['EventType']+' '+ re.findall(' ClassName: (.+?); ', e['Action'])[0]
                    try:
                        text = re.findall(' Text: \[(.+)\]; ', e['Action'])[0]
                        e_words += text
                    except IndexError:
                        e_words += ' '
                        pass

                for e in event_slice[v]:
                    error_words += e['PackageName']+' '+ e['EventType']+' '+ re.findall(' ClassName: (.+?); ', e['Action'])[0]
                    try:
                        text = re.findall(' Text: \[(.+)\]; ', e['Action'])[0]
                        error_words += text
                    except IndexError:
                        error_words += ' '
                        pass
                sim = Levenshtein.ratio(e_words, error_words)
                if sim > 0.95:
                    if sim > 0.99:
                        print(event)
                        print(event_slice[v])
                    result_little.append([event_slice.index(event), sim])

                    print(sim)
            result_error[key].append(result_little)
    result.append(result_error)

with open('sim_event_sequence_95_name.json', 'w') as f:
    json.dump(result, f, indent=4)
