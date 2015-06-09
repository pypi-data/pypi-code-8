"""
Fits background 
* without response
* with empirical model
* iterative, starting with simple model and adding more components if justified
"""

from sherpa.astro.ui import *
import numpy
import json

"""
custom background statistic, similar to chi^2

Sherpa itself does not expose the statistic of the background fit
as far as I can tell. This has the benefit of being rather stable
and giving large, sensitive values when the fit is poor. (CStat tends to 
flatten out)

i: spectrum ID
"""
def my_bkg_stat(i):
	p = get_bkg_fit_plot(i)
	m = p.modelplot
	d = p.dataplot
	return (((d.y - m.y) / m.y) ** 2).mean()

def group_adapt(data, model, nmin = 20):
	i = 0
	while i < len(data):
		for j in range(i, len(data)+1):
			mask = numpy.arange(i, j)
			n = data[mask].sum()
			if n >= nmin or j + 1 >= len(data):
				yield (n, model[mask].sum())
				print '  groups', i,j,n
				break
		i = j + 1

def wstatfunc(data, model, staterror=None, syserror=None, weight=None):
	n = data.astype('int').sum()
	l = len(data)
	if n >= l * 20: # no rebinning needed
		return (((data - model) / model)**2).sum()
	else:
		r = numpy.sum([((d - m)/m)**2 for d, m in group_adapt(data.astype('int'), model, nmin=20)])
		print 'bxaroughstat: %.3f' % r
		return r, 0
def custom_staterr_func(data):
	return data**0.5
load_user_stat("bxaroughstat", wstatfunc, custom_staterr_func)


"""
custom routine to find the best normalisation in a robust way.

Often the starting point can be way off and the statistic will not 
give good indications which way to go. So use my_bkg_stat. This routine
tries to go both up and down from the starting point to escape this flatness.

i: spectrum ID
params: list of params to deal with, in sequence
disp: verbosity
"""
def my_norm_opt(i, params, disp=1):
	if disp > 1: print 'my_norm_opt: my optimization     --- of %s' % i
	if disp > 1: print 'my_norm_opt: \tparameters:', ', '.join([p.fullname for p in params])
	#plot_bkg_fit_resid(i)
	for p in params:
		if disp > 0: print 'my_norm_opt: \toptimizing %s normalization [%e .. %e]' % (p.fullname, p.min, p.max)
		startval = p.val
		beststat = my_bkg_stat(i)
		bestval = p.val
		if disp > 0: print 'my_norm_opt: \t\tstart val = %e: %e' % (p.val, beststat)
		go_up = True
		go_down = True
		for n in list(3.**numpy.arange(1, 20)) + [None] + list(1.1**numpy.arange(1, 13)):
			if n is None:
				startval = bestval
				if disp > 0: print 'my_norm_opt: \t\trefining from %e' % (startval)
				go_up = True
				go_down = True
				continue
			if go_up and startval * n > p.max:
				if disp > 0: print 'my_norm_opt: \t\thit upper border (%e * %e > %e)' % (startval, n, p.max)
				go_up = False
			if go_down and startval / n < p.min:
				if disp > 0: print '\t\thit lower border (%e / %e > %e)' % (startval, n, p.min)
				go_down = False
			if go_up:
				if disp > 1: print 'my_norm_opt: \t\ttrying %e ^' % (startval * n)
				p.val = startval * n
				newstat = my_bkg_stat(i)
				if disp > 1: print 'my_norm_opt: \t\tval = %e: %e' % (p.val, newstat)
				if newstat <= beststat:
					bestval = p.val
					beststat = newstat
					if disp > 0: print 'my_norm_opt: \t\t\timprovement: %e' % p.val
				if newstat > beststat + 100:
					go_up = False
			if go_down:
				if disp > 1: print 'my_norm_opt: \t\ttrying %e v' % (startval / n)
				p.val = startval / n
				newstat = my_bkg_stat(i)
				if disp > 1: print 'my_norm_opt: \t\tval = %e: %e' % (p.val, newstat)
				if newstat + 1e-3 < beststat:
					bestval = p.val
					beststat = newstat
					if disp > 0: print 'my_norm_opt: \t\t\timprovement: %e' % p.val
				if newstat > beststat + 100:
					go_down = False
		p.val = bestval
		print 'my_norm_opt: \tnew normalization of %s: %e' % (p.fullname, p.val)
		#plot_bkg_fit_resid(i)
	print 'my_norm_opt: optimization of %s in %s done, reached %.3f' % (', '.join([p.fullname for p in params]), i, beststat)
	if beststat > 0.2:
		print 'my_norm_opt: no good fit found: %.3f' % beststat
		if False:
			plot_bkg_fit_resid(i)
			print 'press ENTER >> ',
			sys.stdin.readline()
	
	if disp > 1: print 'my_norm_opt: my optimization end ---'

