import E200
import numpy as np
import scipy.optimize as spopt
import matplotlib.pyplot as plt
import scisalt as mt
__all__ = ['eaxis', 'eaxis_ELANEX', 'yaxis_ELANEX', 'yanalytic', 'E_no_eta', 'y_no_eta']

import logging
loggerlevel = logging.DEBUG
logger      = logging.getLogger(__name__)


def eaxis(y, uid, camname, hdf5_data, E0=20.35, etay=0, etapy=0):
    logger.log(level=loggerlevel, msg='Getting energy axis...')

    # eaxis     = E200.eaxis(camname=camname, y=y, res=res, E0=20.35, etay=0, etapy=0, ymotor=ymotor)
    imgstr = hdf5_data['raw']['images'][str(camname)]
    res    = np.float64(imgstr['RESOLUTION'][0, 0])
    res    = res*np.float64(1.0e-6)

    logger.log(level=loggerlevel, msg='Camera detected: {}'.format(camname))
    if camname == 'ELANEX':
        ymotor = hdf5_data['raw']['scalars']['XPS_LI20_DWFA_M5']['dat']
        ymotor = mt.derefdataset(ymotor, hdf5_data.file)
        ymotor = ymotor[0]*1e-3
        logger.log(level=loggerlevel, msg='Original ymotor is: {}'.format(ymotor))

        raw_rf     = hdf5_data['raw']
        scalars_rf = raw_rf['scalars']
        setQS_str  = scalars_rf['step_value']
        setQS_dat  = E200.E200_api_getdat(setQS_str, uid).dat[0]
        setQS      = mt.hardcode.setQS(setQS_dat)

        logger.log(level=loggerlevel, msg='Eaxis''s setQS is: {}'.format(setQS_dat))

        ymotor = setQS.elanex_y_motor()*1e-3
        logger.log(level=loggerlevel, msg='Reconstructed ymotor is: {ymotor}'.format(ymotor=ymotor))

        return eaxis_ELANEX(y=y, res=res, etay=etay, etapy=etapy, ymotor=ymotor)

    elif camname == 'CMOS_FAR':
        return eaxis_CMOS_far(y=y, res=res, E0=E0, etay=etay, etapy=etapy)

    else:
        msg = 'No energy axis available for camera: {}'.format(camname)
        logger.log(level=loggerlevel, msg=msg)
        raise NotImplementedError(msg)


def eaxis_ELANEX(y, res, etay=None, etapy=None, ypinch=None, img=None, ymotor=None):
    ymotor = np.float64(ymotor)
    y      = y+ymotor/res

    #  y_motor_calibrated = np.float64(-1e-3)
    #  y_pinch_calibrated = np.float64(130)
    #  y_pixel_size       = np.float64(4.65e-6)
    #  E0 = 20.35

    #  y_motor_calibrated = np.float64(-0.00677574370709)
    #  y_pinch_calibrated = np.float64(211)
    #  y_pixel_size       = np.float64(8.9185e-6)
    E0 = 23.737805394397343771

    # ypinch = y_pinch_calibrated + y_motor_calibrated/y_pixel_size

    # E0=20.35 observed at 130px, motor position -1mm
    #  E0=20.35

    theta  = np.float64(6e-3)
    Lmag   = np.float64(2*4.889500000E-01)
    Ldrift = np.float64(8.792573)

    logger.log(level=loggerlevel, msg='ypinch is: {}'.format(ypinch))
    logger.log(level=loggerlevel, msg='ymotor is: {}'.format(ymotor))

    out = E_no_eta(y, ypinch, res, Ldrift, Lmag, E0, theta)
    return out


def yaxis_ELANEX(E, res, E0=None, etay=None, etapy=None, ypinch=None, img=None, ymotor=None):
    # y=0
    def merit_fcn(y, res, E0=None, etay=None, etapy=None, ypinch=None, img=None, ymotor=None):
        val = eaxis_ELANEX(y, res, E0, etay, etapy, ypinch, img, ymotor)
        print('===========')
        print(y)
        print(val)
        print(E)
        out = (E-val)**2
        print(out)
        return out

    etay   = 0
    etapy  = 0
    ypinch = 0
    img    = 0

    # args = np.array([res, E0, etay, etapy, ypinch, img, ymotor])
    args = (res, E0, etay, etapy, ypinch, img, ymotor)

    # print(merit_fcn(0, res, E0, etay, etapy, ypinch, img, ymotor))
    # print(args)
    outval = spopt.minimize(merit_fcn, x0=np.array([-4000]), args=args, tol=1e-7)
    print(outval)
    return outval.x[0]


def eaxis_CMOS_far(y, res, E0=None, etay=None, etapy=None, img=None):
    # The axis is flipped.  Since the offset is arbitrary and
    # calibrated for below, I can use an arbitrary offset here
    # in order to flip the axis. I've decided on a random value of 4000
    # since I'm pretty sure none of our photos have a resolution
    # greater than that, and I'm trying to error out on a negative
    # value.
    ypinch = 1660
    y_flip_offset = max(y) + 10
    y = y_flip_offset - y
    ypinch = y_flip_offset - ypinch
    if min(y) < 0:
        raise ValueError('y<0 indicates my arbitrary offset is bad. Change source code!')
    if etay is None:
        etay = input('Dispersion in y in mm (eta_y)? ')
        etay = etay * 1e-3
        print('Dispersion entered is {}'.format(etay))

    if etapy is None:
        etapy = input('Dispersion-prime in y in mrad (eta''_y)? ')
        etapy = etapy * 1e-3
        print('Dispersion-prime entered is {}'.format(etapy))

    if img is not None:
        plt.imshow(img)
        plt.show()
    if ypinch is None:
        ypinch = input('Location of zero energy in y in pixels? ')

    # E0 = 20.35
    if E0 is None:
        E0 = input('Zero energy in GeV? ')
    theta = 6e-3

    Lmag   = 2*4.889500000E-01
    Ldrift = 8.792573 + 0.8198
    # out  = np.zeros(y.shape[0])
    # for i, yval in enumerate(y):
    #     args=np.array([yval, ypinch, res, E0, theta, Ldrift, Lmag, etay, etapy])
    #     outval=spopt.minimize(merit_fcn, x0=np.array([20]), args=args)
    #     out[i]=outval.x[0]
    #
    out = E_no_eta(y, ypinch, res, Ldrift, Lmag, E0, theta)
    return out

