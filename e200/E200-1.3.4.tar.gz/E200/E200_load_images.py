# import tifffile
from .E200_api_getdat import E200_api_getdat
from .classes import *  # NOQA
from .get_remoteprefix import get_remoteprefix
import PIL
import logging
import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import scipy.io as _spio
import os
loggerlevel = logging.DEBUG
logger      = logging.getLogger(__name__)


def E200_load_images(img_dataset, UID=None):
    """
    Loads available images from *img_dataset* (type :class:`E200.Drill` containing camera data) corresponding to *UID* (:code:`array` or number).

    Returns an instance of :class:`E200.E200_Image`.
    """
    logger.log(level=loggerlevel, msg='Loading images...')
    try:
        remote_bool = img_dataset._hdf5.file['data']['VersionInfo']['remotefiles']['dat'][0, 0]
    except:
        remote_bool = True
    if remote_bool:
        prefix = get_remoteprefix()
    else:
        prefix = ''

    imgdat = E200_api_getdat(img_dataset, UID=UID)

    imgs = _np.array([PIL.Image.open(os.path.join(prefix, val[1:])) for val in imgdat.dat], dtype=object)
    num_imgs = _np.size(imgs)
    timestamps = _np.empty(num_imgs)
    for i, img in enumerate(imgs):
        img_arr       = _np.asarray(img)
        imgs[i]       = _np.uint64(img_arr)
        timestamps[i] = img.tag[65002][0]

    logger.log(level=loggerlevel, msg='Loading backgrounds...')

    imgbgdat = E200_api_getdat(img_dataset, fieldname='background_dat', UID=imgdat.uid)

    # for i, val in enumerate(imgbgdat.dat):
    # print val
    i = 0
    val = imgbgdat.dat[i]
    val = os.path.join(prefix, val[1:])
    mat = _spio.loadmat(val)
    imgbg = mat['img']
        
    # if imgs[i].shape[0] == imgbg.shape[1]:
    #     imgbg = _np.transpose(imgbg)

    # imgs[i] = _np.fliplr(_np.abs(imgs[i]-_np.float64(imgbg)))

    return E200_Image(images=_np.array(imgs), dat=imgdat.dat, uid=imgdat.uid, image_backgrounds=imgbg, timestamps=timestamps)
