# -*- coding: utf-8 -*-
"""
settings.py
===========

"""
NAME_LABEL_DICT = {
    'phi': '$\phi_h$',
    'xN': '$\chi N$',
    'chiN': '$\chi N$',
}

PHASE_LIST = ['DIS', 'LAM', 'HEX',
              'Gyroid', 'O70',
              'BCC', 'FCC', 'A15', 'Sigma']
NA_PHASE = 'NA'  # to denote not available stable phase

SOLVER_LIST = ['POLYORDER', 'POLYFTS', 'PYDIAGRAM']

DIAGRAM_FILE = 'diagram.p'

INFO_MAP_FILE = 'info_map.p'

AF_MAP_FILE = 'aF_map.p'

BOUNDARY_FILE = 'boundary.p'

MARK_FILE = 'pydiagram.mark'

# DATA_FILE format
# Matlab MAT-file
# mat['F'] for free energy F
# mat['a'] for length of unit vector a of a unit cell
# mat['b'] for length of unit vector b of a unit cell
# mat['c'] for length of unit vector c of a unit cell
DATA_FILE = 'scft_out_cell.mat'

# LOG_FILE format
# Sample
#
# ********* Model_AB3_A Parameter List **********
# Compressibility: Incompressible model.
# Grid initialization: File
# SCFT initialization: Field
# Confinement: None
# MDE algorithm: ETDRK4
# SCFT algorithm: Anderson mixing
# Cell optimization algorithm: Brent method
# Contour integration algorithm: Simpson

# fA = 0.4    fB = 0.6    alpha = 0.5
# phiA = 0.4  phiB = 0.6
# chiN = 17.2
# aA = 1  aB = 1
# dsA = 0.01  dsB = 0.01  dshA = 0.01
# sA = 41 sB = 21 shA = 21
# seedA = 0   seedB = 0

# dimension: 3
# (Lx, Ly, Lz) = (32, 32, 32)
# (a, b, c) = (3.9, 3.9, 3.9)
# *******************************************

# 10
# t = 2.237
#     Unit Cell: Cubic
#     (lx,ly,lz) = 3.9000,3.9000,3.9000
#     H    = 4.080888 = 3.363803 + 0.717086
#     phicA = 0.4000  [0.1854, 0.9492]
#     phihA = 0.0000  [0.0000, 0.0000]
#     phiA = 0.4000   [0.1854, 0.9492]
#     phiB = 0.6000   [0.0513, 0.8144]
#     wA   = 10.9702  [3.2410, 15.2375]
#     wB   = 7.5301   [4.4153, 18.6805]
#     yita = 0.6501   [-0.6323, 2.4859]
#     Incompressibility = 1.12e-04
#     Qc = 3.05e-04   Qh = 1.38e-01
#     Residual Error    = 1.49e-04
LOG_FILE = 'log'

CELL_OPT_FIGURE = 'cell_opt'

CELL_SIZE_FIGURE = 'cell_size'

DIAGRAM_FIGURE = 'diagram'

TOL_CELL_SIZE = 1e-4  # tolerance for determining identical cell size

TOL_PHI = 1e-3  # tolerance for determining identical density value

TOL_F = 1e-5  # tolerance for determining identical free energy

# tolerance for stopping the SCFT/FTS simulations
# which is specified in polyorder/param.ini
# Compare it with the actual accuracy to determine whether a simulation
# is successful.
# The simulation is successful if accuracy <= C_STOP * TOL_STOP
TOL_STOP = 1e-6
C_STOP = 5.0

# tolerance for stopping the SCFT/FTS simulation using variable cell
TOL_STRESS = 1.0e-4
