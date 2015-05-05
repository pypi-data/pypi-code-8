from os.path import join
from matmodlab.utils.fortran.product import DGPADM_F, FIO
from matmodlab.mmd.product import MAT_D
D = join(MAT_D, 'src')

# Auxiliary files
ABA_UANISOHYPER_JAC_F90 = join(D, 'uanisohyper_inv_jac.f90')
ABA_UHYPER_JAC_F90 = join(D, 'uhyper_jac.f90')
ABA_TENSALG_F90 = join(D, 'tensalg.f90')
ABA_IO_F90 = join(D, 'aba_io.f90')
ABA_SDVINI = join(D, 'sdvini.f90')

# Signature files
ABA_UANISOHYPER_PYF = join(D, 'uanisohyper_inv.pyf')
ABA_UHYPER_PYF = join(D, 'uhyper.pyf')
ABA_UMAT_PYF = join(D, 'umat.pyf')

ABA_MATS = ['umat', 'uhyper', 'uanisohyper_inv']


def fortran_libraries():
    libs = {}

    visco_f90 = join(D, 'visco.f90')
    visco_pyf = join(D, 'visco.pyf')
    libs['visco'] = {'source_files': [visco_f90, visco_pyf, FIO]}

    expansion_f90 = join(D, 'expansion.f90')
    expansion_pyf = join(D, 'expansion.pyf')
    libs['expansion'] = {'source_files': [expansion_f90, expansion_pyf],
                         'mmlabpack': True}

    return libs
