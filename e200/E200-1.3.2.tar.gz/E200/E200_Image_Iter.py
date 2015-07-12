import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
from .E200_load_images import E200_load_images
from .get_matlab import is_facet_srv
import logging
from .classes import E200_Image
logger = logging.getLogger(__name__)


# ======================================
# Image iterator
# ======================================
class E200_Image_Iter(object):
    """
    Iterable object for use in embedding in :code:`for` loops to prevent running out of memory. Loads available images from *img_dataset* (type :class:`E200.Drill` containing camera data). If *UID* is present, only loads matching UIDs. Loads *numperset* images at a time.

    *(Note: Can and should be used directly!)*
    """
    def __init__(self, img_dataset, UID=None, numperset=None):
        # ======================================
        # Check platform (only facet-srvs have
        # major memory issues)
        # ======================================
        if numperset is None:
            if is_facet_srv():
                numperset = 50
            else:
                numperset = 500

        # ======================================
        # Initialize requested iterator
        # ======================================
        self._numperset = numperset
        self._imgstr    = img_dataset
        self._uids      = UID
        self._uids_orig = UID

    def __iter__(self):
        # ======================================
        # Initialize this loop
        # ======================================
        self._subind = 0
        if self._uids is None:
            self._uids = self._imgstr.UID

        self._load_next_batch()

        return self

    def __next__(self):
        if self._imgs_ind >= self._num_uids_load:
            self._load_next_batch()

        img   = _np.array([self._images.images[self._imgs_ind]])
        dat   = _np.array([self._images.dat[self._imgs_ind]])
        uid   = _np.array([self._images.uid[self._imgs_ind]])
        imgbg = self._images.image_backgrounds
        time  = _np.array([self._images.timestamps[self._imgs_ind]])

        out = E200_Image(images=img, dat=dat, uid=uid, image_backgrounds=imgbg, timestamps=time)
        self._imgs_ind = self._imgs_ind + 1
        return out

    def _load_next_batch(self):
            # ======================================
            # Load only up to the next batch avail.
            # uids to prevent memory overflow
            # ======================================
            num_uids_left = _np.size(self._uids)
            logger.debug('Number of UIDs left: {}'.format(num_uids_left))

            if num_uids_left == 0:
                raise StopIteration

            if self._numperset == -1:
                uids = self._uids
            else:
                uid_ind = _np.min([num_uids_left, self._numperset])
                uids = self._uids[0:uid_ind]
            self._num_uids_load = _np.size(uids)

            self._images = E200_load_images(self._imgstr, UID=uids)
            self._imgs_ind = 0

            self._uids = _np.delete(self._uids, slice(0, self._num_uids_load))

            return
