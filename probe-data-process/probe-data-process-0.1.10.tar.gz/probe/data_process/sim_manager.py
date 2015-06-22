from __future__ import absolute_import
import logging
import sys
from .sim_process import SimProcess
import matplotlib.pyplot as plt
import numpy as np
import boltons

logger = logging.Logger('NULL')
logger.addHandler(logging.NullHandler())

cfg = {'debug' : 2}

class MultiLineFormatter(logging.Formatter):

    def __init__(self, fmt, datefmt):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        # hack: http://stackoverflow.com/a/5879524/533618
        backup_exc_text = record.exc_text
        record.exc_text = None
        formatted = logging.Formatter.format(self, record)
        header = formatted.split(record.message)[0]
        record.exc_test = backup_exc_text
        return header + ('\n' + header).join(it for it in record.message.split('\n') if it)


logger = logging.getLogger()
logger.setLevel({1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}.get(cfg['debug'], 0))
sh = logging.StreamHandler(sys.stderr)
fmt = '%(asctime)s.%(msecs).03d %(process)+5s %(levelname)-8s %(filename)s:%(lineno)d:%(funcName)s(): %(message)s'
sh.setFormatter(MultiLineFormatter(fmt, '%Y-%m-%d %H:%M:%S'))
logger.handlers = []
logger.addHandler(sh)

class SimManager(object):

    def __init__(self, h5_paths_dict):

        """
        This object can handle a compare results from multiple simulations.

        It should be initialized by a dictionary, where key is a short description
        of the simluation and a value is a path to h5 file with results.
        """

        self.h5_paths_dict = h5_paths_dict
        logger.debug('self.h5_paths_dict: %s', self.h5_paths_dict)

        self.sim_processes = dict()
        for desc, path_to_h5 in self.h5_paths_dict.iteritems():
            logger.info('initializing sim_process, desc: %s, path: %s', desc, path_to_h5)
            self.sim_processes[desc] = SimProcess(path_to_h5)


    def plot_current(self, fit_from=None, filename=None, figsize=(25, 13)):

        if fit_from is not None:
            fit_from_dict = self.parse_ts_from_to(fit_from)
            logger.debug('fit_from_dict: %s', fit_from_dict)

        _, ax = plt.subplots(figsize=figsize)
        current_fit = dict()
        fit_from_index_dict = dict()
        for desc, sp in self.sim_processes.iteritems():
            if fit_from is not None:
                fit_from_index_dict[desc] = self.sim_processes[desc].stats['itime'].index(fit_from_dict[desc])
                logger.debug('desc: %s, fit_from_index: %s', desc, fit_from_index_dict[desc])

                current_fit[desc] = np.polyfit(sp.stats['itime'][fit_from_index_dict[desc]:],
                                               sp.stats['current'][fit_from_index_dict[desc]:],
                                               0)[0]


            ax.plot(sp.stats['itime'], sp.stats['current'], label=desc)
            if fit_from is not None:
                ax.plot([sp.stats['itime'][fit_from_index_dict[desc]], sp.stats['itime'][-1]],
                        [current_fit[desc], current_fit[desc]],
                        label='{}, {}'.format(desc, current_fit[desc]))

        ax.legend(loc='best')

        if filename is not None:
            plt.savefig(filename)
        else:
            plt.show()


    def parse_ts_from_to(self, ts):
        if isinstance(ts, int):
            ts_dict = dict()
            for desc, _ in self.h5_paths_dict.iteritems():
                ts_dict[desc] = ts
        elif isinstance(ts, dict):
            ts_dict = ts
        elif isinstance(ts, list) or isinstance(ts, tuple):
            ts_dict = dict()

            c = 0
            for desc, _ in self.h5_paths_dict.iteritems():
                ts_dict[desc] = ts[c]
                c += 1

            print ts_dict
        else:
            raise ValueError('ts_from must be integer, dict, list or tuple, see docstring')

        return ts_dict


    def plot_averaged_profiles(self, ts_from=1, ts_to=-1, scale_by_rd=False, filename=None,
                         figsize=(25, 13), n_infty=None):
        """
        plot averaged profiles of all simulations

        arguments:

        ts_from     should be either integer (average all simulation from that ts)
                    or dict (keys are same strings as in h5_paths_dict in __init__)
        ts_to       similar to ts_from
        """
        is_iterable = boltons.iterutils.is_iterable

        if is_iterable(ts_from):
            index_from = {label: self.sim_processes[label].timestep2dataindex(ts_f) for label, ts_f in ts_from.iteritems()}
        else:
            index_from = {label: self.sim_processes[label].timestep2dataindex(ts_from) for label in self.sim_processes.iterkeys()}

        if is_iterable(ts_to):
            index_to = {label: self.sim_processes[label].timestep2dataindex(ts_t) for label, ts_t in ts_to.iteritems()}
        else:
            index_to = {label: self.sim_processes[label].timestep2dataindex(ts_to) for label in self.sim_processes.iterkeys()}

        assert set(index_from.keys()) == set(index_to.keys())

        print 'averaging profiles'
        averaged_profiles = dict()
        for desc in index_from.iterkeys():
            averaged_profiles[desc] = self.sim_processes[desc].average_profiles(index_from[desc],
                                                                                index_to[desc],
                                                                               )
        print 'profiles averaged'

