#!/usr/bin/env python -u
"""
Calculates the viscosity of a fluid. 


"""
# system modules
import argparse
import itertools
import math
import numpy as np

# custom modules
import f_core as fc
import output_tracker as ot

parser = argparse.ArgumentParser()
parser.add_argument('topology', type=str, help='The topology to work with.')
parser.add_argument('coordinates', type=str, help='The coordinates to work with.')
parser.add_argument('velocities', type=str, help='The velocities to work with.')
parser.add_argument('temperature', type=float, help='The simulation temperature.')
parser.add_argument('--selection_frame', type=int, help='Input frame to select on (zero-based).', default=0)
parser.add_argument('--atom-charmm', type=str, help='CHARMM selection syntax.', default=None)

def get_lj_force(e1, e2, s1, s2, r):
	e = math.sqrt(e1*e2)
	s = (s1+s2)/2
	return -24*e*(s**6/r**7-2*s**12/r**13)

def get_coulomb_force(q1, q2, r):
	return 1389.355 * q1 * q2 / r**2

def get_parameters(atomtype):
	data = None
	if atomtype == 'FCF3':
		data = [-0.0240, 1.3400, -0.12]
	if atomtype == 'CCF3':
		data = [-0.0780, 2.0400, 0.36]
	if atomtype == 'FCF2':
		data = [-0.1050, 1.6300, -0.185]
	if atomtype == 'CCF2':
		data = [-0.0420, 2.0500, 0.37]
	if data is None:
		raise ValueError('Unknown atom type.')
	data[1] *= 2**(5./6)
	return data

def get_force(universe, group1, group2, frame, axis, output):
	# CHARMM force field: LJ and Coulomb
	#if set(group1) == set(group2):
	#	output.print_error(messages.IDENTICAL_GROUPS)

	force = np.array((0,0,0))
	g1pos = universe.atoms[group1].get_positions()
	g2pos = universe.atoms[group2].get_positions()
	for idx1, atom1 in enumerate(group1):
		e1, s1, q1 = get_parameters(universe.atoms[atom1].type)
		for idx2, atom2 in enumerate(group2):
			e2, s2, q2 = get_parameters(universe.atoms[atom2].type)
			d = g1pos[idx1]-g2pos[idx2]
			n = np.linalg.norm(d)
			f = get_lj_force(e1, e2, s1, s2, n) + get_coulomb_force(q1, q2, n)
			f *= d / n
			force += f

	return force[axis]

def get_velocity(universe, group, frame, output):
	"""
	Extracts the velocity of a molecule from the trajectory.
	
	Returns
	-------
	Iterable :
		Cartesian representation of velocities in Angstrom/ps.
	"""
	try:
		d = universe.atoms[group].get_velocities(ts=frame, copy=True)
	except:	
		# TODO: check for DCD file format
		d = universe.atoms[group].get_positions() * 20.45482706
	m = universe.atoms[group].masses()
	total = sum(map(lambda x: x[0]*x[1], zip(d, m)))
	return total / (len(group) * sum(m))

def get_distance(universe, group1, group2, frame, axis, output):
	r1 = universe.atoms[group1].centerOfMass()
	r2 = universe.atoms[group2].centerOfMass()
	d = r1-r2
	return abs(d[axis])

def get_mass(universe, group, output):
	return sum(universe.atoms[group].masses())

def sigma(coordinates, velocities, groups, frame, alpha, beta, output):
	"""
	Calculates sigma.

	Parameters
	----------
	coordinates : :class:`MDAnalysis.Universe`
		The trajectory to work on.
	velocities : :class:`MDAnalysis.Universe`
		The velocities to work with.
	groups : Tuple of Tuples
		All groups (either molecules or atoms) that are being considered as moving entity. Single atom indices have to be given as tuples, as well. Indices are zero-based.
	frame : Integer
		The timestep to work on. Zero-based.
	alpha : Integer
		The first axis to select. (0 = x, 1 = y, 2 = z)
	beta : Integer
		The second axis to select. (0 = x, 1 = y, 2 = z)
	output : :class:`output_tracker.output_tracker`
		Instance for logging purposes. 

	Returns
	-------
	sigma :
		In units of amu m^2/s^2.
	"""
	value = 0
	for idx, group in enumerate(groups):
		velocity = get_velocity(velocities, group, frame, output)
		value += velocity[alpha] * velocity[beta] * get_mass(coordinates, group, output)
		for group_idx in range(idx + 1, len(groups)):
			force = get_force(coordinates, group, groups[group_idx], frame, alpha, output)
			distance = get_distance(coordinates, group, groups[group_idx], frame, beta, output)
			value += force * distance
	exit(2)

	value /= len(groups)
	return value

def P(coordinates, velocities, groups, frame, alpha, beta, output):
	value = sigma(coordinates, velocities, groups, frame, alpha, beta, output) + sigma(coordinates, velocities, groups, frame, beta, alpha, output)
	value /= 2
	if alpha == beta:
		for gamma in (0, 1, 2):
			value -= sigma(coordinates, velocities, groups, frame, gamma, gamma, output)

	return value

