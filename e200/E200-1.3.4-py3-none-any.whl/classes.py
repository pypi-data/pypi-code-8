import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    import re as _np
    import re as _h5
else:
    import numpy as _np
    import h5py as _h5
from .E200_api_getdat import E200_api_getdat
from .E200_Dat import *                        # noqa

__all__ = ['Data', 'Drill', 'E200_Dat', 'E200_Image']


class Data(object):
    """
    Top-level data file representing all information for a single dataset loaded from *filename*. *read_file* (type :class:`h5py._hl.files.File`, an h5py file) is the loaded data, to be read-only.

    **Should not be created directly, only accessed through** :func:`E200.E200_load_data` **or** :func:`E200.E200_load_data_gui`\ **.**
    """
    def __init__(self, read_file, filename=None):
        self._filename = filename
        self.read_file = read_file
        self.rdrill    = Drill(read_file)

        # self.data=datalevel()
        # recursivePopulate(self._data, self)

    def __enter__(self):
        return self

    @property
    def filename(self):
        """
        The *filename* the dataset was loaded with.
        """
        return self._filename

    @property
    def loadname(self):
        """
        The name of the dataset (i.e. :code:`'E217_17990'`).
        """
        return _os.path.splitext(_os.path.basename(self.filename))[0]

    def close(self):
        """
        Closes the *read_file*
        """
        self.read_file.close()

    def __exit__(self, type, value, traceback):
        self.close()


class Drill(object):
    """
    Designed for representing hierarchical h5py data. *data* (type :class:`h5py._hl.files.File`, an h5py file) is the h5py file at a particular hierarchical depth.

    Members: If not nested :class:`E200.Drill` objects, they may be arrays representing various types of information particular to their parent.
    
    **Should not be created directly, only accessed through** :func:`E200.E200_load_data` **or** :func:`E200.E200_load_data_gui`\ **.**
    """
    def __init__(self, data):
        self._hdf5 = data
        for key in data.keys():
            if key[0] != '#':
                out = data[key]
                if type(out) == _h5._hl.group.Group:
                    setattr(self, key, Drill(out))
                elif key == 'desc':
                    desc = out.value.flatten()
                    desc = desc.view('S2')
                    desc = _np.char.decode(desc, 'UTF-8')
                    setattr(self, key, ''.join(desc))
                elif key == 'dat' and ('UID' in data.keys()):
                    uids = data['UID'].value
                    dats = E200_api_getdat(data, uids)
                    setattr(self, key, dats.dat)
                elif len(out.shape) == 2:
                    if out.shape[0] == 1 or out.shape[1] == 1:
                        out = out.value.flatten()
                    setattr(self, key, out)
                elif key == 'UID':
                    setattr(self, key, out.value)
                else:
                    setattr(self, key, out)

    def __repr__(self):
        out = '\<E200.E200_load_data.Drill with keys:\n_hdf5'
        for val in self._hdf5.keys():
            out = out + '\n' + val

        out = out[1:] + '\n>'
        return out


class E200_Image(E200_Dat):
    """
    Bases: :class:`E200.E200_Dat`

    Contains image data. This is designed to prevent accidental incorrect correlation of images with UIDs, in case a request for images cannot find UIDs.

    **Should not be created directly, only accessed through** :func:`E200.E200_load_images`\ **.**
    """
    def __init__(self, images, dat, uid, timestamps, image_backgrounds=None):
        self._imgs_subbed = None

        E200_Dat.__init__(self, dat, uid, field='dat')

        self._images            = images
        self._image_backgrounds = image_backgrounds
        self._timestamps        = timestamps

    @property
    def images(self):
        """
        An array of images, correlated with :attr:`E200.E200_Image.UID`.
        """
        return self._images

    @property
    def image_backgrounds(self):
        """
        An array of image backgrounds,  correlated with :attr:`E200.E200_Image.UID`.
        """
        return self._image_backgrounds

    @property
    def imgs_subbed(self):
        """
        An array of images with backgrounds subtracted,  correlated with :attr:`E200.E200_Image.UID`.
        """
        if self._imgs_subbed is None:
            self._imgs_subbed = self.images - 2*_np.fliplr(self.image_backgrounds)
        
        return self._imgs_subbed

    @property
    def timestamps(self):
        """
        An array of timestamps indicating when :attr:`E200.E200_Image.images` were taken, correlated with :attr:`E200.E200_Image.UID`.
        """
        return self._timestamps