#        logger.debug('averaged_profiles: %s', averaged_profiles)
#        fig = plt.figure(figsize=figsize)
        ax_el = plt.subplot2grid((2, 2), (0, 0))
        ax_ion = plt.subplot2grid((2, 2), (0, 1))
        ax_all = plt.subplot2grid((2, 2), (1, 0), colspan=2)
#        fig.tight_layout()

        for desc in averaged_profiles.iterkeys():
            if scale_by_rd:
                ax_el.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                           averaged_profiles[desc]['ne'],
                           label='{} el'.format(desc))
            else:
                ax_el.plot(self.sim_processes[desc].r_grid[0],
                           averaged_profiles[desc]['ne'],
                           label='{} el'.format(desc))

        ax_el.legend(loc='best')

        for desc in averaged_profiles.iterkeys():
            if scale_by_rd:
                ax_ion.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                            averaged_profiles[desc]['ni'],
                            label='{} ion'.format(desc))
            else:
                ax_ion.plot(self.sim_processes[desc].r_grid[0],
                            averaged_profiles[desc]['ni'],
                            label='{} ion'.format(desc))

        ax_ion.legend(loc='best')

        for desc in averaged_profiles.iterkeys():
            if scale_by_rd:
                ax_all.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                            averaged_profiles[desc]['ne'],
                            label='{} el'.format(desc))
                ax_all.plot(self.sim_processes[desc].r_grid[0] / self.sim_processes[desc].params[0]['r_d'],
                            averaged_profiles[desc]['ni'],
                            label='{} ion'.format(desc))
            else:
                ax_all.plot(self.sim_processes[desc].r_grid[0],
                            averaged_profiles[desc]['ne'], label='{} el'.format(desc))
                ax_all.plot(self.sim_processes[desc].r_grid[0],
                            averaged_profiles[desc]['ni'], label='{} ion'.format(desc))

        ax_all.legend(loc='best')

        if n_infty:
            ax_el.plot([self.sim_processes[desc].params[0]['r_p'], self.sim_processes[desc].params[0]['r_d']],
                       [n_infty, n_infty])
            ax_ion.plot([self.sim_processes[desc].params[0]['r_p'], self.sim_processes[desc].params[0]['r_d']],
                       [n_infty, n_infty])
            ax_all.plot([self.sim_processes[desc].params[0]['r_p'], self.sim_processes[desc].params[0]['r_d']],
                       [n_infty, n_infty])


        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
