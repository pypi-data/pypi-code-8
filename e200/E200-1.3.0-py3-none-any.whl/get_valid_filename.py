import logging
loggerlevel = 9
loggerlevel = logging.DEBUG
logger      = logging.getLogger(__name__)

from .get_remoteprefix import *  # NOQA
from glob import glob as _glob
import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import scisalt as _mt
    import scisalt.qt as _mtqt
    from PyQt4 import QtGui as _QtGui
import os.path as _path
import re as _re
import warnings as _warnings


class Filename(object):
    def __init__(self, path, local=False):
        logger.log(level=loggerlevel, msg='Entering Filename class')
        self._local = local
        self.pathstr = path

    @property
    def experiment(self):
        match = _re.search('(?<=/)E\d{3}(?=/)', self.pathstr)
        experiment = match.group()
        return experiment

    # Return pathstr and set pathstr
    def _get_pathstr(self):
        return self._pathstr

    def _set_pathstr(self, value):
        # Reprocess pathstr
        self._pathstr          = value
        out                    = get_valid_filename(value, experiment=self.experiment, local=self._local)
        self._dir_beg          = out[0]
        self._dir_mid          = out[1]
        self._filename         = out[2]
        self._data_source_type = out[3]
    pathstr = property(_get_pathstr, _set_pathstr)

    # Retrieve dir_beg
    def _get_dir_beg(self):
        return self._dir_beg
    dir_beg = property(_get_dir_beg)

    # Retrieve dir_mid
    def _get_dir_mid(self):
        return self._dir_mid
    dir_mid = property(_get_dir_mid)

    # Retrieve filename
    def _get_filename(self):
        return self._filename
    filename = property(_get_filename)

    # Retrieve valid path
    def _get_valid_path(self):
        return '/'.join([self.dir_beg, self.dir_mid, self.filename])
    valid_path = property(_get_valid_path)

    # Retrieve data_source_type
    def _get_data_source_type(self):
        return self._data_source_type
    data_source_type = property(_get_data_source_type)

    def _get_processed_dir(self):
        processed_dir = _path.join(self.dir_beg, self.dir_mid)
        if not self._local:
            processed_dir = _re.sub('nas/nas-li20-pm0.', 'processed_data', processed_dir)
        return processed_dir
    processed_dir = property(_get_processed_dir)
    py_processed_dir = property(_get_processed_dir)

    def _get_processed_filename(self):
        fileparts = _path.splitext(self.filename)
        final_filename = '{}_processed{}'.format(fileparts[0], fileparts[1])
        return final_filename
    processed_filename = property(_get_processed_filename)

    def _get_processed_path(self):
        return _path.join(self.processed_dir, self.processed_filename)
    processed_path = property(_get_processed_path)

    def _get_py_processed_filename(self):
        return _re.sub('processed', 'py_processed', self.processed_filename)
    py_processed_filename = property(_get_py_processed_filename)
    
    def _get_py_processed_path(self):
        return _path.join(self.py_processed_dir, self.py_processed_filename)
    py_processed_path = property(_get_py_processed_path)


