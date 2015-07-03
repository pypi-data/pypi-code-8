import numpy as _np
# import ipdb
from . import const as ct


def _set_if_none(self, mainkwargs, params):
    for name, default in params.items():
        try:
            value = mainkwargs.get(name, default)
            setattr(self, name, value)
        except KeyError:
            raise
            # print('Key doesn''t exist')


# ===============================
# Beam Positioning
# ===============================
class BeamPositioning(object):
    # beam centered in x & y
    # beam toward front of box in z
    def _C_x_y(self, box, plasma, bunches, off, magic):
        box_xy = box.box_xy(
            plasma = plasma,
            bunches = bunches,
            magic = magic
            )
        C = 0.5 * box_xy + off  # um
        return C

    def C_x(self, box, plasma, bunches, bunch, magic):
        return self._C_x_y(
            box=box,
            plasma=plasma,
            bunches=bunches,
            magic=magic,
            off=bunch.off_x
            )

    def C_y(self, box, plasma, bunches, bunch, magic):
        return self._C_x_y(
            box=box,
            plasma=plasma,
            bunches=bunches,
            magic=magic,
            off=bunch.off_y
            )

    def C_z(self, bunches, bunch):
        C_z = 4.0 * bunches[0].sig_z + bunch.off_z  # um
        return C_z


# ===============================
# Phase Space Sampling:
# Sizes & Resolution
# ===============================
class PhaseSpaceSampling(object):
    def __init__(self,
            # Beam Phase Space
            samp_beam_pha_N = int(pow(2, 17)),   # particles

            # Plasma Phase Space
            samp_plas_pha_N = int(pow(2, 17)),   # particles

            # Beam Centroid Resolution
            beam_cent_res_dz = int(pow(2, 6))    # z-slices
            ):
        self.samp_beam_pha_N = samp_beam_pha_N
        self.samp_plas_pha_N = samp_plas_pha_N
        self.beam_cent_res_dz = beam_cent_res_dz

    # beam phase space sampling particle count
    @property
    def ind_beam_pha(self):
        ind_beam_pha = int(round(_np.log2(self.samp_beam_pha_N)))
        return ind_beam_pha

    def NP_beam_pha(self, box, plasma, bunches, magic):
        ind_xy = box.ind_xy(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)
        ind_z = box.ind_z(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)
        NP_beam_pha = int(pow(2, 2 * ind_xy + ind_z - self.ind_beam_pha))
        return NP_beam_pha

    # plasma phase space sampling particle count
    @property
    def ind_plas_pha(self):
        ind_plas_pha = int(round(_np.log2(self.samp_plas_pha_N)))
        return ind_plas_pha

    def NP_plas_pha(self, box, plasma, bunches, magic):
        ind_xy = box.ind_xy(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)
        ind_z = box.ind_z(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)
        NP_plas_pha = int(pow(2, 2 * ind_xy + ind_z - self.ind_plas_pha))
        return NP_plas_pha


# ===============================
# "Magic" Simulation Factors
# ===============================
class MagicSettings(object):
    def __init__(self,
            box_xy_fact = 1.0            ,  # should be ~1-2
            box_z_fact  = 1.0            ,  # should be ~1-2
            d_grid_fact = 0.05           ,  # exact
            NP_xy_fact  = -1             ,  # exact
            np_min      = 4              ,  # exact
            DT_fact     = (2. / 3.) / 10.   # exact
            ):
        self.box_xy_fact = box_xy_fact
        self.box_z_fact  = box_z_fact
        self.d_grid_fact = d_grid_fact
        self.NP_xy_fact  = NP_xy_fact
        self.np_min      = np_min
        self.DT_fact     = DT_fact
    

