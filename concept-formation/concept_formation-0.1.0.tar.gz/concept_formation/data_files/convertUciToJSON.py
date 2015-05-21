import json
import csv

data = []
with open('iris.data.txt', 'rt') as f:
    r = csv.reader(f)
    for row in r:
        vec = {}
        for i, v in enumerate(row):
            if v != "?":
                vec[i] = v
        data.append(vec)

print(json.dumps(data))

