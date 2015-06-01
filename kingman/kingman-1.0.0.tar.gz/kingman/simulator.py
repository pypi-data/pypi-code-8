#
# Copyright (C) 2015 Jerome Kelleher <jerome.kelleher@well.ox.ac.uk>
#
# This file is part of kingman.
#
# kingman is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kingman is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kingman.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Simulation code for the kingman module.
"""
from __future__ import print_function
from __future__ import division

import random


def simulate(sample_size, random_seed=None):
    """
    Simulates the Kingman coalescent for the specified sample size
    and random seed.

    Returns a tuple (parent, time) which describes the simulated
    history of the sample as an oriented forest. ``parent`` is a
    list of integers, in which the parent of node ``j`` is
    ``parent[j]``. ``time`` an array of floating point values
    in which the time at which node ``j`` was created is ``time[j]``. See
    `<http://jeromekelleher.github.io/ercs/#oriented-trees-and-forests>`_
    for further information on oriented forests.

    Time is measured in units of 4Ne generations,
    following Hudson's ms.

    :param sample_size: The sample size; must be >= 2.
    :param random_seed: The random seed for simulations
    :type sample_size: integer
    :type random_seed: integer or None
    :rtype: (list, list)
    """
    if sample_size < 2:
        raise ValueError("sample_size must be >= 2")
    random.seed(random_seed)
    time = [0 for j in range(2 * sample_size)]
    parent = [0 for j in range(2 * sample_size)]
    # Following Knuth, we make the zeroth element -1.
    time[0] = -1
    parent[0] = -1
    ancestors = list(range(1, sample_size + 1))
    t = 0
    next_node = sample_size + 1
    for n in range(sample_size, 1, -1):
        t += random.expovariate(n * (n - 1))
        for _ in range(2):
            child = random.choice(ancestors)
            parent[child] = next_node
            ancestors.remove(child)
        ancestors.append(next_node)
        time[next_node] = t
        next_node += 1
    return parent, time