# ===============================
# Simulation area settings
# ===============================
class BoxSettings(object):
    # ===============================
    # Box Dimensions
    # ===============================
    # simulation box length
    # default: 2.5 x L_bubble or
    #          6.0 x sig_z
    # set to '0' for automatic setting

    # simulation box height/width
    # default: 4.0 x R_bubble or
    #          5.0 x sig_x/y
    # set to '0' for automatic setting
    def __init__(self,
            box_width  = None,
            box_height = None,
            box_length = None,
            NP_dynamic = False
            ):
        self.box_width  = box_width
        self.box_height = box_height
        self.box_length = box_length
        self.NP_dynamic = NP_dynamic

    # ===============================
    # Box Size and Particle Densities
    # ===============================
    def box_xy(self, plasma, bunches, magic):
        # box size in x and y:
        # use specified size if given
        if self.box_width is not None:
            box_xy = int(round(self.box_width / 5.) * 5)      # um
        # otherwise use default value
        else:
            max_sig = 0
            for bunch in bunches:
                max_sig = max(
                    max_sig,
                    bunch.sig_x0(plasma),
                    bunch.sig_y0(plasma))

            box_xy = int(round(
                magic.box_xy_fact * max(4.0 * plasma.R_bub(bunches[0]),
                    7.0 * max_sig)
                    / 5.) * 5)                         # um
        # ensure box_xy is odd:
        if not(box_xy % 2):
            box_xy += 1

        return box_xy

    def box_z(self, bunches, plasma, magic):
        # box size in z
        # use specified size if given
        if self.box_length is not None:
            box_z = int(round(self.box_length / 5.) * 5)      # um
        # otherwise use default value
        else:
            max_sig_z = 0
            for bunch in bunches:
                max_sig_z = max(max_sig_z, bunch.sig_z)

            box_z = int(round(
                magic.box_z_fact * max(2.5 * plasma.L_bub,
                    6.0 * max_sig_z)
                    / 5.) * 5)                          # um
        # ensure box_z is odd:
        if not(box_z % 2):
            box_z  += 1

        return box_z

    def d_grid(self, magic, plasma):
        # grid spacing
        d_grid   = magic.d_grid_fact * plasma.cwp * ct.cm2um             # um
        return d_grid

    def ind_xy(self, plasma, bunches, magic):
        # number of cells (power of 2)
        ind_xy   = int(
            max(
                round(
                    _np.log2(
                        self.box_xy(
                            plasma  = plasma,
                            bunches = bunches,
                            magic   = magic)
                        / self.d_grid(
                            plasma = plasma,
                            magic = magic)
                        )
                    ),
                6)
            )

        # limit number of cells in each dimension
        if (ind_xy > 9):
            ind_xy = 9

        return ind_xy

    def ind_z(self, plasma, bunches, magic):
        ind_z    = int(
            max(
                round(
                    _np.log2(
                        self.box_z(
                            plasma  = plasma,
                            bunches = bunches,
                            magic   = magic)
                        / self.d_grid(
                            plasma  = plasma,
                            magic   = magic)
                        )
                    ),
                6)
            )

        # limit number of cells in each dimension
        if (ind_z > 8):
            ind_z = 8

        # ensure ind_z > ind_xy
        ind_xy = self.ind_xy(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)

        if (ind_z <= ind_xy):
            ind_z = int(ind_xy + 1)

        return ind_z

    def N_cell(self, plasma, bunches, magic):
        ind_xy = self.ind_xy(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)
        ind_z = self.ind_z(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)

        N_cell   = int(pow(2, ind_xy + ind_xy + ind_z))
        return N_cell

    def V_box(self, plasma, bunches, magic):
        box_xy = self.box_xy(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)
        box_z = self.box_z(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)

        # box volume
        V_box    = box_xy * box_xy * box_z  # um^3
        return V_box

    def NP_xy(self, plasma, bunches, magic):
        if self.NP_dynamic:
            ind_xy = self.ind_xy(
                plasma  = plasma,
                bunches = bunches,
                magic   = magic)

            # dynamically assigned values->
            NP_xy    = int(pow(2, ind_xy + magic.NP_xy_fact))
        else:
            # beam particle density (power of 2)
            # default "safe" values->
            NP_xy    = int(pow(2, 8))

        return NP_xy

    def NP_z(self, plasma, bunches, magic):
        if self.NP_dynamic:
            ind_z = self.ind_z(
                plasma  = plasma,
                bunches = bunches,
                magic   = magic)

            # dynamically assigned values->
            NP_z     = int(pow(2, ind_z))
        else:
            # beam particle density (power of 2)
            # default "safe" values->
            NP_z     = int(pow(2, 7))

        return NP_z

    def NP2(self, plasma, bunches, magic):
        ind_xy = self.ind_xy(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)
        # plasma particle density (power of 2)
        NP2      = round(_np.sqrt(pow(pow(2, ind_xy), 2) * max(plasma.np_cell, magic.np_min)))
        return NP2


