#!/usr/bin/env python
"""
Calculates the dielectric constant of a fluid.
"""

import argparse

# system modules
import argparse
import math
import numpy as np

# custom modules
import f_core as fc
import output_tracker as ot

parser = argparse.ArgumentParser()
parser.add_argument('topology', type=str, help='The topology to work with.')
parser.add_argument('coordinates', type=str, help='The coordinates to work with.')
parser.add_argument('temperature', type=float, help='The simulation temperature.')

def magnetic_moments(universe, timestep, molecules):
	ms = np.zeros((len(molecules), 3))
	for i in range(len(molecules)):
		ms[i] = molecules[i].dipole_moment(universe, timestep)

	res = -np.sum((np.sum(ms, axis=1)/len(molecules))**2)
	res += np.sum(ms*ms)/len(molecules)

	return res

class molecule(object):
	def __init__(self, universe, ids):
		self._ids = ids
		self._charges = universe.atoms[ids].charges()*1.609*10e-19
		self._revmap = dict()
		for here, there in enumerate(self._ids):
			self._revmap[there] = here

		# fetch bonds
		self._bonds = []
		ag = universe.atoms[ids]
		self._ag = ag
		for key in ag.bondDict.keys():
			for bond in ag.bondDict[key]:
				self._bonds.append((bond.atom1.number, bond.atom2.number))

	def dipole_moment(self, universe, timestep):
		coord = self._ag.get_positions(ts=timestep)
		mu = np.zeros(3)
		for atom1, atom2 in self._bonds:
			mu += coord[self._revmap[atom1]]-coord[self._revmap[atom2]] * (self._charges[self._revmap[atom1]]-self._charges[self._revmap[atom2]])
		return mu

def main():
	"""
	Wrapper function.
	"""
	output = ot.output_tracker()
	mda = fc._require_mda(output)
	args = parser.parse_args()

	# messages
	messages = fc.messages

	# read input
	output.print_info('Reading source files.').add_level()
	output.print_info('Opening file %s.' % args.topology)
	output.print_info('Opening file %s.' % args.coordinates)

	# create Universe
	fc.mda_set_periodic(True, output)
	u_c = fc.mda_load_universe(args.topology, args.coordinates, output)
	output.print_info('Coordinate file holds %d frames.' % len(u_c.trajectory)).del_level()

	# build groups
	resids = set([_.resid for _ in u_c.atoms])
	output.print_info('Found %d residues. Using them as groups.' % len(resids))
	groups = []
	for resid in resids:
		groups.append(molecule(u_c, [_.number for _ in u_c.atoms if _.resid == resid]))

	# calculate epsilon
	for timestep in u_c.trajectory:
		m = magnetic_moments(u_c, timestep, groups)
		print 1+4*3.14/(3*timestep.volume*1.38*10e-23*args.temperature)*m
		

if __name__ == '__main__':
	main()