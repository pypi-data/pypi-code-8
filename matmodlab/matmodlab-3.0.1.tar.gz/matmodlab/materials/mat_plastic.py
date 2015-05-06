import os
import logging
from femlib.constants import VOIGHT
from matmodlab.mmd.product import MAT_D
from matmodlab.mmd.material import MaterialModel
from matmodlab.utils.errors import MatModLabError, StopFortran

d = os.path.join(MAT_D, "src")
f1 = os.path.join(d, "plastic.f90")
f2 = os.path.join(d, "plastic.pyf")

class Plastic(MaterialModel):
    name = "plastic"
    source_files = [f1, f2]

    def __init__(self):
        self.param_names = ["K", "G", "A1", "A4"]
        self.prop_names = ["K", "G", "DPA", "DPB"]

    def setup(self):
        """Set up the Plastic material

        """
        global mat
        try:
            import matmodlab.lib.plastic as mat
        except ImportError:
            raise MatModLabError("model plastic not imported")
        log = logging.getLogger('mps')
        mat.plastic_check(self.params, log.info, log.warn, StopFortran)

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
        d = d / VOIGHT
        log = logging.getLogger('mps')
        mat.plastic_update_state(dtime, self.params, d, stress,
                                 log.info, log.warn, StopFortran)
        return stress, xtra, None
