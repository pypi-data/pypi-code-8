"""
.. module:: sim_process
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: Petr Zikan <zikan.p@gmail.com>

Nejkay kecy.

"""
from __future__ import absolute_import
import logging
from probe.plotting.plotting import Plotting
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants as C
from .sim_common import SimCommon

cfg = {'debug': 3}


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


class SimProcess(SimCommon):
    """
    This is a description of a class SimProcess. It serves for a "first-level"
    manipulation with hdf5 data from simulation.

    After initialization with hdf5 file, every object holds all important information
    about the simulation. As attributes it stores following data
    * self.m_e - mass of electron
    * self.m_Ar - mass of argon ion
    * self.commons -
    """

    def __init__(self, h5_filename):
        """
        Args:
            h5_filename (str): path to hdf5 file

        """
        SimCommon.__init__(self, h5_filename)

        self.m_e = C.m_e
        self.m_Ar = C.m_u * 39.948 - self.m_e

        self.commons = self.get_list_of_groups_as_dict('common')
        logger.debug('self.commons: %s', self.commons)

        self.runs = [int(x.split('_')[1]) for x in self.commons.values()]
        logger.debug('self.runs: %s', self.runs)

        self.gstats = self.get_list_of_groups_as_dict('gstats')
        logger.debug('self.gstats: %s', self.gstats)

        self.inits = self.get_list_of_groups_as_dict('init')
        logger.debug('self.inits: %s', self.inits)

        self.saves = self.get_list_of_groups_as_dict('save')
        logger.debug('self.saves: %s', self.saves)

        self.sweeps = self.get_list_of_groups_as_dict('sweep')
        logger.debug('self.sweeps: %s', self.sweeps)

        self.data = self.get_list_of_groups_as_dict('ts')
        logger.debug('self.data: %s', self.data)

        assert len(self.commons) == len(self.inits)

        self.no_runs = len(self.commons)
        logger.debug('self.no_runs: %s', self.no_runs)

        self.no_outputs = len(self.data)
        logger.debug('self.no_outputs: %s', self.no_outputs)

        self.r_grid = dict()
        self.rm_grid = dict()
        self.vol_grid = dict()
        self.params = dict()
        self.outputs = dict()

        for no_run in self.runs:
            self.r_grid[no_run] = self.h5_f['{}/r_grid'.format(self.commons[no_run])][...]
            self.rm_grid[no_run] = self.h5_f['{}/rm_grid'.format(self.commons[no_run])][...]
            self.vol_grid[no_run] = self.h5_f['{}/vol_grid'.format(self.commons[no_run])][...]
            self.params[no_run] = self.get_attrs_as_dict(self.commons[no_run])

        outputs = [1]
        last_output = 0
        for no_run in self.runs:
            Ntimes = self.params[no_run]['Ntimes']
            out_every = self.params[no_run]['out_every']
            for output_no in xrange(out_every + last_output, Ntimes + last_output + 1, out_every):
                outputs.append(output_no)
                last_output = output_no
            self.outputs[no_run] = outputs
            outputs = []

        logger.debug('self.r_grid: %s', self.r_grid)
        logger.debug('self.rm_grid: %s', self.rm_grid)
        logger.debug('self.vol_grid: %s', self.vol_grid)

        logger.debug('----------------')
        logger.debug('self.params[0]:')
        for param in self.params[0]:
            if isinstance(self.params[0][param], int) or isinstance(self.params[0][param], float):
                logger.debug('%s: %5.4e', param, self.params[0][param])
            else:
                logger.debug('%s: %s', param, self.params[0][param])

        self.stats = {
            'current' : list(),
            'nprobe_el' : list(),
            'nnew_el' : list(),
            'nprobe_ari' : list(),
            'nsheath_el' : list(),
            'nsheath_ari' : list(),
            'nnew_ari' : list(),
            'nactive_el' : list(),
            'nactive_ari' : list(),
            'time' : list(),
            'itime' : list(),
            'elapsed_time' : list()
        }

        self.get_stats()

        logger.debug('----------------')
        logger.debug('self.stats:')
        for stat in self.stats:
            logger.debug('%s: %s', stat, self.stats[stat])


    def __del__(self):
        self.h5_f.close()


    def close(self):
        self.h5_f.close()


    def get_attrs_as_dict(self, group):
        return {a : v[0] for a, v in self.h5_f['/{}'.format(group)].attrs.iteritems()}


    def get_stats(self):
        for ts in sorted(self.data.keys()):
            for attr, value in self.h5_f['/{}'.format(self.data[ts])].attrs.iteritems():
                self.stats[attr].append(value[0])


    def plot_current(self, print_to_file=False, print_filename='current.eps'):
        Plotting.plot_single_ax(self.stats['itime'], self.stats['current'], list_of_styles='b-',
                                xlabel='itime', ylabel='probe current [A]', print_to_file=print_to_file,
                                print_filename=print_filename)


    def animate_profiles(self, ne_ylim=None, phi_ylim=None, ts_from=1):
        fig, ax = plt.subplots(2, 1, sharex=True)

        tss = sorted(self.data.keys())
        ts_from = tss.index(ts_from)

        for itime in tss[ts_from:]:
            ax[0].clear()
            ax[1].clear()

            if ne_ylim is not None:
                ax[0].set_ylim(ne_ylim)

            if phi_ylim is not None:
                ax[1].set_ylim(phi_ylim)

            ax[0].plot(self.r_grid[0], self.h5_f[self.data[itime]]['num_el_grid'][...] / self.vol_grid[0], 'r-')
            ax[0].plot(self.r_grid[0], self.h5_f[self.data[itime]]['num_ari_grid'][...] / self.vol_grid[0], 'g-')
            ax[1].plot(self.r_grid[0], self.h5_f[self.data[itime]]['phi_grid'][...])
            plt.draw()
            plt.pause(0.1)


    def plot_all(self, ts):

        fig, ax = plt.subplots(2, 3)

        ax[0, 0].plot(self.r_grid[0], self.h5_f['/{}/num_el_grid'.format(self.data[ts])] / self.vol_grid[0], 'r-', label='n_e')
        ax[0, 0].plot(self.r_grid[0], self.h5_f['/{}/num_ari_grid'.format(self.data[ts])] / self.vol_grid[0], 'g-', label='n_i')
        ax[0, 0].set_xlabel('r [m]')
        ax[0, 0].set_ylabel('n_e, n_i [m^-3]')
        ax[0, 0].legend(loc='best')

        ax[1, 0].plot(self.r_grid[0], self.h5_f['/{}/phi_grid'.format(self.data[ts])], 'b-')
        ax[1, 0].set_xlabel('r [m]')
        ax[1, 0].set_ylabel('phi [V]')

        ax10_2 = ax[1, 0].twinx()
        ax10_2.plot(self.r_grid[0], self.h5_f['/{}/er_grid'.format(self.data[ts])], 'r-')
        ax10_2.set_ylabel('Er [V/m]')

        ax[0, 1].plot(self.r_grid[0], self.h5_f['/{}/lstat_el_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...], 'r-')
        ax[0, 1].set_xlabel('r [m]')
        ax[0, 1].set_ylabel('vr [m/s]')
        ax[0, 1].set_title('electron')

        ax[1, 1].plot(self.r_grid[0], self.m_e * self.h5_f['/{}/lstat_el_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_el_num'.format(self.data[ts])][...] / (3 * C.k), 'r-')
        ax[1, 1].set_xlabel('r [m]')
        ax[1, 1].set_ylabel('T [K]')
        ax[1, 1].set_title('electron')

        ax[0, 2].plot(self.r_grid[0], self.h5_f['/{}/lstat_ari_vr'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...], 'g-')
        ax[0, 2].set_xlabel('r [m]')
        ax[0, 2].set_ylabel('vr [m/s]')
        ax[0, 2].set_title('ion')

        ax[1, 2].plot(self.r_grid[0], self.m_Ar * self.h5_f['/{}/lstat_ari_v2'.format(self.data[ts])][...] / self.h5_f['/{}/lstat_ari_num'.format(self.data[ts])][...] / (3 * C.k), 'g-')
        ax[1, 2].set_xlabel('r [m]')
        ax[1, 2].set_ylabel('T [K]')
        ax[1, 2].set_title('ion')

        plt.show()


    def plot_profiles(self, list_of_ts):
        if not isinstance(list_of_ts, list):
            list_of_ts = [list_of_ts]

        list_to_plot = []
        list_of_labels = []

        for ts in list_of_ts:
            list_to_plot.append(self.h5_f['/{}/num_el_grid'.format(self.data[ts])][...] / self.vol_grid[0])
            list_of_labels.append('{} ne'.format(ts))
            list_to_plot.append(self.h5_f['/{}/num_ari_grid'.format(self.data[ts])][...] / self.vol_grid[0])
            list_of_labels.append('{} ni'.format(ts))

        Plotting.plot_single_ax([self.r_grid[0]] * len(list_to_plot), list_to_plot, list_of_labels=list_of_labels,
                                xlabel='r [m]', ylabel='n_e, n_i [m^-3]')
#                                print_to_file=print_to_file, print_filename=print_filename)


    def plot_stats_all(self):

        fig, ax = plt.subplots(3, 4)

        to_plot = ['itime', 'nnew_ari', 'time', 'nsheath_el',
                    'nactive_el', 'elapsed_time', 'nprobe_el', 'nactive_ari',
                    'nsheath_ari', 'current', 'nprobe_ari', 'nnew_el'
                  ]

        for irow in range(3):
            for icol in range(4):
                plot_no = icol + 4 * irow
                ax[irow, icol].plot(self.stats[to_plot[plot_no]])
                ax[irow, icol].set_title(to_plot[plot_no])
#                ax[irow, icol].set_xlabel('r [m]')
#                ax[irow, icol].set_ylabel('phi [V]')

        plt.show()


    def average_profiles(self, ts_from=1, ts_to=-1, plot=False):
        tss = sorted(self.data.keys())
        try:
            index_from = tss.index(ts_from)
        except ValueError:
            logger.error('there is no timestep %s', ts_from)
            return

        if ts_to == -1:
            index_to = tss[-1]
        else:
            try:
                index_to = tss.index(ts_to)
            except ValueError:
                logger.error('there is no timestep %s', ts_to)
                return

        ne_profile = self.h5_f['/{}/num_el_grid'.format(self.data[tss[index_from]])][...]
        ni_profile = self.h5_f['/{}/num_ari_grid'.format(self.data[tss[index_from]])][...]

        for ts in tss[index_from+1:index_to+1]:
            ne_profile += self.h5_f['/{}/num_el_grid'.format(self.data[ts])][...]
            ni_profile += self.h5_f['/{}/num_ari_grid'.format(self.data[ts])][...]

        ne_profile /= len(tss[index_from:index_to+1])
        ni_profile /= len(tss[index_from:index_to+1])

        ne_profile /= self.vol_grid[0]
        ni_profile /= self.vol_grid[0]

        if plot:
            Plotting.plot_single_ax([self.r_grid[0]] * 2, [ne_profile, ni_profile], list_of_labels=['n_e', 'n_i'],
                                    list_of_styles=['r-', 'g-'], xlabel='r [m]', ylabel='n_e, n_i [m^-3]')
        else:
            return ne_profile, ni_profile

    def test_particles_save(self, no_run):
        save_attrs = self.get_attrs_as_dict(self.saves[no_run])
        init_attrs = self.get_attrs_as_dict(self.inits[no_run+1])

        all_ok = True
        test_keys = ['itime', 'nprobe_tmp_Electron', 'nprobe_tmp_ArgonIon', 'nsheath_tmp_Electron',
                     'nsheath_tmp_ArgonIon', 'NNew_electron_tmp', 'NNew_ArgonIon_tmp', 'sweep_rest',
                    ]
        for key in test_keys:
            try:
                comparison = save_attrs[key] == init_attrs[key]
                logger.debug('key %s compared - %s', key, comparison)
                logger.debug('init: %s, save: %s', init_attrs[key], save_attrs[key])
                all_ok = all_ok and comparison
            except KeyError:
                logger.debug('cant compare %s, missing in one of attrs', key)

        logger.debug('ALL ATTRS TEST: %s', all_ok)

        ari_is_there = self.h5_f[self.saves[no_run]]['ari_is_there'][...]
        el_is_there = self.h5_f[self.saves[no_run]]['el_is_there'][...]

        mask_ari = ari_is_there == 1
        mask_el = el_is_there == 1

        dataset_to_test = 'ari_is_there'
        logger.debug('testing %s', dataset_to_test)
        self._test_particles_save_one(no_run, dataset_to_test)

        dataset_to_test = 'el_is_there'
        logger.debug('testing %s', dataset_to_test)
        self._test_particles_save_one(no_run, dataset_to_test)

        tests_ari = ['ari_vx', 'ari_vy', 'ari_vz', 'ari_x', 'ari_y', 'ari_z', 'ari_time_rest', 'ari_tau_c']
        tests_el = ['el_vx', 'el_vy', 'el_vz', 'el_x', 'el_y', 'el_z', 'el_time_rest', 'el_tau_c']

        for test_ari, test_el in zip(tests_ari, tests_el):
            logger.debug('testing %s', test_ari)
            self._test_particles_save_one(no_run, test_ari, mask=mask_ari)

            logger.debug('testing %s', test_el)
            self._test_particles_save_one(no_run, test_el, mask=mask_el)


    def _test_particles_save_one(self, no_run, dataset_name, mask=None):
        array1 = self.h5_f[self.saves[no_run]][dataset_name][...]
        array2 = self.h5_f[self.inits[no_run+1]][dataset_name][...]

        #import pdb; pdb.set_trace()

        if mask is None:
            logger.debug('sum1: {}, sum2: {}'.format(np.sum(array1), np.sum(array2)))
            assert np.allclose([np.sum(array1)], [np.sum(array2)], atol=1e-10, rtol=1e-10),\
                   '{}: sum1: {}, sum2: {}'.format(dataset_name, np.sum(array1), np.sum(array2))
        else:
            logger.debug('sum1: {}, sum2: {}'.format(np.sum(array1[mask]), np.sum(array2)))
            assert np.allclose([np.sum(array1[mask])], [np.sum(array2)], atol=1e-10, rtol=1e-8),\
                   '{}: sum1: {}, sum2: {}'.format(dataset_name, np.sum(array1), np.sum(array2))


    def test_stats(self):
        """
        This test can be ran only with special type of output data. To test whether gstats are really
        sum of all lstats, we need to have all lstats. Therefore, run simulation with out_every = 1 and
        every_ion = 1. Run the simulation only once and on these data run this test.
        """
        to_test = ['ari_num', 'el_num', 'ari_v2', 'el_v2', 'ari_vr', 'el_vr', 'ari_vr2', 'el_vr2',
                   'ari_vx', 'el_vx', 'ari_vy', 'el_vy', 'ari_vz', 'el_vz']
        for test in to_test:
            logger.debug('testing {}'.format(test))
            g = self.h5_f['/{}/gstat_{}'.format(self.gstats[0], test)][...]
            l = self.h5_f['/{}/lstat_{}'.format(self.data[1], test)][...]
            max_ts = max(self.data.keys())
            for ts in xrange(2, max_ts+1):
                l += self.h5_f['/{}/lstat_{}'.format(self.data[ts], test)][...]

        assert np.allclose(g, l), '{} g: {}, l: {}'.format(test, g, l)

