#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Manuel Guenther <Manuel.Guenther@idiap.ch>

# This file includes the setup for the set of experiments ran to re-generate Figure 4 of the paper.

# The preprocessor, with different standard deviations for the translations in y and x direction, as well as different random seeds.
preprocessor = 'xfacereclib.paper.IET2015.facereclib.RandomPerturbation(cropped_image_size=(80,64), cropped_positions = {"reye":(16,15), "leye":(16,48)}, sigma=(#1,#2), seed=#3)'

# The feature extractor, which differs for all face recognition algorithms
feature_extractor = "#4"

# The face recognition algorithm
tool = "#5"

# The set of parameters that should be tested
replace = {
    # define, which parameters affect only the preprocessing stage
    'preprocessing' : {
        # replace #1 (i.e., the y-standard deviation in the preprocessor) with these values:
        '#1' : {
            'sy+1' : 1,
            'sy+2' : 2,
            'sy+3' : 3,
            'sy+4' : 4,
            'sy+5' : 5,
            'sy+7' : 7,
            'sy+9' : 9,
        },
        # replace #2 (i.e., the x-standard deviation in the preprocessor) with these values:
        '#2' : {
            'sx+1' : 1,
            'sx+2' : 2,
            'sx+3' : 3,
            'sx+4' : 4,
            'sx+5' : 5,
            'sx+7' : 7,
            'sx+9' : 9,
        },
        # replace #3 (i.e., the random seed in the preprocessor) with these values:
        '#3' : {
            'seed1' : 95359,
            'seed2' : 4464,
            'seed3' : 29721
        }
    },

    # define, which parameters affect only the feature extraction stage
    'extraction' : {
        # since feature extraction and face recognition algorithm are bound together, we define both of them here, i.e., as a tuple
        # replace #4 with the first value (the feature extractor) and #5 with the second value (the face recognition algorithm) **at the same time**
        # See FaceRecLib documentation for the actual meaning of these names
        '(#4, #5)' : {
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

