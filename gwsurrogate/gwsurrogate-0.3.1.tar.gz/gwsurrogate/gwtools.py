# --- gwtools.py ---

"""
	A collection of useful gravitational wave tools
"""

from __future__ import division

__copyright__ = "Copyright (C) 2014 Scott Field and Chad Galley"
__email__     = "sfield@astro.cornell.edu, crgalley@tapir.caltech.edu"
__status__    = "testing"
__author__    = "Scott Field, Chad Galley"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import minimize


##############################################
# Functions for changing parameters

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def m1m2_to_Mc(m1,m2):
    """Chirp mass from m1, m2"""
    return (m1*m2)**(3./5.)/(m1+m2)**(1./5.)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def m1m2_to_nu(m1,m2):
    """Symmetric mass ratio from m1, m2"""
    return m1*m2/(m1+m2)**2

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def m1m2_to_Mcnu(m1, m2):
	"""Compute symmetric mass ratio and chirp mass from m1, m2"""	
	return m1m2_to_Mc(m1,m2), m1m2_to_nu(m1,m2)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def q_to_nu(q):
	"""Convert mass ratio (which is >= 1) to symmetric mass ratio"""
	return q / (1.+q)**2.

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def nu_to_q(nu):
	"""Convert symmetric mass ratio to mass ratio (which is >= 1)"""
	return (1.+np.sqrt(1.-4.*nu)-2.*nu)/(2.*nu)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def Mq_to_m1m2(M, q):
	"""Convert total mass, mass ratio pair to m1, m2"""
	m2 = M/(1.+q)
	m1 = M-m2
	return m1, m2

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def Mq_to_Mc(M, q):
	"""Convert mass ratio, total mass pair to chirp mass"""
	return M*q_to_nu(q)**(3./5.)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def Mcq_to_M(Mc, q):
	"""Convert mass ratio, chirp mass to total mass"""
	return Mc*q_to_nu(q)**(-3./5.)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def Mcnu_to_M(Mc, nu):
	"""Convert chirp mass and symmetric mass ratio to total mass"""
	return Mc*nu**(-3./5.)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def Mnu_to_Mc(M, nu):
	"""Convert total mass and symmetric mass ratio to chirp mass"""
	return M*nu**(3./5.)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def Mcnu_to_m1m2(Mc, nu):
	"""Convert chirp mass, symmetric mass ratio pair to m1, m2"""
	q = nu_to_q(nu)
	M = Mcq_to_M(Mc, q)
	return Mq_to_m1m2(M, q)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def m1m2_to_delta(m1, m2):
	"""Convert m1, m2 pair to relative mass difference [delta = (m1-m2)/(m1+m2)]"""
	return (m1-m2)/(m1+m2)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def delta_to_nu(delta):
	"""Convert relative mass difference (delta) to symmetric mass ratio"""
	return (1.-delta**2)/4.

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def nu_to_delta(nu):
	"""Convert symmetric mass ratio to relative mass difference delta"""
	return np.sqrt(1.-4.*nu)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def X1X2_to_Xs(X1, X2):
	"""Convert dimensionless spins X1, X2 to symmetric spin Xs"""
	return (X1+X2)/2.

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def X1X2_to_Xa(X1, X2):
	"""Convert dimensionless spins X1, X2 to anti-symmetric spin Xa"""
	return (X1-X2)/2.

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def X1X2_to_XsXa(X1, X2):
	"""Convert dimensionless spins X1, X2 to symmetric and anti-symmetric spins Xs, Xa"""
	return X1X2_to_Xs(X1,X2), X1X2_to_Xa(X1,X2)


