import json

attrs = {'0': 'sepal length',
           '1': 'sepal width',
           '2': 'petal length',
           '3': 'petal width',
           '4': 'class'}

data = []
with open('iris.json') as fin:
    data = json.load(fin)

output = []
for instance in data:
    new = {}
    for attr in instance:
        new[attrs[attr]] = instance[attr]
    output.append(new)

with open('new_iris.json', 'w') as fout:
    json.dump(output, fout)


                          

