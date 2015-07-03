import os as _os
import numpy as _np
import h5py as _h5
from .E200_api_getdat import E200_api_getdat
from .E200_Dat import *                        # noqa

__all__ = ['Data', 'Drill', 'E200_Dat', 'E200_Image']


class Data(object):
    def __enter__(self):
        return self

    def __init__(self, read_file, filename=None):
        self._filename = filename
        self.read_file = read_file
        self.rdrill    = Drill(read_file)

        # self.data=datalevel()
        # recursivePopulate(self._data, self)

    @property
    def filename(self):
        return self._filename

    @property
    def loadname(self):
        return _os.path.splitext(_os.path.basename(self.filename))[0]

    def close(self):
        self.read_file.close()

    def __exit__(self, type, value, traceback):
        self.close()


class Drill(object):
    def __init__(self, data):
        self._hdf5 = data
        #  self._mydir = []
        for key in data.keys():
            if key[0] != '#':
                #  self._mydir.append(key)
                out = data[key]
                if type(out) == _h5._hl.group.Group:
                    setattr(self, key, Drill(data[key]))
                elif key == 'dat' and ('UID' in data.keys()):
                    uids = data['UID'].value
                    dats = E200_api_getdat(data, uids)
                    setattr(self, key, dats.dat)
                elif len(out.shape) == 2:
                    if out.shape[0] == 1 or out.shape[1] == 1:
                        out = out.value.flatten()
                    setattr(self, key, out)
                elif key == 'UID':
                    setattr(self, key, data[key].value)
                #  elif type(out) == _h5._hl.dataset.Dataset:
                #          if
                #          if out[0][0]==_h5.h5r.Reference:
                #                  vals=[out.file[val[0]] for val in out]
                #          else:
                #                  vals = [val for val in out]
                #          if vals[0].shape[0]>1:
                #                  vals = [np.array(val).flatten() for val in vals]
                #                  vals = [''.join(vec.view('S2')) for vec in vals]
                #                  vals = np.array(vals)
                #          else:
                #                  vals = [val[0] for val in vals]
                #                  vals = np.array(vals)
                #          setattr(self, key, vals)
                else:
                    setattr(self, key, data[key])

    def __repr__(self):
        out = '\<E200.E200_load_data.Drill with keys:\n_hdf5'
        for val in self._hdf5.keys():
            out = out + '\n' + val

        out = out[1:] + '\n>'
        return out


class E200_Image(E200_Dat):
    def __init__(self, images, dat, uid, timestamps, image_backgrounds=None):
        self._imgs_subbed = None

        E200_Dat.__init__(self, dat, uid, field='dat')

        self._images            = images
        self._image_backgrounds = image_backgrounds
        self._timestamps        = timestamps

    def _get_images(self):
        return self._images
    images = property(_get_images)

    def _get_image_backgrounds(self):
        return self._image_backgrounds
    image_backgrounds = property(_get_image_backgrounds)

    @property
    def imgs_subbed(self):
        if self._imgs_subbed is None:
            self._imgs_subbed = self.images - 2*_np.fliplr(self.image_backgrounds)
        
        return self._imgs_subbed

    @property
    def timestamps(self):
        return self._timestamps
