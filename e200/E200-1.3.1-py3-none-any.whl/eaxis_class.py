import E200
import scisalt as mt
import numpy as np

__all__ = ['Energy_Axis']

import logging
loggerlevel = logging.DEBUG
logger      = logging.getLogger(__name__)


class Energy_Axis(object):
    """Object that sets up energy function to compute energy axis"""
    # ===================================
    # Initialize class
    # ===================================
    def __init__(self, camname, hdf5_data, uid):
        """Initialize input parameters"""
        self.camname    = camname
        self._hdf5_data = hdf5_data
        self._uid       = uid
        self._reset_class()

    # ===================================
    # Reset hidden data
    # ===================================
    def _reset_class(self):
        """Resets hidden data in the class that all calculations are based off of"""
        self._dataset_num = None
        self._ypinch      = None
        self._setQS       = None

    def _get_hdf5_data(self):
        return self._hdf5_data

    def _set_hdf5_data(self, value):
        self._hdf5_data = value
        self._reset_class()
    hdf5_data = property(_get_hdf5_data, _set_hdf5_data)

    # ===================================
    # Get dataset number
    # ===================================
    def _get_dataset_num(self):
        """Get dataset number from first motor UID"""
        if self._dataset_num is None:
            dataset_num       = np.int64(self._hdf5_data['raw']['scalars']['XPS_LI20_DWFA_M5']['UID'].value[0][0])
            dataset_num       = str(dataset_num)
            dataset_num = dataset_num[0:5]
        return dataset_num
    dataset_num = property(_get_dataset_num)

    # ===================================
    # Get camera resolution
    # ===================================
    def _get_res(self):
        """Camera resolution"""
        imgstr = self._hdf5_data['raw']['images'][str(self.camname)]
        res    = np.float64(imgstr['RESOLUTION'][0, 0])
        res    = res*np.float64(1.0e-6)
        return res
    res = property(_get_res)

    # ===================================
    # Get ymotor for ELANEX from file
    # (not saved properly for all steps)
    # ===================================
    def _get_ymotor_orig(self):
        """Motor position from file"""
        #  if self.camname=='ELANEX':
        ymotor = hdf5_data['raw']['scalars']['XPS_LI20_DWFA_M5']['dat']
        ymotor = mt.derefdataset(ymotor, hdf5_data.file)
        ymotor = ymotor[0]*1e-3
        logger.log(level=loggerlevel, msg='Original ymotor is: {}'.format(ymotor))
        return ymotor
    ymotor_orig = property(_get_ymotor_orig)

    # ===================================
    # Get setQS equivalent
    # ===================================
    def _get_setQS(self):
        if self._setQS is None:
            '''Reconstruct quadrupole functions because motor values aren't recorded properly to file'''
            raw_rf     = self.hdf5_data['raw']
            scalars_rf = raw_rf['scalars']
            setQS_str  = scalars_rf['step_value']
            setQS_dat  = E200.E200_api_getdat(setQS_str, self._uid).dat[0]
            #  setQS_dat=0
            self._setQS      = mt.hardcode.setQS(setQS_dat)

            logger.log(level=loggerlevel, msg='Eaxis''s setQS is: {}'.format(setQS_dat))

        return self._setQS
    setQS = property(_get_setQS)

    # ===================================
    # Get ymotor from setQS
    # ===================================
    def _get_ymotor(self):
        ymotor = self.setQS.elanex_y_motor()*1e-3
        logger.log(level=loggerlevel, msg='Reconstructed ymotor is: {ymotor}'.format(ymotor=ymotor))
        return ymotor
    ymotor = property(_get_ymotor)

    # ===================================
    # Elements for calculating dispersion
    # ===================================
    _theta  = np.float64(6e-3)
    _Lmag   = np.float64(2*4.889500000E-01)

    # ===================================
    # Future-proofing, in case we want
    # to calculate dynamically
    # ===================================
    def _get_theta(self):
        return self._theta
    theta = property(_get_theta)

    def _get_Lmag(self):
        return self._Lmag
    Lmag = property(_get_Lmag)

    def _get_Ldrift(self):
        # Drift length depends on camera location
        if self.camname == 'ELANEX':
            self._Ldrift = np.float64(8.792573)
        elif self.camname == 'CMOS_FAR':
            self._Ldrift = np.float64(8.792573) + 0.8198

        return self._Ldrift
    Ldrift = property(_get_Ldrift)

    # ===================================
    # Set ypinch and eta0 to self
    # ===================================
    def _set_ypinch_eta0(self):
        """Set the ypinch and eta0 from dataset number"""
        # ===================================
        # Find and write eta_0, y_0
        # ===================================
        self.E0 = 20.35

        if self.dataset_num is None:
            logger.critical('No dataset_num detected')
            self._ypinch = np.float64(1589)
            self._eta0   = (self.Ldrift+self.Lmag/np.float64(2))*self.theta

        else:
            QS = self.setQS.energy_offset
            logger.debug('Energy offset: {}'.format(QS))

            logger.debug('Dataset_num: {}'.format(self.dataset_num))
            if self.dataset_num == '13437' or self.dataset_num == '13438':
                y0       = np.float64(1589)    # pixel position of E0 (20.35 GeV).
                eta_0_px = np.float64(949.72)  # nominal dipole dispersion in pixel, corresponding to 59.5 mm.

            elif self.dataset_num == '13448' or self.dataset_num == '13449':
                y0       = np.float64(1605.5) - np.float64(0.7923)*(self.E0+QS)  # y0 is adjusted to account for QS dispersion.
                eta_0_px = np.float64(949.72) + np.float64(0.7923)*(self.E0+QS)  # added QS dispersion of 0.7923 pix per QS GeV.

            elif self.dataset_num == '13450':
                y0       = np.float64(1655)   - np.float64(3.321)*(self.E0+QS)  # y0 is adjusted to account for QS dispersion.
                eta_0_px = np.float64(949.72) + np.float64(3.321)*(self.E0+QS)  # added QS dispersion of 3.321 pix per QS GeV.

            elif self.dataset_num == '13537':
                y0       = np.float64(1576)   + np.float(0.5193)*(20.35+QS)  # y0 is adjusted to account for QS dispersion.
                eta_0_px = np.float64(949.72) - np.float(0.5193)*(20.35+QS)  # added QS dispersion of -0.5193 pix per QS GeV.
            else:
                raise ValueError('Dataset number does not exist: {}'.format(self.dataset_num))

            if self.camname == 'ELANEX':
                # ===================================
                # Sebastien's code
                # ===================================
                z_B5D36    = np.float64(2005.65085 )  # middle of dipole magnet
                z_ELANEX   = np.float64(2015.22    )  # linac z location of ELANEX phosphor screen in meter
                z_CFAR     = np.float64(2016.04    )  # linac z location of Cherenkov Far gap in meter
                cal_ELANEX = np.float64(8.9185     )  # ELANEX camera calibration in um/pixel
                cal_CFAR   = np.float64(62.65      )  # CMOS FAR camera calibration in um/pixel

                # y0 = 259 (when QS=0) at ELANEX corresponds to y0 = 1589 on CMOS FAR.
                y0           = np.float64(259) + (cal_CFAR/cal_ELANEX) * (y0-np.float64(1589))
                self._ypinch = y0

                eta_0_px = (cal_CFAR/cal_ELANEX) * (z_ELANEX-z_B5D36) / (z_CFAR-z_B5D36) * eta_0_px

                self._eta0 = eta_0_px * cal_ELANEX * np.float64(1e-6)

            elif self.camname == 'CMOS_FAR':
                self._ypinch = y0
                self._eta0  = eta_0_px * cal_CFAR * np.float64(1e-6)
            else:
                raise ValueError('Camera name not valid: {}'.format(self.camname))

    def _get_ypinch(self):
        if self._ypinch is None:
            self._set_ypinch_eta0()
        return self._ypinch
    ypinch = property(_get_ypinch)

    def _get_eta0(self):
        self._set_ypinch_eta0()
        return self._eta0
    eta0 = property(_get_eta0)

    def energy(self, ypx):
        # ===================================
        # Assuming thin lens
        # ===================================
        if type(ypx) != np.ndarray:
            ypx = np.array([ypx])

        if self.camname == 'ELANEX':
            # For E0=20.35, ypx = 734-259 = 475, y = eta0 = 0.0548, ymotor = 0
            # This calibration comes from Sebastien and Erik
            y = (ypx)*self.res - self.ymotor + 0.050567428212613990412
        elif self.camname == 'CMOS_FAR':
            y = ypx*self.res
        else:
            raise NotImplemented('Camera not implemented: {}'.format(self.camname))

        logger.log(level=loggerlevel, msg='Eta0 is: {}'.format(self.eta0))

        approx = self.eta0*self.E0 / y
        return approx