"""
Loads background file and assigns unit response matrix.

Capabilities for loading and storing previously fitted background models.
"""
class BackgroundStorage(object):
	def __init__(self, backgroundfilename, i, load=False):
		self.backgroundfilename = backgroundfilename
		if load:
			load_pha(i, self.backgroundfilename)
		self.backgroundparamsfile = backgroundfilename + '_bkgparams.json'
		print 'BackgroundStorage: for background model params of ID=%s, will use "%s" as storage' % (i, self.backgroundparamsfile)
		self.i = i
		self.load_rsp()
	def load_rsp(self):
		i = self.i
		copy_data(i,1000+2)
		unit_arf = get_bkg_arf(1000+2)
		unit_arf.specresp = 0.*unit_arf.specresp + 1.0 # * unit_arf.specresp.mean()
		self.bunitrsp = get_response(1000+2,bkg_id=1)
		delete_data(1000+2)
	def load_bkg_model(self):
		i = self.i
		m = get_bkg_model(i)
		bkg_model = json.load(file(self.backgroundparamsfile, 'r'))
		bkg_pars = bkg_model['params']
		for p in m.pars:
			print "set_my_model: \tbkg[%s] = %e" % (p.fullname, bkg_pars[p.fullname])
			if bkg_pars[p.fullname] > p.max or bkg_pars[p.fullname] < p.min:
				print 'set_my_model: \tWARNING: ignoring stored parameter value for', [p.fullname, p.val, p.min, p.max]
				continue
			p.val = bkg_pars[p.fullname]
		return [p.val for p in m.pars]
	
	def store_bkg_model(self, stats):
		i = self.i
		m = get_bkg_model(i)
		params = dict([(p.fullname, p.val) for p in m.pars])
		oldstats = 1e300

		try:
			prev_model = json.load(file(self.backgroundparamsfile, 'r'))
			oldstats = prev_model['stats']
		except Exception as e:
			print 'store_bkg_model: could not check previously stored model, perhaps this is the first', e
		if stats < oldstats + 0.02:
			set_analysis(i, "energy", "counts")
			p = get_bkg_fit_plot(i)
			with file(self.backgroundparamsfile, 'w') as f:
				json.dump(dict(params=params, stats=stats,
					plot=dict(x=p.dataplot.x.tolist(), ydata=p.dataplot.y.tolist(), ymodel=p.modelplot.y.tolist())), 
					f, indent=4)
		else:
			print 'store_bkg_model: ERROR: refusing to store worse model!', stats, oldstats
		names = [p.fullname for p in m.pars]
		values = [p.val for p in m.pars]
		return names, values


