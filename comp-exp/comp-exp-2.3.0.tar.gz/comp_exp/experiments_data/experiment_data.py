from .experiment_step_data import ExperimentStepData
from .utils import summary_dec


class ExperimentData(object):

    def __init__(self, h5group):
        self.group = h5group

    @property
    def time(self):
        try:
            return self.group.attrs['time_sec']
        except:
            return None

    @property
    def time_str(self):
        return self.group.attrs['time_str']

    @property
    def name(self):
        return self.group.attrs['name']

    @property
    def attrs(self):
        return self.group.attrs

    @property
    def steps(self):
        steps_groups = self.group.values()
        steps = map(ExperimentStepData, steps_groups)
        return sorted(steps, key=lambda s: s.ind)

    @summary_dec
    def summary(self):
        yield 'Experiment: {s.name} at {s.time_str}'.format(s=self)
        yield 'Stored as: {gr.file.filename}{gr.name}'.format(gr=self.group)
        yield 'Steps (%d items):' % len(self.steps)
        for step in self.steps:
            yield 1, '{s.ind}. {s.name}'.format(s=step), step

    def __str__(self):
        return 'ExperimentData <"%s" at %s>' % (self.name, self.time_str)

    __repr__ = __str__
