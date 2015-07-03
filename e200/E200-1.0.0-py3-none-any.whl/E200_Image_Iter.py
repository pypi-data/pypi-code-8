import numpy as _np
from .E200_load_images import E200_load_images
from .get_matlab import is_facet_srv
import ipdb  # NOQA
import logging
from .classes import E200_Image
logger = logging.getLogger(__name__)


# ======================================
# Image iterator
# ======================================
class E200_Image_Iter(object):
    def __init__(self, imgstr, uids=None, numperset=None):
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
        self._imgstr    = imgstr
        self._uids      = uids
        self._uids_orig = uids

    def __iter__(self):
        # ======================================
        # Initialize this loop
        # ======================================
        self._subind = 0
        if self._uids is None:
            self._uids = self._imgstr.UID

        self.load_next_batch()

        return self

    def __next__(self):
        if self._imgs_ind >= self._num_uids_load:
            self.load_next_batch()

        img   = _np.array([self._images.images[self._imgs_ind]])
        dat   = _np.array([self._images.dat[self._imgs_ind]])
        uid   = _np.array([self._images.uid[self._imgs_ind]])
        imgbg = self._images.image_backgrounds
        time  = _np.array([self._images.timestamps[self._imgs_ind]])

        out = E200_Image(images=img, dat=dat, uid=uid, image_backgrounds=imgbg, timestamps=time)
        self._imgs_ind = self._imgs_ind + 1
        return out

    def load_next_batch(self):
            # ======================================
            # Load only up to the next batch avail.
            # uids to prevent memory overflow
            # ======================================
            # ipdb.set_trace()
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