class MultiFitter(object):
	def __init__(self, filename, backgroundmodel):
		self.ids = [l.strip() for l in open(filename).readlines()]
		self.bkgs = []
		self.load()
		self.backgroundmodel = backgroundmodel
	def load(self):
		print 'load_bkg_all: loading...'
		for i in self.ids:
			b = BackgroundStorage(i, i, load=True)
			bm = self.backgroundmodel(b)
			self.bkgs[i] = bm
			assert i in list_data_ids(), list_data_ids()
		print 'load_bkg_all: done'
	def store(self, i):
		self.bkgs[i].set_model()
		stats = my_bkg_stat(i)
		self.bkgs[i].storage.store_bkg_model(newstats)
		
	def load_and_fit_all(self):
		for part in range(int(numpy.ceil(len(self.ids) / 10.))):
			batchids = self.ids[part*10:part*10+10]
			for i in batchids:
				self.bkgs[i].set_model()
			self.load_and_fit_batch(batchids)
			for i in batchids:
				self.store(i)
			self.improve_freeshape()
			for i in batchids:
				self.store(i)
		
	def load_and_fit_batch(self, batchids, reinit=True, verbose=False):
		"""
		joint fit of the variables in the batch to get better 
		sensitivity
		"""
		ids = batchids
		print "load_and_fitall: loading ...."
		print ids

		print "load_and_fitall: preparing"
		set_filter()
		
		# sorting from high-count to low-count, get 10 highest
		ids = sorted(ids, key=lambda i: get_bkg(i).counts.sum(), reverse=True)
		selected = ids[:10]
		
		# rough fit first
		set_method_opt('ftol', 0.1)
		
		def plot(i):
			if verbose: 
				print 'load_and_fitall: plotting %s ... ' % i
				plot_bkg_fit_resid(i)
				print 'load_and_fitall: plotting %s ... done' % i
		
		print "load_and_fitall: fitting first ...."
		i = selected[0]
		if True:
			self.bkgs[i].set_model(prev='init' if reinit else i, optimize=True)
			print 'load_and_fitall: first, optimized'
			plot(i)
			fit_bkg(i)
			print 'load_and_fitall: first, fitted'
			plot(i)
			self.store(i)
	
		def fitall(name):
			print "fitall: fitting %s ...." % name
			fit_bkg()
			print "fitall: fitting %s .... done" % name
		print "load_and_fitall: loading rest ...."
		prev = i
		for i in selected:
			if True:
				self.bkgs[i].set_model(prev=prev, optimize=True)
				print 'load_and_fitall: rest, optimized', i
				fit_bkg(i)
				print 'load_and_fitall: rest, fitted', i
				plot(i)
				self.store(i)
			prev = i
		fitall("rest")
	
		set_stat('cstat')
		#set_method('neldermead')

		#set_method_opt('ftol', 0.0001)
		print "load_and_fitall: fitting refined...."
		softend.fwhm.thaw()
		softend.pos.thaw()
		softsoftend.fwhm.thaw()
		softsoftend.pos.thaw()
		for p in softboxes + lines:
			print "load_and_fitall: \tthawing", p.pos.fullname
			p.pos.thaw()
		for i in selected:
			const1d("contlevel%s" % i).c0.thaw()

		fitall("refined, line positions free")
		plot(selected[-1])

		print "load_and_fitall: fit all individually, but fixing shape parameters"
		for c in boxes + lines:
			for p in c.pars:
				print "load_and_fitall: \tfreezing", p.fullname
				p.freeze()
		# soft end is still thawed
	
		for i in selected:
			delete_bkg_model(i)

		prev = None
		for i in ids:
			delete_bkg_model(i)
			if True:
				self.bkgs[i].set_model(prev=selected[0], optimize=True)
				fit_bkg(i)
				plot(i)
				self.store(i)
			prev = i
			fitall("with lines and soft end")
			plot(i)
			self.store(i)
			delete_bkg_model(i)

		print "load_and_fitall: done"
		return ids
	
	def improve_freeshape(self, batchids):
		"""
		unlink batches and try to further improve individual ids
		"""
		
		ids = batchids
		print 'improve_freeshape: start...'
		for i in ids:
			self.bkgs[i].set_model()
			self.bkgs[i].storage.load_bkg_model()
			# freeze all params except soft shape
			for p in get_bkg_model(i).pars:
				if p.name != 'c0':
					#print 'freezing %s' % p.fullname
					p.freeze()
				else:
					#print 'thawing %s' % p.fullname
					p.thaw()
			for p in gauss1d.softsoftend.pars + gauss1d.softend.pars:
				if p.name != 'ampl':
					#print 'thawing %s' % p.fullname
					p.thaw()
			set_filter()
			stat = my_bkg_stat(i)
			print 'improve_freeshape: current stat of %s: %f' % (i, stat)
			#plot_bkg_fit_resid(i)
			fit_bkg(i)
			newstat = my_bkg_stat(i)
			print 'improve_freeshape: stat improved: %.2f --> %.2f (better: %s, much: %s)' % (newstat, stat, newstat < stat, newstat + 0.3 < stat)
			#plot_bkg_fit_resid(i)
			#print 'press ENTER >>',
			#sys.stdin.readline()
			if newstat + 0.01 < stat or True:
				print 'improve_freeshape: saving improvement'
				self.store(i)
		print 'improve_freeshape: done'