def get_valid_filename(pathstr, experiment, verbose=False, local=False):
    # File doesn't exist
    # This case must terminate in us trying again.
    logger.log(level=loggerlevel, msg='Input is: pathstr={}'.format(pathstr))

    # ======================================
    # Return info if the file is local
    # ======================================
    if local:
        if not _path.exists(pathstr):
            _warnings.warn('File not found: {}'.format(pathstr))
            #  raise IOError('File not found: {}'.format(pathstr))
        pathstr = _path.abspath(pathstr)
        dir_beg = ''
        dir_mid = _path.dirname(pathstr)
        filename = _path.basename(pathstr)
        data_source_type = '2014'
        output = (dir_beg, dir_mid, filename, data_source_type)
        return output

    # ======================================
    # Return info if the file is a nas file
    # ======================================
    if not _path.exists(pathstr):

        logger.log(level=loggerlevel, msg='Path does not exist: {}'.format(pathstr))
        # If file didn't exist, maybe it needs a prefix
        # Append prefix
        prefix = get_remoteprefix()
        pathstr = _path.join(prefix, pathstr)
        # print(prefix)

        # If it didn't work, we need to find the file somehow
        # The prefix may be wrong, the file may not be where we thought,
        # or the drive might not have been mounted and we can mount and
        # try again.
        if not _path.exists(pathstr):
            logger.log(level=loggerlevel, msg='Adding prefix didn''t help, new pathstr={}'.format(pathstr))

            title    = 'File not found!'
            maintext = 'File doesn''t exist:\n\n{}'.format(pathstr)
            subtext  = '(External drive may not be mounted.)'
            buttons  = _np.array([
                _mtqt.Button('Try again', _QtGui.QMessageBox.AcceptRole),
                _mtqt.Button('Change prefix', _QtGui.QMessageBox.ActionRole, default=True),
                _mtqt.Button('Locate file', _QtGui.QMessageBox.ActionRole),
                _QtGui.QMessageBox.Abort
                ])

            buttonbox = _mtqt.ButtonMsg(maintext, title=title, infotext=subtext, buttons=buttons)
            clicked   = buttonbox.clickedArray

            # Change prefix
            if clicked[0]:
                logger.log(level=loggerlevel, msg='Trying again')
            elif clicked[1]:
                logger.log(level=loggerlevel, msg='Changing prefix')

                prefix = _mt.E200.choose_remoteprefix(pathstart=prefix)
            # Locate file
            elif clicked[2]:
                logger.log(level=loggerlevel, msg='Locating file')

                # Try to open the path by chopping of the end
                while not _path.isdir(pathstr):
                    lastpath = pathstr
                    pathstr  = _path.dirname(pathstr)
                    # If you've chopped all you can chop, look in the base data folder
                    if lastpath == pathstr:
                        pathstr = _get_datapath()
                        break
                pathstr = _mtqt.getOpenFileName(directory=pathstr, caption='Locate file', filter='Matlab Files (*.mat)')
            elif clicked[3]:
                logger.log(level=loggerlevel, msg='Aborting')

                raise IOError('Aborting')
            else:
                print('Thar be dragons!')
        logger.log(level=loggerlevel, msg='Trying new pathstr={}'.format(pathstr))

        return get_valid_filename(pathstr)
    elif _path.isdir(pathstr):
        logger.log(level=loggerlevel, msg='Path is a directory')

        patterns = ['*scan_info.mat', '*filenames.mat', '{}_*.mat'.format(experiment)]
        files    = _np.array([])
        for i, val in enumerate(patterns):
            gfiles = _glob(_path.join(pathstr, val))
            files = _np.append(files, gfiles)
        logger.log(level=loggerlevel, msg='Files match patterns\npatterns: {}\nfiles: {}'.format(patterns, files))

        if files.size == 1:
            logger.log(level=loggerlevel, msg='Found one file.')

            pathstr = files[0]
        elif files.size == 0:
            logger.log(level=loggerlevel, msg='Found no files.')

            title    = 'File Not Found'
            maintext = 'No valid file found in folder.'
            subtext  = 'Locate manually?'
            buttons  = _np.array([
                _QtGui.QMessageBox.Ok,
                _QtGui.QMessageBox.Abort
                ], dtype=object)

            buttonbox = _mtqt.ButtonMsg(maintext, title=title, infotext=subtext, buttons=buttons)
            clicked   = buttonbox.clickedArray

            if clicked[0]:
                logger.log(level=loggerlevel, msg='Trying to locate manually.')

                pathstr = _mtqt.getOpenFileName(directory=pathstr, caption='Locate file', filter='Matlab Files (*.mat)')
            elif clicked[1]:
                logger.log(level=loggerlevel, msg='Aborting.')

                raise IOError('Aborting')
        logger.log(level=loggerlevel, msg='Trying new pathstr={}'.format(pathstr))

        return get_valid_filename(pathstr)

    elif _path.isfile(pathstr):
        logger.log(level=loggerlevel, msg='Path is a file.')

        # Check for string endings
        strends = _np.array(['scan_info.mat$', 'filenames.mat$', '{}_[0-9]*\.mat'.format(experiment)])
        strmatch = _np.empty(strends.size, dtype=object)
        for i, val in enumerate(strends):
            strmatch[i] = _re.search(val, pathstr)

        # True for matches
        strmatch_bool = _np.not_equal(strmatch, None)

        # Warn if there are no matches
        if not _np.any(strmatch_bool):
            logger.log(level=loggerlevel, msg='File doesn''t match patterns={}'.format(strends))

            _warnings.warn('Neither a 2014+ data file, scan_info.mat file, nor a filenames.mat file: {}'.format(pathstr))

        if strmatch_bool[2]:
            data_source_type = '2014'
        else:
            data_source_type = '2013'

        logger.log(level=loggerlevel, msg='data_source_type is {}'.format(data_source_type))

        # Check that this is a data file
        # Must have /nas/nas-li20-pm01
        match = _re.search('/nas/nas-li20-pm0', pathstr)
        if match is None:
            raise IOError('Does not point to a file with /nas/nas-li20-pm01 or /nas/nas-li20-pm00 in its path.')

        # Get the directories
        dirstr   = _path.dirname(pathstr)
        filename = _path.basename(pathstr)
        
        dir_beg = dirstr[:match.start()]
        dir_mid = dirstr[match.start()+1:]

        output = (dir_beg, dir_mid, filename, data_source_type)
        logger.log(level=loggerlevel, msg='Output is: {}'.format(output))

        return output
