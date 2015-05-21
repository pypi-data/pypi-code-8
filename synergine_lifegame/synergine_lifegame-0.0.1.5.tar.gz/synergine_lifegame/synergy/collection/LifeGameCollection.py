from synergine.synergy.collection.SynergyCollection import SynergyCollection
from synergine_lifegame.synergy.event.DieAction import DieAction
from synergine_lifegame.synergy.event.BornAction import BornAction
from synergine_lifegame.synergy.event.TimePassAction import TimePassAction


class LifeGameCollection(SynergyCollection):
    """
    This collection own cells of simulation.
    """

    def __init__(self, configuration):
        super().__init__(configuration)
        # We list here actions who concern our simulation.
        self._actions = [DieAction, BornAction, TimePassAction]
