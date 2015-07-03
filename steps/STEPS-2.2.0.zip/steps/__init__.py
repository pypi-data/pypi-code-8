# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# STEPS - STochastic Engine for Pathway Simulation
# Copyright (C) 2007-2014 Okinawa Institute of Science and Technology, Japan.
# Copyright (C) 2003-2006 University of Antwerp, Belgium.
#
# See the file AUTHORS for details.
#
# This file is part of STEPS.
#
# STEPS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# STEPS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

__name__      = 'steps'
__longname__  = 'STochastic Engine for Pathway Simulation'
__version__   = '2.2.0'
__author__    = 'STEPS Development Team'
__url__       = 'steps.sourceforge.net'
__license__   = """
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# STEPS - STochastic Engine for Pathway Simulation                              #
# Copyright (C) 2007-2014 Okinawa Institute of Science and Technology, Japan.   #
# Copyright (C) 2003-2006 University of Antwerp, Belgium.                       #
#                                                                               #
# See the file AUTHORS for details.                                             #
#                                                                               #                             
# STEPS is free software: you can redistribute it and/or modify                 #
# it under the terms of the GNU General Public License as published by          #
# the Free Software Foundation, either version 3 of the License, or             #
# (at your option) any later version.                                           #
#                                                                               #
# STEPS is distributed in the hope that it will be useful,                      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                  #
# GNU General Public License for more details.                                  #
#                                                                               #
# You should have received a copy of the GNU General Public License             #
# along with this program. If not, see <http://www.gnu.org/licenses/>.          #
#                                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    """
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print ""
print ""
print "####################", __longname__, "#################"
print "                                Version: ", __version__
print __license__
print "                        ", __url__
print "#############################################################################"
print ""
print ""

try:
    import steps.model
    import steps.geom
    import steps.rng
    import steps.solver
    import steps.utilities

except:
    print "Unable to load STEPS modules."
else:
    print "The following STEPS Modules are loaded:\n"
    print "steps.model, steps.geom, steps.rng, steps.solver, steps.utilities"
print "#############################################################################"
print ""
print ""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# END
