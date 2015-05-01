import h5py
from .experiment_data import ExperimentData
from .utils import summary_dec


class ExperimentsData(object):

    def __init__(self, h5fname, mode='r'):
        self.h5file = h5py.File(h5fname, mode=mode)

    @property
    def experiments(self):
        groups = [group
                  for group in self.h5file.values()
                  if group.attrs.get('_is_experiment', False)]
        experiments = map(ExperimentData, groups)
        return sorted(experiments, key=lambda e: e.time)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.h5file.close()

    @summary_dec
    def summary(self):
        yield 'File: %s' % self.h5file.filename
        yield 'Experiments (%d items):' % len(self.experiments)
        for i, exp in enumerate(self.experiments):
            yield 1, '{i}. {exp.group.name}: {exp.name} at {exp.time_str}'.format(exp=exp, i=i), exp

    def __str__(self):
        return 'ExperimentsData <file "%s">' % (self.h5file.filename)

    __repr__ = __str__
