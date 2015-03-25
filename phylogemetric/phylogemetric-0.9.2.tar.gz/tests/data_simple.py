# SplitsTree:
#
# Executing: analysis distances once DeltaScore SelectedTaxa=0 ;
# Delta scores for individual taxa
# Id      Taxon   Delta Score     Q-residual
# 1       A       0.14375 0.042517
# 2       B       0.08125 0.028345
# 3       C       0.1125  0.028345
# 4       D       0.14375 0.042517
# 5       E       0.09375 0.028345
# ===========================
#
# Delta score = 0.115
# Q-residual score = 0.03401

MATRIX = {
    'A': [
        '1', '1', '1', '1', '0', '0', '1', '1', '1', '0', '1', '1',
        '1', '1', '0', '0', '1', '1', '1', '0'
    ],
    'B': [
        '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1',
        '1', '1', '1', '0', '0', '1', '1', '1'
    ],
    'C': [
        '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '0',
        '0', '0', '0', '1', '0', '1', '1', '1'
    ],
    'D': [
        '1', '0', '0', '0', '0', '1', '0', '1', '1', '1', '1', '0',
        '0', '0', '0', '1', '0', '1', '1', '1'
    ],
    'E': [
        '1', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '0',
        '0', '0', '0', '1', '1', '1', '1', '1'
    ],
}

EXPECTED = {
    'A': {
        'delta': 0.14375,
        'q': 0.042517,
    },
    'B': {
        'delta': 0.08125,
        'q': 0.028345,
    },
    'C': {
        'delta': 0.1125,
        'q': 0.028345,
    },
    'D': {
        'delta': 0.14375,
        'q': 0.042517,
    },
    'E': {
        'delta': 0.09375,
        'q': 0.028345,
    },
}



