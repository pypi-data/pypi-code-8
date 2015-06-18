links = {1: {'grade': -1.2,
'length': 0.25,
'road_type': 5,
'source_distr': {21: 1.0},
'speed': 34,
'volume': 400}}

activity =  {'age_distr': {21: {5: 1.0}},
    'county': 50027,
    'day_type': 5,
    'hour': 16,
    'month': 6,
    'year': 2015,
    'links': links}

options = {'detail': 'average', 'breakdown':['process']}

import moves
reload(moves)
m = moves.Moves(activity, options)
m.cleanup = False
emissions_out = m.run()
#emissions_out = list(emissions_out)