class group(object):
	def __init__(self, coordinates, indices):
		self._masses = coordinates.atoms[indices].masses()
		self._mass = sum(self._masses)
		self._params = [get_parameters(coordinates.atoms[_].type) for _ in indices]
		self._es = np.array([_[0] for _ in self._params])
		self._ss = np.array([_[1] for _ in self._params])
		self._qs = np.array([_[2] for _ in self._params])
		self._indices = indices

def P_complete(coordinates, velocities, groups, framenum, output):
	# extract velocities and coordinates on a group basis
	cor = coordinates.trajectory[framenum][:]
	vel = velocities.trajectory[framenum][:]

	n = len(groups)
	g_mass = np.zeros(n)
	g_coord = np.zeros([n, 3])
	g_vel = np.zeros([n, 3])
	for idx, group in enumerate(groups):
		g_mass[idx] = group._mass
		g_coord[idx] = np.sum(cor[group._indices].transpose() * group._masses, axis=1)/group._mass
		g_vel[idx] = np.sum(vel[group._indices].transpose() * group._masses, axis=1)/group._mass

	# calculate forces and distances
	g_fd = np.zeros([n, n, 3])
	for i in range(n):
		g1_cor = cor[groups[i]._indices]
		g_fd[i+1:, i] = g_coord[i]-g_coord[i+1:]
		for j in range(i+1, n):
			if np.linalg.norm(g_fd[j, i]) > 15:
				continue
			g2_cor = cor[groups[j]._indices]
			for idx, atom in enumerate(g1_cor):
				d = g2_cor - atom
				r = np.linalg.norm(d, axis=1)

				es = np.sqrt(groups[i]._es[idx] * groups[j]._es)
				ss = (groups[i]._ss[idx] + groups[j]._ss)/2
				qs = groups[i]._qs[idx] * groups[j]._qs
				res = -24*es*(ss**6/r**7-2*ss**12/r**13)*4.1868
				res += 1389.355 * qs / r**2
				d = d.transpose()/r
				g_fd[i, j] += np.linalg.norm(res * d, axis=1)

	# calculate sigmas
	sigma = np.zeros([3, 3])
	for alpha in range(3):
		for beta in range(3):
			sigma[(alpha, beta)] += np.sum(g_vel[:,alpha] * g_vel[:,beta] * g_mass)
			for i in range(n):
				for j in range(i+1, n):
					sigma[(alpha, beta)] += g_fd[i, j, alpha] * g_fd[j, i, beta]
	sigma /= n

	# calculate P
	P = np.zeros([3, 3])
	for alpha in range(3):
		for beta in range(3):
			P[alpha, beta] = (sigma[alpha, beta]+sigma[beta, alpha])/2
			if alpha==beta:
				P[alpha, beta] -= sum([sigma[_, _] for _ in range(3)])

	return P

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
	output.print_info('Opening file %s.' % args.velocities)

	# create Universe
	fc.mda_set_periodic(True, output)
	u_c = fc.mda_load_universe(args.topology, args.coordinates, output)
	output.print_info('Coordinate file holds %d frames.' % len(u_c.trajectory))
	u_v = fc.mda_load_universe(args.topology, args.velocities, output)
	output.print_info('Velocity file holds %d frames.' % len(u_v.trajectory))
	if len(u_v.trajectory) != len(u_c.trajectory):
		output.print_error(messages.VEL_COORD_MISMATCH)
	else:
		output.del_level()

	# build groups
	resids = set([_.resid for _ in u_c.atoms])
	output.print_info('Found %d residues. Using them as groups.' % len(resids))
	groups = []
	for resid in resids:
		groups.append(group(u_c, [_.number for _ in u_c.atoms if _.resid == resid]))

	# running calculation of eta
	history = np.zeros((len(u_c.trajectory), 3, 3))
	history[0,0:,0:] = P_complete(u_c, u_v, groups, 0, output)
	b = [history[0,0,1]]
	eta = 0
	for frame in xrange(1, len(u_c.trajectory)):
		#eta += np.sum(P_complete(u_c, u_v, groups, frame, output)*cache)
		#print frame, eta*u_c.trajectory[frame].volume*1.66053892*10e-4/(10*1.3806488*args.temperature)	
		history[frame,0:,0:] = P_complete(u_c, u_v, groups, frame, output)
		b.append(history[frame,0,1])
		#autocorr = np.correlate(history[:frame,0,1], history[:frame,0,1], mode='full')
		autocorr = np.correlate(b,b, mode='full')
		autocorr = autocorr[autocorr.size/2:]
		autocorr /= autocorr[0]
		print frame, sum(autocorr)*u_c.trajectory[frame].volume*1.66053892*10e-4/(10*1.3806488*args.temperature)
		#for idx, a in axes:
			#alpha, beta = a

			#eta += P(u_c, u_v, groups, frame, alpha, beta, output) * cache[idx]
			#print frame, eta*u.trajectory[frame].volume*1.66053892*10e-4/(10*1.3806488*temperature)

if __name__ == '__main__':
	main()