class SingleFitter(object):
	def __init__(self, id, filename, backgroundmodel):
		"""
		file that has the background in it
		"""
		self.id = id
		print 'SingleFitter(for ID=%s, storing to "%s")' % (id, filename)
		b = BackgroundStorage(filename, id)
		self.bm = backgroundmodel(b)
		try:
			self.bm.storage.load_bkg_model()
		except IOError:
			pass
	def store(self):
		i = self.id
		print 'SingleFitter::store()'
		self.bm.set_model(optimize=False)
		print 'SingleFitter::store() stats'
		newstats = my_bkg_stat(i)
		print 'SingleFitter::store() bm store'
		self.bm.storage.store_bkg_model(newstats)
		print 'SingleFitter::store() done'
	def tryload(self):
		try:
			self.bm.storage.load_bkg_model()
			return True
		except:
			return False
		
	def fit(self, reinit=True, verbose=False):
		self.bm.set_filter()
		i = self.id
		# rough fit first
		set_method_opt('ftol', 0.1)
		
		def plot(i):
			if verbose: 
				print 'load_and_fitall: plotting %s  (stat: %.3f)... ' % (i, my_bkg_stat(i))
				plot_bkg_fit_resid(i)
				print 'load_and_fitall: plotting %s ... done' % i
		
		self.bm.set_model(prev='init' if reinit else i, optimize=True)
		print 'fit: optimized'
		plot(i)
		fit_bkg(i)
		print 'fit: optimized'
		set_method_opt('ftol', 0.001)
		fit_bkg(i)
		print 'fit: fitted'
		plot(i)
		self.store()
		print "fit: done"

