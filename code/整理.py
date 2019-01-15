import json
import re

with open("e_event_sequence_find.json") as f:
    list_pre = json.load(f)

with open('sim_event_sequence_98_name.json') as f:
    list_after = json.load(f)

with open('slice-event.json') as f:
    event_sequence = json.load(f)


def data_reform(event_sequence):
    words = ''
    for e in event_sequence:
        words += e['PackageName'] + ' ' + e['EventType'] + ' ' + re.findall(' ClassName: (.+?); ', e['Action'])[0] + ' '
        try:
            words += re.findall(' Text: \[(.+)\]; ', e['Action'])[0]
        except IndexError:
            words += ' '
            pass
        words += ' '
    return words

result = []
for item in list_pre:
    result_little = {}
    for key, value in item.items():
        result_little[key] = {}
        result_little[key]['first'] = []
        result_little[key]['second'] = []
        num_key = list_pre.index(item)
        for v in value:
            num_v = value.index(v)
            if v not in result_little[key]['first']:
                result_little[key]['first'].append(v)
        for v in value:
            num_v = value.index(v)
            for u in list_after[num_key][key][num_v]:
                if u[0] not in result_little[key]['second'] and u[0] not in result_little[key]['first']:
                    result_little[key]['second'].append(u[0])
    result.append(result_little)

with open('make_up_after_find_hier_98.json', 'w') as f:
    json.dump(result, f, indent=4)

all = []
num = 0
for r in result:
    for key, value in r.items():
        num += len(r[key]['first'])
        for key_child, value_child in value.items():
            print(key, key_child, len(value_child))
            for v in value_child:
                print(data_reform(event_sequence[v]))
            all += value_child