# ===============================
# Plasma parameters
# ===============================
class PlasmaSettings(object):
    def __init__(self,
            bunches,
            magic,
            qpic,
            np         = 3.0e16,  # cm^-3
            np_cell   = 4,       # per cell
            preformed = True,    # boolean
            # plasma spiecies atomic number
            # Note: only used if plasma is
            # not pre-formed
            # --------
            # H : 1
            # Li: 3
            # He: 2
            # Ar: 18
            # Cs: 55
            # --------
            plasma_z          = 1,
            # maximum ionization level
            max_ion_lv        = 1,
            # --------
            # transverse plasma geometry
            # --------
            #  'flat'  : constant density
            #  'gauss' : gaussian ramps
            #  'circle': circular filament
            # --------
            plasma_trans_geom = 'flat',
            ramp_dir          = 1,
            ramp_width        = 80,  # um
            plas_radius       = 80,   # um
            # --------
            # longitudinal plasma geometry
            # --------
            #  'flat'  : constant density
            #  'gauss' : gaussian ramps
            # --------
            plasma_long_geom  = 'gauss',
            # --------
            # longitudinal plasma params
            # for gaussian ramps
            # --------
            # upramp length (sigma)
            upramp_sig  = 15.0E4,  # um
            # flat-top start
            flat_start  = 30.0E4,  # um
            # flat-top end
            flat_end    = 60.0E4,  # um
            # downramp length (sigma)
            dnramp_sig  = 15.0E4   # um
            ):
        self.np          = np
        self.np_cell     = np_cell
        self.preformed   = preformed
        self.plasma_z    = 1
        self.max_ion_lv  = 1
        self.ramp_dir    = ramp_dir
        self.ramp_width  = ramp_width
        self.plas_radius = plas_radius

        self.set_plasma_trans_geom(
            plasma_trans_geom = plasma_trans_geom,
            qpic              = qpic)

        self.upramp_sig = upramp_sig,
        self.flat_start = flat_start,
        self.flat_end   = flat_end,
        self.dnramp_sig = dnramp_sig,

        self.set_plasma_long_geom(plasma_long_geom, bunches, magic, qpic)

    @property
    def wp(self):
        # plasma frequency
        wp     = (5.64E4) * _np.sqrt(self.np)  # rad/s
        return wp
    
    @property
    def cwp(self):
        # characteristic length
        cwp    = ct.c / self.wp  # cm
        return cwp

    @property
    def kp(self):
        # wavenumber
        kp     = 1.0 / self.cwp  # 1/cm
        return kp

    def R_bub(self, drive_bunch):
        # max bubble radius
        R_bub    = 2.58 * _np.sqrt((drive_bunch.Lambda / (ct.qe * ct.c)) * (1 / self.np)) * ct.cm2um  # um
        return R_bub

    @property
    def L_bub(self):
        # bubble length
        L_bub    = 2 * ct.pi * self.cwp * ct.cm2um      # um
        return L_bub

    @property
    def r_sheath(self, drive_bunch):
        # outer radius of bubble sheath
        r_sheath = 1.287 * self.R_bub(drive_bunch)         # um
        return r_sheath

    # -------------------
    # Plasma Species
    # -------------------
    @property
    def N_PREFORMED(self):
        if self.preformed:
            N_PREFORMED = int(1)
        else:
            N_PREFORMED = int(0)
        return N_PREFORMED

    @property
    def N_NEUTRAL(self):
        if self.preformed:
            N_NEUTRAL   = int(0)
        else:
            N_NEUTRAL   = int(1)
        return N_NEUTRAL

    # plasma species only used
    # if plasma is not preformed
    @property
    def Z_PLAS(self):
        Z_PLAS  = int(self.plasma_z)
        return Z_PLAS

    @property
    def MAX_ION(self):
        MAX_ION = int(self.max_ion_lv)
        return MAX_ION
    
    @property
    def plasma_trans_geom(self):
        return self._plasma_trans_geom

    def set_plasma_trans_geom(self, plasma_trans_geom, qpic):
        self._plasma_trans_geom = plasma_trans_geom
        # -------------------
        # Plasma Geometry
        # -------------------
        # initialize transverse plasma parameters
        self._plas_p1 = 1
        self._plas_p2 = 1
        self._plas_p3 = 1
        # set transverse profile code
        # --------
        #  0: flat
        #  3: gaussian ramp
        # 19: circle
        # 21: piecewise (custom)
        # --------
        # flat transverse profile:
        # np(r) = np0
        if plasma_trans_geom == 'flat':
            self._plas_prof = int(0)
        # gaussian transverse  profile:
        # np(r) = np0(1+p1*_np.exp(-((r-p2)/p3)^2))
        # p1: height of peak w.r.t. np0
        # p2: offset of peak
        # p3: _np.sqrt(2)*sig
        elif plasma_trans_geom == 'gauss':
            self._plas_prof = int(3)
            self._plas_p1   = -1 * self.ramp_dir
            self._plas_p2   = ((1 - self.ramp_dir) / 2) * qpic.L_sim
            self._plas_p3   = 2 * pow(self.ramp_width, 2)
        # circular filament:
        # np(r) = np0*p2(r > p1) or 0(r < p1)
        elif plasma_trans_geom == 'circle':
            self._plas_prof = int(19)
            self._plas_p1 = self.plas_radius
            self._plas_p2 = 1.0

    @property
    def plas_prof(self):
        return self._plas_prof

    @property
    def plas_p1(self):
        return self._plas_p1

    @property
    def plas_p2(self):
        return self._plas_p2

    @property
    def plas_p3(self):
        return self._plas_p3
    
    @property
    def plasma_long_geom(self):
        return self._plasma_long_geom

    def set_plasma_long_geom(self, plasma_long_geom, bunches, magic, qpic):
        self._plasma_long_geom = plasma_long_geom
        # longitudinal density profile
        # --------
        # initialize longitudinal density parameters
        self._z_max   = 1
        self._z_nstep = int(1)
        self._z_step  = [0]
        self._z_prof  = [0]

        # --------
        # define gaussian ramp function
        def gaussramps(A, z1, sig1, z2, sig2, z):
            return A * (
                (z < z1) * _np.exp(-_np.power(z - z1, 2) / (2 * _np.power(sig1, 2))) +
                (z >= z1) * (z <= z2) +
                (z > z2) * _np.exp(-_np.power(z - z2, 2) / (2 * _np.power(sig2, 2))))
        # --------
        # flat longitudinal profile
        if (plasma_long_geom == 'flat'):
            self._dense_var = "false"
        # gaussian ramps profile
        elif (plasma_long_geom == 'gauss'):
            TEND = qpic.TEND(bunches[0], self, magic)
            DT = qpic.DT(bunches[0], magic)
            self._dense_var = "true"
            self._z_max   = TEND * self.cwp * ct.cm2um  # um
            self._z_nstep = int(min(100, _np.floor(TEND / DT)))
            self._z_step  = _np.linspace(0, self._z_max, self._z_nstep)  # um
            self._z_prof  = gaussramps(1, self.flat_start, self.upramp_sig,
                      self.flat_end, self.dnramp_sig, self._z_step)  # np

    @property
    def dense_var(self):
        return self._dense_var

    @property
    def z_max(self):
        return self._z_max

    @property
    def z_nstep(self):
        return self._z_nstep

    @property
    def z_step(self):
        return self._z_step

    @property
    def z_prof(self):
        return self._z_prof


