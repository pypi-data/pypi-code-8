#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Manuel Guenther <Manuel.Guenther@idiap.ch>

# This file includes the setup for the set of experiments ran to re-generate Figure 4 of the paper.

# The preprocessor, with different translations and rotation angles
preprocessor = "xfacereclib.paper.IET2015.facereclib.FixedPerturbation(cropped_image_size=(80,64), cropped_positions = {'reye':(16,15), 'leye':(16,48)}, translation=(#1,#2), angle=#3)"

# The feature extractor, which differs for all face recognition algorithms
feature_extractor = "#4"

# The face recognition algorithm
tool = "#5"

# The set of parameters that should be tested
replace = {
    # define, which parameters affect only the preprocessing stage
    'preprocessing' : {
        # replace #1 (i.e., the translation-y in the preprocessor) with these values:
        "#1" : {
            'ty-9' : -9,
            'ty-7' : -7,
            'ty-5' : -5,
            'ty-3' : -3,
            'ty-1' : -1,
            'ty+0' : 0,
            'ty+1' : 1,
            'ty+3' : 3,
            'ty+5' : 5,
            'ty+7' : 7,
            'ty+9' : 9
        },
        # replace #2 (i.e., the translation-x in the preprocessor) with these values:
        "#2" : {
            'tx-9' : -9,
            'tx-7' : -7,
            'tx-5' : -5,
            'tx-3' : -3,
            'tx-1' : -1,
            'tx+0' : 0,
            'tx+1' : 1,
            'tx+3' : 3,
            'tx+5' : 5,
            'tx+7' : 7,
            'tx+9' : 9
        },
        # replace #3 (i.e., the angle in the preprocessor) with these values:
        "#3" : {
            'a-20' : -20,
            'a-15' : -15,
            'a-10' : -10,
            'a-05' : -5,
            'a+00' : 0,
            'a+05' : 5,
            'a+10' : 10,
            'a+15' : 15,
            'a+20' : 20
        }
    },

    # define, which parameters affect only the feature extraction stage
    'extraction' : {
        # since feature extraction and face recognition algorithm are bound together, we define both of them here, i.e., as a tuple
        # replace #4 with the first value (the feature extractor) and #5 with the second value (the face recognition algorithm) **at the same time**
        # See FaceRecLib documentation for the actual meaning of these names
        "(#4, #5)" : {
            'eigenfaces' : ('linearize', 'pca'),
            'fisherfaces' : ('linearize', 'pca+lda'),
            'gabor-jet' : ('grid-graph', 'gabor-jet'),
            'lgbphs' : ('lgbphs', 'lgbphs'),
            'isv' : ('dct', 'isv')
        }
    }
}

# these packages need to be imported for the above configuration to work
imports = ['facereclib', 'xfacereclib.paper.IET2015']

