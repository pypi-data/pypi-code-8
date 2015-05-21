from synergine.lib.eint import IncrementedNamedInt

ALIVE = IncrementedNamedInt.get('synergine_lifegame.alive')
DIED = IncrementedNamedInt.get('synergine_lifegame.died')

COL_DIED = IncrementedNamedInt.get('synergine_lifegame.col.died')
COL_ALIVE = IncrementedNamedInt.get('synergine_lifegame.col.alive')
