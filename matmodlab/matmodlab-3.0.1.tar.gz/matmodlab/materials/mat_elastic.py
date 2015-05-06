import os
import sys
import logging
from matmodlab.mmd.product import MAT_D
from matmodlab.mmd.material import MaterialModel
from matmodlab.utils.errors import StopFortran
from femlib.constants import VOIGHT

mat = None

d = os.path.join(MAT_D, "src")
f1 = os.path.join(d, "elastic.f90")
f2 = os.path.join(d, "elastic.pyf")


class Elastic(MaterialModel):
    name = "elastic"
    source_files = [f1, f2]
    def __init__(self):
        self.param_names = ["K:BMOD", "G:SMOD:MU"]
        self.prop_names = ["K", "G"]

    def setup(self):
        """Set up the Elastic material

        """
        global mat
        try:
            import matmodlab.lib.elastic as mat
        except ImportError:
            raise ImportError('elastic model not imported')
        log = logging.getLogger('mps')
        mat.elastic_check(self.params, log.info, log.warn, StopFortran)

    def mimicking(self, mat_mimic):
        # reset the initial parameter array to represent this material
        iparray = np.zeros(2)
        iparray[0] = mat_mimic.completions["K"] or 0.
        iparray[1] = mat_mimic.completions["G"] or 0.
        if mat_mimic.completions["YT"]:
            logging.getLogger('mps').warn("{0} cannot mimic a strength limit, only "
                             "an elastic response will occur".format(self.name))
        return iparray

    def update_state(self, time, dtime, temp, dtemp, energy, rho, F0, F,
        stran, d, elec_field, stress, xtra, **kwargs):
        """Compute updated stress given strain increment

        Parameters
        ----------
        dtime : float
            Time step

        d : array_like
            Deformation rate

        stress : array_like
            Stress at beginning of step

        xtra : array_like
            Extra variables

        Returns
        -------
        S : array_like
            Updated stress

        xtra : array_like
            Updated extra variables

        """
        # model is written with strain components given as tensor strain,
        # matmodlab uses engineering shear strains
        d = d / VOIGHT
        log = logging.getLogger('mps')
        mat.elastic_update_state(dtime, self.params, d, stress,
                                 log.info, log.warn, StopFortran)
        return stress, xtra, self.constant_jacobian