# ===============================
# QuickPIC settings (dumps, etc.)
# ===============================
class QuickPICSettings(object):
    def __init__(self,
            restart      = False,
            dump_restart = True,
            RST_START    = 1200,
            DRST_STEP    = 100,
            TOT_PROC     = 128,
            verbose      = False,
            is_multistep = True,
            L_sim        = 35.0,    # cm
            # -------------------
            # Simulation Output Parameters
            # -------------------
            # 3-D sampling?
            # Warning: Can drastically
            # increase simulation time.
            # -------------------
            # E-field
            samp_E_3D    = False,  # boolean
            # B-field
            samp_B_3D    = False,  # boolean
            # Beam
            samp_beam_3D = False,  # boolean
            # Plasma
            samp_plas_3D = False,  # boolean
            # -------------------
            # Sampling Plane(s)
            # x0: x=0, y-z plane
            # y0: y=0, x-z plane
            # z0: z=0, x-y plane
            # -------------------
            # E-field
            samp_E_x0     = True,  # boolean
            samp_E_y0     = True,  # boolean
            samp_E_z0     = False,  # boolean
            # B-field
            samp_B_x0     = True,  # boolean
            samp_B_y0     = True,  # boolean
            samp_B_z0     = False,  # boolean
            # Beam
            samp_beam_x0  = True,  # boolean
            samp_beam_y0  = True,  # boolean
            samp_beam_z0  = False,  # boolean
            # Plasma
            samp_plas_x0  = True,  # boolean
            samp_plas_y0  = True,  # boolean
            samp_plas_z0  = False,  # boolean
            # Beam Phase Space
            samp_beam_pha = True,  # boolean
            # Plasma Phase Space
            samp_plas_pha = False,  # boolean
            # -------------------
            # Sampling Periods in Time
            # (in units of sim. timestep)
            # -------------------
            # E-field
            samp_E_dt        = 20,   # dt (int)
            # B-field
            samp_B_dt        = 20,   # dt (int)
            # Beam
            samp_beam_dt     = 20,   # dt (int)
            # Plasma
            samp_plas_dt     = 20,   # dt (int)
            # Beam Phase Space
            samp_beam_pha_dt = 20,   # dt (int)
            # Plasma Phase Space
            samp_plas_pha_dt = 20,   # dt (int)
            # -------------------
            # Phase Space Sampling Sizes & Resolution
            # -------------------
            # Beam Phase Space
            samp_beam_pha_N = int(pow(2, 17)),   # particles
            # Plasma Phase Space
            samp_plas_pha_N = int(pow(2, 17)),   # particles
            # Beam Centroid Resolution
            beam_cent_res_dz = int(pow(2, 6))    # z-slices
            ):
        # read the restart file
        # if this is a restart run
        self.restart = restart
        self.dump_restart = dump_restart

        self.RST_START = RST_START
        self.DRST_STEP = DRST_STEP
        self.TOT_PROC  = TOT_PROC
        
        self.VERBOSE = _np.int(verbose)

        self.is_multistep     = is_multistep

        self.L_sim            = L_sim

        self.samp_E_3D        = samp_E_3D
        self.samp_B_3D        = samp_B_3D
        self.samp_beam_3D     = samp_beam_3D
        self.samp_plas_3D     = samp_plas_3D
        self.samp_E_x0        = samp_E_x0
        self.samp_E_y0        = samp_E_y0
        self.samp_E_z0        = samp_E_z0
        self.samp_B_x0        = samp_B_x0
        self.samp_B_y0        = samp_B_y0
        self.samp_B_z0        = samp_B_z0
        self.samp_beam_x0     = samp_beam_x0
        self.samp_beam_y0     = samp_beam_y0
        self.samp_beam_z0     = samp_beam_z0
        self.samp_plas_x0     = samp_plas_x0
        self.samp_plas_y0     = samp_plas_y0
        self.samp_plas_z0     = samp_plas_z0
        self.samp_beam_pha    = samp_beam_pha
        self.samp_plas_pha    = samp_plas_pha
        self.samp_E_dt        = samp_E_dt
        self.samp_B_dt        = samp_B_dt
        self.samp_beam_dt     = samp_beam_dt
        self.samp_plas_dt     = samp_plas_dt
        self.samp_beam_pha_dt = samp_beam_pha_dt
        self.samp_plas_pha_dt = samp_plas_pha_dt
        self.samp_beam_pha_N  = samp_beam_pha_N
        self.samp_plas_pha_N  = samp_plas_pha_N
        self.beam_cent_res_dz = beam_cent_res_dz

    @property
    def READ_RST(self):
        if self.restart:
            READ_RST = "true"
        else:
            READ_RST = "false"
        return READ_RST

    @property
    def DUMP_RST(self):
        # dump restart files
        if self.dump_restart:
            DUMP_RST = "true"
        else:
            DUMP_RST = "false"
        return DUMP_RST

    # -------------------
    # Beam Evolution
    # -------------------
    @property
    def BEAM_EVO(self):
        if self.is_multistep:
            BEAM_EVO = "true"
        else:
            BEAM_EVO = "false"
        return BEAM_EVO

    # -------------------
    # Simulation Time Scales
    # -------------------
    def DT(self, drive_bunch, magic):
        # time step size
        DT = round(magic.DT_fact * _np.sqrt(2. * drive_bunch.gamma))  # 1/wp
        return DT
    
    # total simulation time
    def TEND(self, drive_bunch, plasma, magic):
        if self.is_multistep:
            TEND = _np.floor(self.L_sim / plasma.cwp)  # 1/wp
        else:
            TEND = 1.01 * self.DT(
                drive_bunch = drive_bunch,
                magic       = magic
                )  # 1/wp
        return TEND

    # -------------------
    # Simulation Output Parameters
    # -------------------
    # 3-D Sampling
    # -------------------

    # 3-D E-field sampling?
    @property
    def E3D(self):
        if self.samp_E_3D:
            E3D  = int(1)  # 1:true
        else:
            E3D  = int(0)  # 0:false
        return E3D

    # 3-D B-field sampling?
    @property
    def B3D(self):
        if self.samp_B_3D:
            B3D  = int(1)  # 1:true
        else:
            B3D  = int(0)  # 0:false
        return B3D

    # 3-D Beam sampling?
    @property
    def QEB3D(self):
        if self.samp_beam_3D:
            QEB3D = int(1)  # 1:true
        else:
            QEB3D = int(0)  # 0:false
        return QEB3D

    # 3-D Plasma sampling?
    @property
    def QEP3D(self):
        if self.samp_plas_3D:
            QEP3D = int(1)  # 1:true
        else:
            QEP3D = int(0)  # 0:false
        return QEP3D

    # -------------------
    # Phase Space Sampling
    # -------------------
    # Beam Phase Space Sampling?
    @property
    def DUMP_PHA_BEAM(self):
        if self.samp_beam_pha:
            DUMP_PHA_BEAM = "true"
        else:
            DUMP_PHA_BEAM = "false"
        return DUMP_PHA_BEAM

    # Plasma Phase Space Sampling?
    @property
    def DUMP_PHA_PLASMA(self):
        if self.samp_plas_pha:
            DUMP_PHA_PLASMA = "true"
        else:
            DUMP_PHA_PLASMA = "false"
        return DUMP_PHA_PLASMA

    # -------------------
    # Sampling Plane(s)
    # -------------------

    # E-field sampling plane(s)
    def EX0(self, box, plasma, bunches, magic):
        if self.samp_E_x0:
            box_xy = box.box_xy(plasma=plasma, bunches=bunches, magic=magic)
            EX0  = box_xy / 2.  # um
        else:
            EX0  = 0.         # none
        return EX0

    def EY0(self, box, plasma, bunches, magic):
        if self.samp_E_y0:
            box_xy = box.box_xy(plasma=plasma, bunches=bunches, magic=magic)
            EY0  = box_xy / 2.  # um
        else:
            EY0  = 0.         # none
        return EY0

    def EZ0(self, box, plasma, bunches, magic):
        if self.samp_E_z0:
            box_z = box.box_z(plasma=plasma, bunches=bunches, magic=magic)
            EZ0  = box_z / 2.   # um
        else:
            EZ0  = 0.         # none
        return EZ0
    # B-field sampling plane(s)

    def BX0(self, box, plasma, bunches, magic):
        if self.samp_B_x0:
            box_xy = box.box_xy(plasma=plasma, bunches=bunches, magic=magic)
            BX0  = box_xy / 2.  # um
        else:
            BX0  = 0.         # none
        return BX0

    def BY0(self, box, plasma, bunches, magic):
        if self.samp_B_y0:
            box_xy = box.box_xy(plasma=plasma, bunches=bunches, magic=magic)
            BY0  = box_xy / 2.  # um
        else:
            BY0  = 0.         # none
        return BY0

    def BZ0(self, box, plasma, bunches, magic):
        if self.samp_B_z0:
            box_z = box.box_z(plasma=plasma, bunches=bunches, magic=magic)
            BZ0  = box_z / 2.   # um
        else:
            BZ0  = 0.         # none
        return BZ0
    # Beam sampling plane(s)

    def QEBX0(self, box, plasma, bunches, magic):
        if self.samp_beam_x0:
            box_xy = box.box_xy(plasma=plasma, bunches=bunches, magic=magic)
            QEBX0 = box_xy / 2.  # um
        else:
            QEBX0 = 0.        # none
        return QEBX0

    def QEBY0(self, box, plasma, bunches, magic):
        if self.samp_beam_y0:
            box_xy = box.box_xy(plasma=plasma, bunches=bunches, magic=magic)
            QEBY0 = box_xy / 2.  # um
        else:
            QEBY0 = 0.        # none
        return QEBY0

    def QEBZ0(self, box, plasma, bunches, magic):
        if self.samp_beam_z0:
            box_z = box.box_z(plasma=plasma, bunches=bunches, magic=magic)
            QEBZ0 = box_z / 2.  # um
        else:
            QEBZ0 = 0.        # none
        return QEBZ0

    # Plasma sampling plane(s)
    def QEPX0(self, box, plasma, bunches, magic):
        if self.samp_plas_x0:
            box_xy = box.box_xy(plasma=plasma, bunches=bunches, magic=magic)
            QEPX0 = box_xy / 2.  # um
        else:
            QEPX0 = 0.        # none
        return QEPX0

    def QEPY0(self, box, plasma, bunches, magic):
        if self.samp_plas_y0:
            box_xy = box.box_xy(plasma=plasma, bunches=bunches, magic=magic)
            QEPY0 = box_xy / 2.  # um
        else:
            QEPY0 = 0.        # none
        return QEPY0

    def QEPZ0(self, box, plasma, bunches, magic):
        if self.samp_plas_z0:
            box_z = box.box_z(plasma=plasma, bunches=bunches, magic=magic)
            QEPZ0 = box_z / 2.  # um
        else:
            QEPZ0 = 0.        # none
        return QEPZ0

    # -------------------
    # Sampling Periods in Time
    # -------------------
    @property
    def DFE(self):
        if self.is_multistep:
            # E-field
            DFE      = int(self.samp_E_dt)    # DT
        else:
            # E-field
            DFE      = int(1)        # DT
        return DFE

    @property
    def DFB(self):
        if self.is_multistep:
            # B-field
            DFB      = int(self.samp_B_dt)    # DT
        else:
            DFB      = int(1)        # DT
            # Beam
        return DFB

    @property
    def DFQEB(self):
        if self.is_multistep:
            # Beam
            DFQEB    = int(self.samp_beam_dt)  # DT
        else:
            # Beam
            DFQEB    = int(1)        # DT
        return DFQEB

    @property
    def DFQEP(self):
        if self.is_multistep:
            # Plasma
            DFQEP    = int(self.samp_plas_dt)  # DT
        else:
            # Plasma
            DFQEP    = int(1)        # DT
        return DFQEP

    # Beam Phase Space
    @property
    def DFPHA_BEAM(self):
        if (self.samp_beam_pha):
            DFPHA_BEAM   = int(self.samp_beam_pha_dt)  # DT
        else:
            DFPHA_BEAM   = int(1)  # DT
        return DFPHA_BEAM

    @property
    def DFPHA_PLASMA(self):
        # Plasma Phase Space
        if (self.samp_plas_pha):
            DFPHA_PLASMA = int(self.samp_plas_pha_dt)  # DT
        else:
            DFPHA_PLASMA = int(1)  # DT
        return DFPHA_PLASMA
    
    # -------------------
    # Phase Space Sampling Sizes & Resolution
    # -------------------
    # Beam Phase Space
    def DSAMPLE_BEAM(self, plasma_phase_sampling, box, plasma, bunches, magic):
        return plasma_phase_sampling.NP_beam_pha(box, plasma, bunches, magic)  # particles

    # Plasma Phase Space
    def DSAMPLE_PLASMA(self, plasma_phase_sampling, box, plasma, bunches, magic):
        return plasma_phase_sampling.NP_plas_pha(box, plasma, bunches, magic)  # particles

    # Beam Centroid Resolution
    @property
    def BC_RES(self):
        return int(self.beam_cent_res_dz)  # z-slices
    
    # -------------------
    # Number of Simulation Stages
    # -------------------
    # check that total proc. < number of cells in z
    # if (TOT_PROC > pow(2, ind_z)):
    #    TOT_PROC = pow(2, ind_z)
    # number of proc. per stage
    def STAGE_PROC(self, box, plasma, bunches, magic):
        ind_xy = box.ind_xy(
            plasma  = plasma,
            bunches = bunches,
            magic   = magic)
        return max(pow(2, ind_xy - 3), 1)

    # number of stages = total proc./proc. per stage
    def N_STAGES(self, box, plasma, bunches, magic):
        N_STAGES = max(
            int(
                self.TOT_PROC /
                self.STAGE_PROC(
                    box     = box,
                    plasma  = plasma,
                    bunches = bunches,
                    magic   = magic
                    )
                ),
            1)
        return N_STAGES


