from concept_formation.trestle import TrestleTree
from concept_formation.cluster import cluster

# Data is stored in a list of dictionaries where values can be either nominal,
# numeric, component, or relational.

data = [{'f1': 'v1', #nominal value
         'f2': 2.6, #numeric value
         'f3': {'sub-feature1': 'v1'}, # component value
         'f4': {'sub-feature1': 'v1'}, # component value
         'f5': ['some-relation', 'f3', 'f4'] #relational value
        },
        {'f1': 'v1', #nominal value
         'f2': 2.8, #numeric value
         'f3': {'sub-feature1': 'v2'}, # component value
         'f4': {'sub-feature1': 'v1'}, # component value
         'f5': ['some-relation', 'f3', 'f4'] #relational value
        }]

# Data can be clustered with a TrestleTree, which supports all data types or
# with a specific tree (CobwebTree or Cobweb3Tree) that supports subsets of
# datatypes.
tree = TrestleTree()
tree.fit(data)

# Trees can be printed in plaintext or exported in JSON format
print(tree)
print(tree.root.output_json())

# Trees can also be used to predict missing attributes of new data points.
new = {'f2': 2.6, 'f3': {'sub-feature1': 'v1'}, 'f4': {'sub-feature1': 'v1'},
       'f5': ['some-relation', 'f3', 'f4']}
concept = tree.categorize(new)
print(concept.predict('f1'))

# Trees can be used to produce flat clusterings
new_tree = TrestleTree()
clustering = cluster(new_tree, data, minsplit=1, maxsplit=1)
print(clustering)