##############################################
#

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def fgwisco(Mtot):
	"""GW frequency at ISCO. [Note: Maggiore's text has an extra 1/2.]"""
	return 6.0**(-1.5) / (np.pi*Mtot)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def get_arg(a, a0):
	"""Get argument at which a0 occurs in array a"""
	return np.argmin(np.abs(a-a0))

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def get_peak(x, y):
	"""Get argument and values of x and y at maximum value of |y|"""
	arg = np.argmax(y)
	return [arg, x[arg], y[arg]]

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def fit_peak(x, y, ftype='poly', i1=10, i2=10, deg=2, num=1000):
	"""
	Estimate peak of y through interpolation.
		
	Input
	=====
	x		--- x data array (1d)
	y		--- y data array (1d)
	ftype	--- Type of fitting function (default='poly')
	i1		--- Number of points to fit before estimated peak (default=10)
	i2		--- Number of points to fit after estimated peak (default=10)
	deg		--- Degree or order of fitting function (default=2)
	num		--- Number of high resolution x samples for estimating peak (default=1000)
	
	Output
	======
	x_peak 	--- Estimated x value of the estimated maximum of y data
	y_peak	--- Estimated maximum of y data
	
	Note: Choose between 'poly' and 'spline' for polynomial and 1d 
	spline fitting functions. The fitting is currently done with ROMpy. 
	The maximum of the y data is estimated by evaluating the fitting
	function at num(=1000) points. However, the default fitting 
	function is a quadratic polynomial, the peak of which is 
	calculated analytically and does not use num.
	"""
	
	# Get argument of discrete data y
	arg = np.argmax(y)
	
	# Take di1 and di2 points of x and y data around peak
	x_fit = x[arg-i1:arg+i2+1]
	y_fit = y[arg-i1:arg+i2+1]
	
	# Fit over this interval using the requested fitting function
	if ftype == 'poly':
		fit = Polynomial(x_fit, y_fit, deg=deg)
		if deg == 2:
			c, b, a = fit.fitparams
			x_peak = -b/(2.*c)
		else:
			x_fine = np.linspace(x_fit[0], x_fit[-1], num)
			x_peak = x_fine[np.argmax(fit.fit(x_fine))]
	
	elif ftype == 'spline':
		fit = Spline1d(x_fit, y_fit, k=deg)
		x_fine = np.linspace(x_fit[0], x_fit[-1], num)
		x_peak = x_fine[np.argmax(fit.fit(x_fine))]
		y_peak = fit.fit(x_peak)
		
	else:
		raise Exception, "Fit types must be 'poly' or 'spline'."
	
	y_peak = fit.fit(x_peak)
	return x_peak, y_peak

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def chop(x, y, xmin, xmax):
	"""Chop arrays x, y for x in [xmin, xmax]"""
	argmin = get_arg(x, xmin)
	argmax = get_arg(x, xmax)
	return x[argmin:argmax+1], y[argmin:argmax+1]

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def shift(x, xshift):
	"""Shift array x by xshift"""
	arg = get_arg(x, xshift)
	return x-x[arg]

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def shift_chop(x, y, xshift, xmin, xmax):
	"""Shift x, y arrays by xshift then chop for x in [xmin, xmax]"""
	xnew = shift(x, xshift)
	xminnew = xmin-xshift
	xmaxnew = xmax-xshift
	return chop(xnew, y, xminnew, xmaxnew)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def amp(h):
	"""Get amplitude of waveform, h = A*exp(i*phi)"""
	return np.abs(h)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def amp_phase(h):
    """Get amplitude and phase of waveform, h = A*exp(i*phi)"""

    amp = np.abs(h);
    return amp, phase(h)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def phase(h):
	"""Get phase of waveform, h = A*exp(i*phi)"""
	if np.shape(h):
		# Compute the phase only for non-zero values of h, otherwise set phase to zero.
		nonzero_h = h[np.abs(h) > 1e-300]
		phase = np.zeros(len(h), dtype='double')
		phase[:len(nonzero_h)] = np.unwrap(np.real(-1j*np.log(nonzero_h/np.abs(nonzero_h))))
	else:
		nonzero_h = h
		phase = np.real(-1j*np.log(nonzero_h/np.abs(nonzero_h)))
	return phase

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def cycles(h):
	"""Count number of cycles (to merger, if present) in waveform"""
	phi = phase(h)
	ipk, phi_pk, A_pk = get_peak(phi, np.abs(h))
	return (phi_pk - phi[0])/(2.*np.pi)
	
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def hplus(h):
	"""Get real part of waveform, h = A*exp(i*phi)"""
	return np.real(h)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def hcross(h):
	"""Get imaginary part of waveform, h = A*exp(i*phi)"""
	return np.imag(h)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def logd(t,f):
	"""Compute a logarithmic derivative"""
	dfdt = np.diff(f)/np.diff(t)
	return t[1:], dfdt/f[1:]

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def plot_pretty(time, y, fignum=1, flavor='linear', color='k', linestyle=['-', '--'], \
				label=['$h_+(t)$', '$h_-(t)$'], legendQ=True, showQ=False):
	"""create a waveform figure with nice formatting and labels.
	returns figure method for saving, plotting, etc."""

	import matplotlib.pyplot as plt
	
	# Plot waveform
	fig = plt.figure(fignum)
	ax = fig.add_subplot(111)
	
	dim_y = np.shape(y)
	num_y = len(dim_y)
	num_color, num_label = np.size(color), np.size(label)
	dim_linestyle = np.shape(linestyle)
	
	if num_y > 2:
		raise ValueError("Can only plot one or two functions")
	
	for ii in range(num_y):

		if num_y == 1: yy = y
		else: yy = y[ii]
		
		if num_color == 1: cc = color
		else: cc = color[ii]
		
		if num_label == 1: ll = label
		else: ll = label[ii]
		
		if len(dim_linestyle) == 0: ss = linestyle
		elif len(linestyle) == 1: ss = linestyle[0]
		else: ss = linestyle[ii]
		
		if flavor == 'linear':
			if legendQ:
				plt.plot(time, yy, color=cc, linestyle=ss, label=ll)
			else:
				plt.plot(time, yy, color=cc, linestyle=ss)
			
		elif flavor == 'semilogy':
			if legendQ:
				plt.semilogy(time, yy, color=cc, linestyle=ss, label=ll)
			else:
				plt.semilogy(time, yy, color=cc, linestyle=ss)
		
		else:
			raise ValueError("Not a valid plot type")

	plt.xlabel('Time')
	plt.ylabel('Waveform')
	
	if legendQ:
		plt.legend(loc='upper left')
	
	if showQ:
		plt.show()
	
	return fig


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def ecc_estimator(t,h,fit_window,type=1,fit_deg=1):
	""""Estimate the eccentricity associated with gravitational 
	waveform h from Eq. (17) of arxiv:1004.4697 (gr-qc)."""

	### TODO: add butterworth filter for fit residuals. what would amplitude estimator look like?

	### crop h to fit interval ###
	ecc_interval = np.arange(fit_window[0],fit_window[1])
	t            = t[ecc_interval]
	h            = h[ecc_interval]

	if type == 1:

		### fit phase with degree fit_deg polynomial on fit_window ###
		amp_tmp, phase = get_amp_phase(h)
		p_coeff        = np.polyfit(t,phase,fit_deg)
		phase_fit      = np.polyval(p_coeff,t)

		### compute the estimator ###
		ecc_est = ( phase - phase_fit ) / 4.

		return t, ecc_est

	elif type == 2:

		amp_tmp        = amp(h)
		t, amp_log     = logd(t,amp_tmp) # t will be one element shorter than before
		p_coeff        = np.polyfit(t,amp_log,fit_deg)
		amplog_fit     = np.polyval(p_coeff,t)

		return t, (amp_log - amplog_fit)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def find_instant_freq(hp, hc, t):
    """instantaneous starting frequency for 

                h = A(t) exp(2 * pi * i * f(t) * t), 

       where we approximate \partial_t A ~ \partial_t f ~ 0."""

    h    = hp + 1j*hc
    dt   = t[1] - t[0]
    hdot = (h[2] - h[0]) / (2 * dt) # 2nd order derivative approximation at t[1]

    f_instant = hdot / (2 * np.pi * 1j * h[1])
    f_instant = f_instant.real

    return f_instant

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def dimensionless_time(M,t):
    """ input time and mass in seconds. return dimensionless time """
    #tmp = lal.LAL_MSUN_SI * lal.LAL_G_SI / np.power(lal.LAL_C_SI,3.0)
    #return ( t / tmp ) / M
    return t/M

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def remove_amplitude_zero(t,h):
    """ removes h[i] t[i] from array if |h[i]| = 0 """

    amp, phase     = amp_phase(h)
    where_non_zero = np.nonzero(amp)

    return t[where_non_zero], h[where_non_zero]


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def modify_phase(h,offset):
    """ Modify GW mode's phase to be \phi(t) -> \phi(t) + offset.
        For h_{ell,m}, typically offset = m*z_rot where z_rot is a 
        physical rotation about the z-axix (orthogonal to the orbital plane)."""

    return  h*np.exp(1.0j * offset)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def coordinate_time_shift(t,offset):
    """ modify times to be t -> t + offset """

    return t + offset

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def find_common_time_window(t1,t2):
    """ given two temporal grids, find the largest range of common times 
        defined by [min_common,max_common] """

    min_common = max( t1[0], t2[0] )
    max_common = min( t1[-1], t2[-1] )
    
    if (max_common <= min_common):
        raise ValueError("there is no common time grid")

    return min_common, max_common

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def simple_align_params(t1,h1,t2,h2):
    """ t1 times for complex waveform h1. 

        This routine returns simple alignment parameters 
        deltaT and deltaPhi by...
          (i)  fining discrete waveform peak
          (ii) aligning phase values at the peak time """

    amp1,phase1 = amp_phase(h1)
    amp2,phase2 = amp_phase(h2)

    deltaT   = t1[np.argmax( amp1 )] - t2[np.argmax( amp2 )]
    deltaPhi = phase1[np.argmax( amp1 )] - phase2[np.argmax( amp2 )]

    return deltaT, deltaPhi

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def euclidean_norm_sqrd(f,dx):
    """ Euclidean norm squared of a complex vector f """
    return (np.sum(f*np.conj(f)) * dx).real

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def euclidean_norm_sqrd_2sphere(f,dx):
    """ Euclidean norm squared of a complex function 

       h(t,theta,phi) = \sum h_{ell,m}(t) B_{ell,m} (theta,phi) 

       known through its harmonic coefficients h_{ell,m}, each
       of which are column vector of an input matrix f."""

    full_norm = 0.0
    for ii in range(f.shape[1]):
        full_norm += euclidean_norm_sqrd(f[:,ii],dx)

    return full_norm


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def generate_parameterize_waveform(t,h1_func,h1_type,h1_params=None):
  """ returns function for h(t;tc,phic) evaluations.

    INPUT
    =====
    t         --- array of times
    h1_func   --- waveform which can be evaluated for input set of times 
    h1_type   --- h1_func type ('interp1d','h_sphere') 
    h1_params --- any additional parameters needed for waveform evalautions"""

  if h1_type == 'interp1d': # interpolant built from scipy.interpolate.interp1d(t,h1_data)
    def parameterize_waveform(x):

      tc   = x[0]
      phic = x[1]

      h1_eval = h1_func( coordinate_time_shift(t,tc) ) # differing sign from minimize_norm_error is correct
      h1_eval = modify_phase(h1_eval,-phic)

      return h1_eval
  elif h1_type == 'h_sphere': # waveform from h_sphere_builder
    theta = h1_params
    def parameterize_waveform(x):

      tc   = x[0]
      phic = x[1]

      times = coordinate_time_shift(t,tc)
      hp,hc = h1_func(times,theta=theta, phi=0.0, z_rot=phic, psi_rot=None)
      return hp + 1.0j*hc
  else:
    raise ValueError('unknown waveform type')

  return parameterize_waveform


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def generate_parameterized_norm(h1,h_ref,mynorm,t=None):
    """ 
    this routine will return a parameterized discrete norm 

           N(p1,p2,...) = || h1(p1,p2,...) - h_ref || 

    which can be minimized over the parameters (p1,p2...). If p1 = p2 = ... = 0 then 
    the norm is simply

                   || h1 - h_ref ||   for h1 = h1[t]

    h_ref is a reference waveform (represented by a discrete set
    evaluations) to which we match another waveform h1 (represented as a
    function). 

    h1 is a python function which takes inputs p1, p2,...
    where, typically, p1 is timeshift (tc) and p2 is a rotation about 
    the z-axis phic. The function h1 returns a vector h1(t_c,phi_c) collocated
    with h2_ref.


    Input
    =====
    t:         array of times such that h2_ref = h_ref[t]
    h2_ref:    array of reference waveform evaluations
    h1:        parameterized waveform function 
    mynorm:    function s.t. mynorm(f,dt) is a discrete norm


    Input expectations
    ==================
    (i) h1 should be defined on a larger temporal grid 
        than t and, hence, h2_ref. Why? When looking for the 
        minimum, h1 will be evaluated at times t + deltaT. 
        t should be viewed as the "common set of times" on which both 
        h1 and h_ref are known. """

    dt = 1.0 # we optimize the relative errors, factors of dt cancel

    # TODO: should check for TypeError by seeing if parameterized waveform can be evaluated by passing single x
    def ParameterizedNorm(x):

        h1_trial = h1(x)
        diff_h    = h1_trial - h_ref

        # normalize by h2_ref as its fixed. Goal is to match h1 to h_ref #
        overlap_errors = mynorm(diff_h,dt)/mynorm(h_ref,dt) 

        return overlap_errors

    return ParameterizedNorm

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def create_common_time_grid(t1,t2,t_low_adj,t_up_adj):
  """ from temporal grids t1 and t2, create grid of common times"""

  common_dt      = (t1[2] - t1[1]) # TODO: t2 or t1 or variable
  t_start, t_end = find_common_time_window(t1,t2)
  common_times   = np.arange(t_start+t_low_adj,t_end-t_up_adj,common_dt) # small buffer needed 

  return common_times, t_start, t_end, common_dt

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def discrete_minimization_from_discrete_waveforms(t,h,t_ref,h_ref):
  deltaT, deltaPhi = simple_align_params(t,h,t_ref,h_ref)
  h                = modify_phase(h,-deltaPhi)
  t                = coordinate_time_shift(t,-deltaT) # different sign from generate parameterize norm is correct

  return deltaT, deltaPhi, t, h

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def setup_minimization_from_discrete_waveforms(t1,h1,t2,h2,t_low_adj,t_up_adj,verbose=False):

  t1, h1 = remove_amplitude_zero(t1,h1)
  t2, h2 = remove_amplitude_zero(t2,h2)

  if( (t1[-1] - t1[0]) < (t2[-1] - t2[0]) ):
      raise ValueError('first waveform should be longer')


  deltaT, deltaPhi, t1, h1 = discrete_minimization_from_discrete_waveforms(t1,h1,t2,h2)

  common_times, t_start, t_end, common_dt = create_common_time_grid(t1,t2,t_low_adj,t_up_adj)

  h1_interp = interp1d(t1,h1)
  h2_interp = interp1d(t2,h2)

  h2_eval = h2_interp(common_times)

  if(verbose):
    common_times_full = np.arange(t_start,t_end,common_dt)
    h2_eval_full_nrm  = mynorm(h2_interp(common_times_full),1.0)
    h2_eval_nrm       = mynorm(h2_interp(common_times),1.0)
    print "|| h_full || /  || h_adjmynorm(h2_eval_full) = ",h2_eval_full_nrm/h2_eval_nrm

  return h1_interp, h2_eval, common_times, deltaT, deltaPhi

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def minimize_waveform_match(h1_parameterized,href,mynorm,start_values,method):
    """ write me: should pass vector of values to h1... will generalize """

    ParameterizedNorm = generate_parameterized_norm(h1_parameterized,href,mynorm)

    opt_result   = minimize(ParameterizedNorm, start_values, method=method,tol=1e-12)
    opt_solution = opt_result.x

    min_norm     = ParameterizedNorm(opt_solution) # norm's value at global minimum
    h1_align     = h1_parameterized(opt_solution) # h1 waveform optimally matched to href
    guessed_norm = ParameterizedNorm(start_values) # norm's value using initial guess

    return [guessed_norm,min_norm], opt_solution, h1_align

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#TODO: better description needed
def minimize_norm_error(t1,h1,tref,href,mynorm,t_low_adj=.1,t_up_adj=.1,method='nelder-mead',verbose=False):
    """
    Input
    ===== 
    t1,h1:      time/waveform vectors sampled at equally spaced times
    tref,href:  a pair of reference time/waveform vectors
    mynorm:     norm function (e.g. euclidean_norm_sqrd(f,dx) ) which takes a vector f
    t_low,t_up: adjusments  to "clip" the start and end portions of the pre-aligned waveforms

    Output
    ====== 
    guessed:      relative norm error with discrete "guess" for tc and phic offsets 
    min_norm:     minimized norm error by solving optimization problem
    tc, phic:     time/phase offsets which solve the 2D minimization problem
    common_times: WRITE ME
    h1_align:     WRITE ME
    href_eval:      WRITE ME

    Output in form [guessed, min_norm]  [tc, phic]  [common_times, h1_align, href_eval]


    Input expectations
    ================== 
    (i)  t1 and tref should be equally spaced grid of times. 
    (ii) for waveforms of different length, (t1,h1) pair should be longer

    Output caveats
    ============== 
    (i) evaluating the norm with values of (tc,phic) might give slightly different answers
        depending on the order of shifts/interpolants etc."""

    ### from discrete waveform data (t1,h1) and (tref,href), return items needed to solve minimization problem ###
    h1_interp, href_eval, common_times, deltaT, deltaPhi = \
        setup_minimization_from_discrete_waveforms(t1,h1,tref,href,t_low_adj,t_up_adj,verbose)

    ### h1_parameterized returns evaluations at common_times for given (tc,phic), induces parameterized norm ###
    h1_parameterized  = generate_parameterize_waveform(common_times,h1_interp,'interp1d')

    [guessed_norm,min_norm], opt_solution, h1_align = minimize_waveform_match(h1_parameterized,href_eval,mynorm,[0.0,0.0],method)

    tc         = opt_solution[0] + deltaT
    phic       = opt_solution[1] + deltaPhi


    return [guessed_norm, min_norm], [tc, phic], [common_times, h1_align, href_eval]

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def minimize_norm_error_multi_mode(t1,h1,tref,href,mode_list,ell_m_match,t_low_adj=.1,t_up_adj=.1,method='nelder-mead',verbose=False):
  """ performs single-mode match, uses optimal match parameters for multi-mode waveform alignment"""

  ### solve single mode match here ###
  ell_match = ell_m_match[0]
  m_match   = ell_m_match[0]

  mode_indx = mode_list.index((ell_match,m_match))
  h_ref_22 = href[:,mode_indx]
  h1_22    = h1[:,mode_indx]

  [guessed_norm_1mode, minimized_norm_1mode], [tc, phic], [common_times,h1_align,href_align] = \
    minimize_norm_error(t1,h1_22,tref,h_ref_22,euclidean_norm_sqrd,method='nelder-mead')
  z_rot_opt = -phic/m_match

  ### use single mode results for multi-mode waveform ###
  h_sphere = h_sphere_builder(mode_list,href.real,href.imag,tref)
  href_eval_hp, href_eval_hc    = h_sphere(common_times)
  href_eval = href_eval_hp + 1.0j*href_eval_hc

  h_sphere = h_sphere_builder(mode_list,h1.real,h1.imag,t1)
  h1_align_hp, h1_align_hc  = h_sphere(times=common_times+tc,z_rot=z_rot_opt)
  h1_align = h1_align_hp + 1.0j*h1_align_hc

  ### check multi-mode waveform's closeness ###
  h_diff = href_eval - h1_align
  min_norm_sphere = euclidean_norm_sqrd_2sphere(h_diff,1.0)/euclidean_norm_sqrd_2sphere(href_eval,1.0)

  ### compute errors mode-by-mode ###
  rel_mode_errors = compute_many_mode_errors(h1_align,href_eval,mode_list,euclidean_norm_sqrd)

  return [rel_mode_errors, min_norm_sphere], [tc, z_rot_opt], [common_times,h1_align,href_eval]
  


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def h_sphere_builder(modes,hp,hc,t):
  """Returns a function h(t,theta,phi;z_rot,tc). This function can be evaluated 
     for rotations about z-axis and returns either (i) a list of modes or (ii) 
     evaluation on sphere at (theta, phi)

      INPUT
      =====
      modes --- array of modes (ell,m)
      hp/hc --- matrix modes. each column is a mode evaluation for (ell[i],m[i]) in modes
      t     --- arrary of times at which modes have been evaluated"""

  from harmonics import sYlm as sYlm
  from scipy.interpolate import splrep
  from scipy.interpolate import splev

  ### fill dictionary with model's modes as a spline ###
  hp_modes_spline = dict()
  hc_modes_spline = dict()
  ii = 0
  for ell_m in modes:
    hp_modes_spline[ell_m] = splrep(t, hp[:,ii], k=3)
    hc_modes_spline[ell_m] = splrep(t, hc[:,ii], k=3)
    ii += 1

  ### time interval for valid evaluations ###
  t_min = t.min()
  t_max = t.max()

  ### create function which can be used to evaluate for h(t,theta,phi) ###
  def h_sphere(times,theta=None,phi=None,z_rot=None,psi_rot=None):
    """ evaluations h(t,theta,phi), defined as matrix of modes, or sphere evaluations.

        INPUT
        =====
        times     --- numpy array of times to evaluate at
        theta/phi --- angle on the sphere, evaluations after z-axis rotation
        z_rot     --- rotation angle about the z-axis (coalescence angle)
        psi_rot   --- overall phase adjustment of exp(1.0j*psi_rot) mixing h+,hx"""

    # TODO: restore this after testing
    #if times.min() < t_min or times.max() > t_max:
    #  raise ValueError('surrogate cannot be evaluated outside of its time window')

    if psi_rot is not None:
      raise ValueError('not coded yet')

    ### output will be h (if theta,phi specified) or hp_modes, hc_modes ###
    if theta is not None and phi is not None:
      h = np.zeros((times.shape[0],),dtype=complex)
    else:
      hp_modes = np.zeros((times.shape[0],len(modes)))
      hc_modes = np.zeros((times.shape[0],len(modes)))

    ### evaluate modes at times ###
    jj=0
    for ell_m in modes:

      hp_modes_eval = splev(times, hp_modes_spline[ell_m])
      hc_modes_eval = splev(times, hc_modes_spline[ell_m])

      ### apply rotation about z axis and evaluation on sphere if requested ###
      h_modes_eval  = hp_modes_eval + 1.0j*hc_modes_eval
      if z_rot is not None:
        h_modes_eval = modify_phase(h_modes_eval,z_rot*ell_m[1])

      if theta is not None and phi is not None:
        sYlm_value =  sYlm(-2,ll=ell_m[0],mm=ell_m[1],theta=theta,phi=phi)
        h = h + sYlm_value*h_modes_eval

      else:
        hp_modes[:,jj] = h_modes_eval.real
        hc_modes[:,jj] = h_modes_eval.imag

      jj+=1

    if theta is not None and phi is not None:
      return h.real, h.imag
    else:
      return hp_modes, hc_modes

  return h_sphere

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def compute_many_mode_errors(h,h_ref,mode_list,mynorm):
  """input: matrix of modes h, h_ref, mode_list, and norm 
    output: dictionary relating mode to relative errors h_{ell,m} compared with href_{ell,m} """

  h_mode_diff = h_ref - h
  relative_mode_errs = dict()
  ii=0
  for ell_m in mode_list:
    err = mynorm(h_mode_diff[:,ii],1.0)/mynorm(h_ref[:,ii],1.0)
    relative_mode_errs[ell_m] = err
    ii += 1

  return relative_mode_errs

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def interpolant_h(t, h, deg=3):
	"""Compute spline interpolant of input data h at samples t."""
	
	dtype = h.dtype
	if dtype == 'complex':
		interp_real = splrep(t, np.real(h), k=deg)
		interp_imag = splrep(t, np.imag(h), k=deg)
		return interp_real, interp_imag
	elif dtype == 'double':
		interp = splrep(t, h, k=deg)
		return interp
	else:
		raise Exception, "Function to be interpolated must be real or complex."
	pass

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def interpolate_h(tin, h, tout, deg=3):
	"""Interpolate input data h at samples tout."""
		
	if tout[0] < tin[0] or tout[-1] > tin[-1]:
		print ">>> Warning: Requested samples are outside of interpolated domain."
	
	dtype = h.dtype
	if dtype == 'complex':
		interp_real, interp_imag = interpolant_h(tin, h, deg=deg)
		return splev(tout, interp_real) + 1j*splev(tout, interp_imag)
	elif dtype == 'double':
		inter = interpolant_h(tin, h, deg=deg)
		return splev(tout, interp)
	else:
		raise Exception, "Function to be interpolated must be real or complex."
	pass