"""
Background model for Chandra, as for the CDFS.

Uses a flat continuum, two broad gaussians and 8 narrow instrumental lines.
"""
class ChandraBackground(object):
	def __init__(self, storage):
		centers = [1.486, 1.739, 2.142, 7.478, 8.012, 8.265, 8.4939, 9.7133]
		continuum, softsoftend, softend, line1, line2, line3, line4, line5, line6, line7, line8 = (box1d.continuum, gauss1d.softsoftend, gauss1d.softend, gauss1d.line1, gauss1d.line2, gauss1d.line3, gauss1d.line4, gauss1d.line5, gauss1d.line6, gauss1d.line7, gauss1d.line8)
		box2 = gauss1d.softsoftend
		box3 = gauss1d.softend

		self.lines = [line1, line2, line3, line4, line5, line6, line7, line8]
		self.abslines = [line5, line6, line7]
		self.linelines = [line1, line2, line3, line4, line8]
		#lines = linelines + abslines
		self.boxes = [continuum]

		self.softboxes = [softend, softsoftend]
		self.plboxes = self.boxes + self.softboxes
		self.init_shape()
		self.storage = storage
	def init_shape(self):
		print 'creating Chandra background model'
		for l, c in zip(self.lines, self.centers):
			l.pos = c
			l.pos.min = c - 0.1
			l.pos.max = c + 0.1

		for l in self.lines:
			l.ampl = 2000
			l.ampl.min = 1e-8
			l.ampl.max = 1e12
			l.fwhm = 0.02
			l.fwhm.min = 0.002
			l.pos.freeze()

		for l in self.abslines:
			l.fwhm.max = 0.4

		for l in self.linelines:
			l.fwhm.max = 0.1

		# narrow soft end
		softsoftend.pos = 0.3
		softsoftend.pos.min = 0
		softsoftend.pos.max = 0.6
		softsoftend.pos.freeze()
		softsoftend.fwhm = 0.5
		softsoftend.fwhm.min = 0.2
		softsoftend.fwhm.max = 0.7
		softsoftend.fwhm.freeze()

		# wide gaussian
		softend.pos = 0
		softend.pos.max = 1
		softend.pos.min = -1
		softend.pos.freeze()
		softend.fwhm = 3.8
		softend.fwhm.min = 2
		softend.fwhm.max = 7
		softend.fwhm.freeze()

		for b in self.plboxes:
			b.ampl.val = 1
			b.ampl.freeze()
		changepoints = [0.2, 0.8, 1.3, 2.5, 8.2, 8.4, 8.75, 12]
		changepoints = [0., 12]

		for b,clo,chi in zip(self.boxes, changepoints[:-1], changepoints[1:]):
			b.xlow = clo
			b.xhi = chi
			b.xlow.freeze()
			b.xhi.freeze()
			b.ampl.min = 1e-8
			b.ampl.max = 1e8
			b.ampl.val = 1
		
	def set_zero(self):
		for l in self.lines + self.plboxes:
			l.ampl.min = 0
			l.ampl.val = 0
	
	"""
	range over which this model is valid
	"""
	def set_filter(self):
		ignore(None, 0.4)
		ignore(9.8, None)
		notice(0.4, 9.8)

	def set_model(self, withsoft=True, withlines=True, prev=None, optimize=False):
		"""
		sets up model and guesses good values (if optimize=True)
		
		withsoft:  include soft broad gaussians
		withlines: include instrumental lines
		prev:      start from the parameters of another ID 
		           if 'init', start fresh
		"""
		i = self.storage.i
		j = i
		print 'set_my_model: setting model for %s ...' % j
		contlevel = const1d("contlevel%s" % j)
		#linelevel = const1d("linelevel%s" % j)
		#abslevel = const1d("abslevel%s" % j)
		softlevel = const1d("softlevel%s" % j)
		softsoftlevel = const1d("softsoftlevel%s" % j)
		contlevel.c0.min = 1e-6
		softlevel.c0.min = 1e-4
		softsoftlevel.c0.min = 1e-4
		contlevel.c0.max = 1e10
		softlevel.c0.max = 1e10
		softsoftlevel.c0.max = 1e10
		if prev is not None:
			if prev == 'init':
				print 'set_my_model: \tinitializing level values'
				contlevel.c0.val = 1e-3
				#linelevel.c0.val = 1e11
				#abslevel.c0.val  = 1e11
				softlevel.c0.val = 1e1
				softsoftlevel.c0.val = 1e1
			else:
				print 'set_my_model: \ttaking level values from %s...' % prev
				contlevel.c0.val = const1d("contlevel%s" % prev).c0.val
				#linelevel.c0.val = const1d("linelevel%s" % prev).c0.val
				#abslevel.c0.val = const1d("abslevel%s" % prev).c0.val
				softlevel.c0.val = const1d("softlevel%s" % prev).c0.val
				softsoftlevel.c0.val = const1d("softsoftlevel%s" % prev).c0.val
		
		print 'set_my_model: \tputting model together...'
		print 'set_my_model: \t\tadding continuum...'
		bg_model = continuum * contlevel
		bunitrsp = self.storage.bunitrsp
		set_bkg_model(i, bunitrsp(bg_model))
		set_bkg_full_model(i, bunitrsp(bg_model))
		if optimize:
			ignore(None, 2.5)
			ignore(7, None)
			print 'set_my_model: \t\tzooming to %.1f %.1f' % (2.5, 7)
			my_norm_opt(i, [contlevel.c0])
			self.set_filter()
		
		if withsoft:
			print 'set_my_model: \t\tadding soft end...'
			bg_model += (softend * softlevel + softsoftend * softsoftlevel) * contlevel
			delete_bkg_model(i)
			set_bkg_model(i, bunitrsp(bg_model))
			set_bkg_full_model(i, bunitrsp(bg_model))
			if optimize: 
				ignore(None, 0.4)
				ignore(2., None)
				print 'set_my_model: \t\tzooming to %.1f %.1f' % (0.4, 2.)
				my_norm_opt(i, [softsoftlevel.c0, softlevel.c0, softsoftlevel.c0])
				self.set_filter()
		if withlines:
			print 'set_my_model: \t\tadding lines...'
			for l in linelines + abslines:
				bg_model += l * contlevel
			#bg_model += eval('+'.join([c.name for c in linelines])) * contlevel
			delete_bkg_model(i)
			set_bkg_model(i, bunitrsp(bg_model))
			set_bkg_full_model(i, bunitrsp(bg_model))
			if optimize: 
				for l in linelines + abslines:
					if l.ampl.frozen: continue
					print 'set_my_model: \t\tzooming to %.1f %.1f' % (l.pos.val - 3*l.fwhm.val, l.pos.val + 3*l.fwhm.val)
					ignore(None, l.pos.val - max(3*l.fwhm.val, 0.2))
					ignore(l.pos.val + max(3*l.fwhm.val, 0.2), None)
					my_norm_opt(i, [l.ampl])
					self.set_filter()
	
		for p in get_bkg_model(i).pars:
			print 'set_my_model: \t%15s\t%e\t%e\t%e' % (p.fullname, p.val, p.min, p.max)



