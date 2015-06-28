VERSION = (0, 1, 0, 'alpha', 1)

main = '.'.join(map(str, VERSION[:2] if VERSION[2] == 0 else VERSION[:3]))

sub = ''
if VERSION[3] != 'final':
    mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
    sub = mapping[VERSION[3]] + str(VERSION[4])

__version__ = main + sub