# def merit_fcn(E, ypx, ypinch, res, E0, theta, Ldrift, Lmag, eta0=np.float64(0), etap0=np.float64(0)):
#     E=E[0]
#     yoffset=yanalytic(E0, E0, theta, Ldrift, Lmag, eta0, etap0) - ypinch*res
#     y = ypx*res + yoffset
#     yana = yanalytic(E, E0, theta, Ldrift, Lmag, eta0, etap0)
#
#     # print('=====================')
#     # print(E)
#     # print(y)
#     # print(yana)
#     # print(np.power(y-yana, 2)*1e14)
#     # print('=====================')
#     return np.power(y-yana, 2)*1e14


def yanalytic(E, E0, theta, Ldrift, Lmag, eta0, etap0):
    logger.critical('hello')
    return y_no_eta(E, E0, theta, Ldrift, Lmag) + (E/E0 - 1)*(eta0+etap0*(Ldrift+Lmag))


def y_no_eta(E, E0, theta, Ldrift, Lmag):
    logger.critical('intermediate')
    output = Ldrift/np.sqrt(np.power(E/(E0*np.sin(theta)), 2)-1) + (E*Lmag)/(E0*np.sin(theta)) * (1 - np.sqrt(1-np.power(E0*np.sin(theta)/E, 2)))
    logger.critical('{}'.format(output))
    return output


# def my_E_no_eta(y, E0, theta, Ldrift, Lmag):

def E_no_eta(ypx, ypinch, res, Ldrift, Lmag, E0, theta, dataset_num=None):
    # Determine pinch location
    #  ypinch = y_pinch_calibrated + y_motor_calibrated/y_pixel_size
    #  E0 = 23.737805394397343771
    E0 = 20.35

    eta_0_meters = None
    if dataset_num == 13437 or dataset_num == 13438:
        y0    = np.float64(1589)    # pixel position of E0 (20.35 GeV).
        eta_0 = np.float64(949.72)  # nominal dipole dispersion in pixel, corresponding to 59.5 mm.
        
    elif dataset_num == 13448 or dataset_num == 13449:
        y0    = np.float64(1605.5) - np.float64(0.7923)*(E0+QS)  # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float64(949.72) + np.float64(0.7923)*(E0+QS)  # added QS dispersion of 0.7923 pix per QS GeV.
        #  eta_0 = np.float64(59.5e-3) + np.float64(0.7923)*(E0+QS)
            
    elif dataset_num == 13450:
        y0    = np.float64(1655)   - np.float64(3.321)*(E0+QS)  # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float64(949.72) + np.float64(3.321)*(E0+QS)  # added QS dispersion of 3.321 pix per QS GeV.
        
    elif dataset_num == 13537:
        y0    = np.float64(1576)   + np.float(0.5193)*(20.35+QS)  # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float64(949.72) - np.float(0.5193)*(20.35+QS)  # added QS dispersion of -0.5193 pix per QS GeV.
    else:
        y0   = np.float64(1589)
        eta_0_meters = (Ldrift+Lmag/np.float64(2))*theta

    # ===========================
    # Sebastien's code
    # ===========================
    z_B5D36    = np.float64(2005.65085 )  # middle of dipole magnet
    z_ELANEX   = np.float64(2015.22    )  # linac z location of ELANEX phosphor screen in meter
    z_CFAR     = np.float64(2016.04    )  # linac z location of Cherenkov Far gap in meter
    cal_ELANEX = np.float64(8.9185     )  # ELANEX camera calibration in um/pixel
    cal_CFAR   = np.float64(62.65      )  # CMOS FAR camera calibration in um/pixel
    # y0 = 259 (when QS=0) at ELANEX corresponds to y0 = 1589 on CMOS FAR.
    y0    = np.float64(259) + (cal_CFAR/cal_ELANEX) * (y0-np.float64(1589))
    ypinch = y0

    # ===========================
    # vvv Moved Code
    # ===========================

    yoffset = yanalytic(E0, E0, theta, Ldrift, Lmag, eta0=0, etap0=0) - ypinch*res

    y = ypx*res + yoffset

    if type(y) != np.ndarray:
        y = np.array([y])

    # ===========================
    # ^^^^ Moved Code
    # ===========================

    eta_0 = (cal_CFAR/cal_ELANEX) * (z_ELANEX-z_B5D36) / (z_CFAR-z_B5D36) * eta_0

    if eta_0_meters is None:
        eta_0_meters = eta_0*cal_CFAR*np.float64(1e-6)

    logger.debug('Dispersion is: {}'.format(eta_0_meters))

    approx = E0*eta_0_meters / y

    def merit(Eguess, yval):
        yfromE = y_no_eta(Eguess, E0, theta, Ldrift, Lmag)
        return np.power(yfromE-yval, 2)
    #  #
    results = np.zeros(y.size, dtype=np.float64)
    for i, yval in enumerate(y):
        guess      = E0*(np.float64(2)*Ldrift+Lmag)*theta / (np.float64(2)*yval)
        results[i] = spopt.fmin(merit, guess, args=(yval, ), disp=False)
    
    return results, approx