"""
Background model for Chandra, as for the CDFS.

Uses a flat continuum, two broad gaussians and 8 narrow instrumental lines.
"""
class SwiftXRBBackground(object):
	def __init__(self, storage):
		self.storage = storage
		self.init_shape()
		
	def init_shape(self):
		i = self.storage.i
		print 'setting up Swift/XRB background for ', i
		self.bg_model = (1 - box1d.dip) * (xsbknpower.pbknpl + gauss1d.g1 + gauss1d.g2 + gauss1d.g3)
		bunitrsp = self.storage.bunitrsp
		set_bkg_model(i, self.bg_model)
		set_bkg_full_model(i, bunitrsp(self.bg_model))

		pbknpl.BreakE.min = 0.2
		pbknpl.BreakE.max = 5
		pbknpl.BreakE.val = 2
		pbknpl.PhoIndx1.max = 4
		pbknpl.PhoIndx2.max = 4
		pbknpl.PhoIndx1.min = 1
		pbknpl.PhoIndx2.min = 1
		pbknpl.PhoIndx1.val = 2
		pbknpl.PhoIndx2.val = 1.5
		pbknpl.norm.min = 1e-10
		pbknpl.norm.max = 1
		pbknpl.norm.val = 0.004
		
		lines = [(0.1, 0.7, 1.1), (2, 2.15, 2.5), (1, 1.2, 1.4)]
		

		for g, (lo, mid, hi) in zip([g1, g2, g3], lines):
			g.pos.val = mid
			g.pos.min = lo
			g.pos.max = hi
			g.fwhm.val = 0.2
			g.fwhm.max = 1
			g.fwhm.min = 0.01
			g.ampl.val = 0.01
			g.ampl.max = 1
			g.ampl.min = 1e-10

		box1d.dip.xlow = 2
		box1d.dip.xhi = 3
		box1d.dip.xlow.min = 1.75
		box1d.dip.xlow.max = 2.25
		box1d.dip.xhi.min = 2.75
		box1d.dip.xhi.max = 3.25
		box1d.dip.ampl.val = 0.5
		box1d.dip.ampl.min = 1e-3
		box1d.dip.ampl.max = 1 - 1e-3
		
	"""
	range over which this model is valid
	"""
	def set_filter(self):
		print 'setting filter 0.3-5keV'
		ignore(None, 0.3)
		ignore(5, None)
		notice(0.3, 5)

	def set_model(self, prev=None, optimize=False):
		"""
		sets up model and guesses good values (if optimize=True)
		
		prev:      start from the parameters of another ID 
		           if 'init', start fresh
		"""
		i = self.storage.i
		j = i
		if prev is not None:
			if prev == 'init':
				print 'set_my_model: \tinitializing level values'
				self.init_shape()
			else:
				print 'set_my_model: \ttaking level values from %s...' % prev
				print '       prev= feature is not supported by SwiftXRBBackground model.'
		
		print 'set_my_model: \tputting model together...'
		bunitrsp = self.storage.bunitrsp
		for model in [2, 3, 4, 5]:
			print 'applying background model level %d' % model
			self.bg_model = xsbknpower.pbknpl
			if model > 1:
				self.bg_model = self.bg_model + gauss1d.g1 
			if model > 2:
				self.bg_model = self.bg_model + gauss1d.g2
			if model > 3:
				self.bg_model = self.bg_model + gauss1d.g3
			if model > 4:
				self.bg_model = (1 - box1d.dip) * self.bg_model

			set_bkg_model(i, self.bg_model)
			set_bkg_full_model(i, bunitrsp(self.bg_model))
			if optimize:
				self.set_filter()
				print 'fitting background model level %d (1/2)' % model
				plot_bkg_fit_resid(i)
				set_stat(bxaroughstat)
				print 'fitting ...'
				fit_bkg()
				print 'fitting done'
				set_stat('cstat')
				plot_bkg_fit_resid(i)
				print 'fitting background model level %d (2/2)' % model
				plot_bkg_fit_resid(i)
				fit_bkg()
				plot_bkg_fit_resid(i)
				print 'fitting background model level %d (done)' % model
		
		for p in self.bg_model.pars:
			print 'set_my_model: \t%15s\t%e\t%e\t%e' % (p.fullname, p.val, p.min, p.max)
		

__dir__ = [SwiftXRBBackground, ChandraBackground, SingleFitter, MultiFitter, BackgroundStorage, my_norm_opt, my_bkg_stat]

