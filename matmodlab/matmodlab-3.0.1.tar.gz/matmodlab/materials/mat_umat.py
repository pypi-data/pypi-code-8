import sys
import logging
from matmodlab.materials.product import ABA_IO_F90, ABA_UMAT_PYF
from matmodlab.mmd.material import AbaqusMaterial, SET_AT_RUNTIME
from matmodlab.utils.errors import StopFortran

mat = None

class UMat(AbaqusMaterial):
    '''Constitutive model class for the umat model'''
    name = 'umat'
    aux_files = [ABA_IO_F90, ABA_UMAT_PYF]
    lapack = 'lite'

    def __init__(self):
        self.param_names = SET_AT_RUNTIME

    def import_model(self):
        global mat
        import matmodlab.lib.umat as mat

    def initialize_umat(self, statev, coords, noel, npt, layer, kspt):
        '''initialize the material state'''
        log = logging.getLogger('mps')
        mat.sdvini(statev, coords, noel, npt, layer, kspt, log.info, log.warn,
                   StopFortran)
        return statev

    def update_state_umat(self, stress, statev, ddsdde,
            sse, spd, scd, rpl, ddsddt, drplde, drpldt, stran, dstran,
            time, dtime, temp, dtemp, predef, dpred, cmname, ndi, nshr,
            nxtra, params, coords, drot, pnewdt, celent, dfgrd0,
            dfgrd1, noel, npt, layer, kspt, kstep, kinc):
        '''update the material state'''
        log = logging.getLogger('mps')
        mat.umat(stress, statev, ddsdde,
            sse, spd, scd, rpl, ddsddt, drplde, drpldt, stran, dstran,
            time, dtime, temp, dtemp, predef, dpred, cmname, ndi, nshr,
            nxtra, params, coords, drot, pnewdt, celent, dfgrd0,
            dfgrd1, noel, npt, layer, kspt, kstep, kinc, log.info, log.warn,
            StopFortran)
        return stress, statev, ddsdde
