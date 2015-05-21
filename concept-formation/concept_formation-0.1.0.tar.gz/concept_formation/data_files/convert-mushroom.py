import json

attrs = {'0': 'classification',
           '1': 'cap-shape',
           '2': 'cap-surface',
           '3': 'cap-color',
           '4': 'bruises?',
           '5': 'odor',
           '6': 'gill-attachment',
           '7': 'gill-spacing',
           '8': 'gill-size',
           '9': 'gill-color',
           '10': 'stalk-shape',
           '11': 'stalk-root',
           '12': 'stalk-surface-above-ring',
           '13': 'stalk-surface-below-ring',
           '14': 'stalk-color-above-ring',
           '15': 'stalk-color-below-ring',
           '16': 'veil-type',
           '17': 'veil-color',
           '18': 'ring-number',
           '19': 'ring-type',
           '20': 'spore-print-color',
           '21': 'population',
           '22': 'habitat'}

vals = {}
vals['classification'] = {'p': 'poisonous',
                          'e': 'edible'}
vals['cap-shape'] = {'b': 'bell',
                     'c': 'conical',
                     'x': 'convex',
                     'f': 'flat',
                     'k': 'knobbed',
                     's': 'sunken'}
vals['cap-surface'] = {'f': 'fibrous',
                       'g': 'grooves',
                       'y': 'scaly',
                       's': 'smooth'}
vals['cap-color'] = {'n': 'brown',
                     'b': 'buff',
                     'c': 'cinnamon',
                     'g': 'gray',
                     'r': 'green',
                     'p': 'pink',
                     'u': 'purple',
                     'e': 'red',
                     'w': 'white',
                     'y': 'yellow'}
vals['bruises?'] = {'t': 'yes',
                    'f': 'no'}
vals['odor'] = {'a': 'almond',
                'l': 'anise',
                'c': 'creosote',
                'y': 'fishy',
                'f': 'foul',
                'm': 'musty',
                'n': 'none',
                'p': 'pungent',
                's': 'spicy'}
vals['gill-attachment'] = {'a': 'attached',
                           'd': 'descending',
                           'f': 'free',
                           'n': 'notched'}
vals['gill-spacing'] = {'c': 'closed',
                        'w': 'crowded',
                        'd': 'distant'}
vals['gill-size'] = {'b': 'broad',
                    'n': 'narrow'}
vals['gill-color'] = {'k': 'black',
                      'n': 'brown',
                      'b': 'buff',
                      'h': 'chocolate',
                      'g': 'gray',
                      'r': 'green',
                      'o': 'orange',
                      'p': 'pink',
                      'u': 'purple',
                      'e': 'red',
                      'w': 'white',
                      'y': 'yellow'}
vals['stalk-shape'] = {'e': 'enlarging',
                       't': 'tapering'}
vals['stalk-root'] = {'b': 'bulbous',
                      'c': 'club',
                      'u': 'cup',
                      'e': 'equal',
                      'z': 'rhizomorphs',
                      'r': 'rooted',
                      '?': 'missing'}
vals['stalk-surface-above-ring'] = {'f': 'fibrous',
                                    'y': 'scaly',
                                    'k': 'silky',
                                    's': 'smooth'}
vals['stalk-surface-below-ring'] = {'f': 'fibrous',
                                    'y': 'scaly',
                                    'k': 'silky',
                                    's': 'smooth'}
vals['stalk-color-above-ring'] = {'n': 'brown',
                                  'b': 'buff', 
                                  'c': 'cinnamon',
                                  'g': 'gray',
                                  'o': 'orange',
                                  'p': 'pink',
                                  'e': 'red',
                                  'w': 'white',
                                  'y': 'yellow'}
vals['stalk-color-below-ring'] = {'n': 'brown',
                                  'b': 'buff', 
                                  'c': 'cinnamon',
                                  'g': 'gray',
                                  'o': 'orange',
                                  'p': 'pink',
                                  'e': 'red',
                                  'w': 'white',
                                  'y': 'yellow'}
vals['veil-type'] = {'p': 'partial',
                     'u': 'universal'}
vals['veil-color'] = {'n': 'brown',
                      'o': 'orange',
                      'w': 'white',
                      'y': 'yellow'}
vals['ring-number'] = {'n': 'none',
                       'o': 'one',
                       't': 'two'}
vals['ring-type'] = {'c': 'cobwebby',
                     'e': 'evanescent',
                     'f': 'flaring',
                     'l': 'large',
                     'n': 'none',
                     'p': 'pendant',
                     's': 'sheathing',
                     'z': 'zone'}
vals['spore-print-color'] = {'k': 'black',
                             'n': 'brown',
                             'b': 'buff', 
                             'h': 'chocolate',
                             'r': 'green',
                             'o': 'orange',
                             'u': 'purple',
                             'w': 'white',
                             'y': 'yellow'}
vals['population'] = {'a': 'abundant',
                      'c': 'clustered',
                      'n': 'numerous',
                      's': 'scattered',
                      'v': 'several',
                      'y': 'solitary'}
vals['habitat'] = {'g': 'grasses',
                   'l': 'leaves',
                   'm': 'meadows',
                   'p': 'paths',
                   'u': 'urban',
                   'w': 'waste',
                   'd': 'woods'}

data = []
with open('mushrooms.json') as fin:
    data = json.load(fin)

output = []
for instance in data:
    new = {}
    for attr in instance:
        new[attrs[attr]] = vals[attrs[attr]][instance[attr]]
    output.append(new)

with open('new_mushrooms.json', 'w') as fout:
    json.dump(output, fout)


                          