# ===============================
# Bunch settings
# ===============================
class BunchSettings(object):
    def __init__(self, beamtype='drive', **kwargs
            ):
        if beamtype == 'drive':
            params = {
                # Relativistic gamma
                'gamma': 39823.87,

                # Auto-match spot size to plasma?
                'sig_x_matched': False            ,  # boolean
                'sig_y_matched': False            ,  # boolean
                'sig_x_matched': False            ,  # boolean

                # Auto-match emittance to plasma?
                'en_x_matched': False             ,  # boolean
                'en_y_matched': False             ,  # boolean

                # Bunch charge
                'Q': int(2.0e10)                  ,  # e

                # Bunch length
                'sig_x_unmatched': 30.0        ,  # um
                'sig_y_unmatched': 30.0        ,  # um
                'sig_z': 30.0                  ,  # um

                # Bunch normalized emittance
                'en_x_unmatched': 100.                      ,  # mm-mrad
                'en_y_unmatched': 10.                       ,  # mm-mrad

                # Bunch waist location from start
                'waist': 15.                      ,  # cm

                # Bunch energy spread
                # DOESN'T WORK                    , SET TO 0
                'dp': 0.00                        ,  # (unitless)
                # Bunch drift velocity
                'v_x': 0.                         ,  # c
                'v_y': 0.                         ,  # c
                'v_z': 0.                         ,  # c

                # Bunch transverse &
                # longitudinal offset
                'off_x': 0.                       ,  # um
                'off_y': 0.                       ,  # um
                'off_z': 0.                       ,  # um
                }
        elif beamtype == 'witness':
            params = {
                # Relativistic gamma
                'gamma': 1000                     ,  # (unitless)

                # Auto-match spot size to plasma?
                'sig_x_matched': False            ,  # boolean
                'sig_y_matched': False            ,  # boolean
                'sig_x_matched': False            ,  # boolean

                # Auto-match emittance to plasma?
                'en_x_matched': False             ,  # boolean
                'en_y_matched': False             ,  # boolean

                # Bunch charge
                'Q': int(1.0e9)                   ,  # e

                # Bunch length
                'sig_x_unmatched': 10.0                      ,  # um
                'sig_y_unmatched': 10.0                      ,  # um
                'sig_z': 10.0                      ,  # um

                # Bunch normalized emittance
                'en_x_unmatched': 1.                        ,  # mm-mrad
                'en_y_unmatched': 1.                        ,  # mm-mrad

                # Bunch waist location from start
                'waist': 15.0e-2                      ,  # cm

                # Bunch energy spread
                # DOESN'T WORK                    ,  SET TO 0
                'dp': 0.00                        ,  # (unitless)
                # Bunch drift velocity
                'v_x': 0.                         ,  # c
                'v_y': 0.                         ,  # c
                'v_z': 0.                         ,  # c

                # Bunch transverse &
                # longitudinal offset
                'off_x': 0.                       ,  # um
                'off_y': 0.                       ,  # um
                'off_z': 125.                     ,  # um
                }
        _set_if_none(self, mainkwargs=kwargs, params=params)

    @property
    def Lambda(self):
        # ========================
        # Calculated Peak Current
        # ========================
        # peak current of drive bunch
        Lambda = self.Q * ct.qe * ct.c / (_np.sqrt(2 * ct.pi) * self.sig_z * ct.um2cm)  # A
        return Lambda

    # ===============================
    # Auto-Matching to Plasma
    # ===============================
    def _sig(self, sig_matched, en, plasma, sig_unmatched):
        if sig_matched:
            sig = _np.sqrt(en * (ct.cm2um / plasma.kp) * _np.sqrt(2 / self.gamma))
        else:
            sig = sig_unmatched
        return sig

    def sig_x(self, plasma):
        return self._sig(
            sig_matched   = self.sig_x_matched,
            sig_unmatched = self.sig_x_unmatched,
            en            = self.en_x_unmatched,
            plasma        = plasma
            )

    def sig_y(self, plasma):
        return self._sig(
            sig_matched   = self.sig_y_matched,
            sig_unmatched = self.sig_y_unmatched,
            en            = self.en_y,
            plasma        = plasma
            )

    def _en(self, en_matched, en_unmatched, sig, plasma):
        if en_matched:
            en = pow(sig, 2.0) * (plasma.kp / ct.cm2um) * _np.sqrt(self.gamma / 2.0)
        else:
            en = en_unmatched
        return en

    def en_x(self, plasma):
        return self._en(
            en_matched   = self.en_x_matched,
            en_unmatched = self.en_x_unmatched,
            sig          = self.sig_x(plasma),
            plasma       = plasma
            )

    def en_y(self, plasma):
        return self._en(
            en_matched   = self.en_y_matched,
            en_unmatched = self.en_y_unmatched,
            sig          = self.sig_y(plasma),
            plasma       = plasma
            )

    # ===============================
    # Initial beam parameters
    # ===============================
    def _beta(self, sig, en):
        beta = pow(sig, 2.0) / en / self.gamma
        return beta

    def beta_x(self, plasma):
        return self._beta(
            sig = self.sig_x(plasma),
            en = self.en_x(plasma)
            )

    def beta_y(self, plasma):
        return self._beta(
            sig = self.sig_y(plasma),
            en = self.en_y(plasma)
            )

    def _beta_0(self, beta):
        beta_0 = beta + pow(self.waist, 2.0) / beta
        return beta_0

    def beta_x0(self, plasma):
        return self._beta_0(
            beta = self.beta_x(plasma)
            )

    def beta_y0(self, plasma):
        return self._beta_0(
            beta = self.beta_y(plasma)
            )

    def _alpha_0(self, beta):
        alpha_0 = self.waist / beta
        return alpha_0

    def alpha_x0(self, plasma):
        return self._alpha_0(
            beta = self.beta_x(plasma)
            )

    def alpha_y0(self, plasma):
        return self._alpha_0(
            beta = self.beta_y(plasma)
            )

    def _sig_0(self, en, beta):
        sig_0 = _np.sqrt(en * beta)
        return sig_0

    def sig_x0(self, plasma):
        return self._sig_0(
            en = self.en_x(plasma),
            beta = self.beta_x0(plasma)
            )

    def sig_y0(self, plasma):
        return self._sig_0(
            en = self.en_y(plasma),
            beta = self.beta_y0(plasma)
            )
