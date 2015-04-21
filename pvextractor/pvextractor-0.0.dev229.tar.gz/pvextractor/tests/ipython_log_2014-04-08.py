########################################################
# Started Logging At: 2014-04-08 14:33:52
########################################################

########################################################
# # Started Logging At: 2014-04-08 14:33:54
########################################################
import pyregion
r = pyregion.open('data/tests.reg'
)
r
r[-1]
r[-1].attr
hdu = fits.open('/Users/adam/work/w51/12co_final_cube_c_supersampledh2cogrid.fits')
hdu[0]
w = WCS(hdu[0].header)
wcs
w = wcs.WCS(hdu[0].header)
endpoints = ([50,1],[49,2])
wcs=w
pixendpoints = wcs.wcs_world2pix([[x,y,wcs.wcs.crval3] 
                                  for x,y in endpoints], 0)
w.wcs.crval
pixendpoints = wcs.wcs_world2pix([[x,y,wcs.wcs.crval[2]] 
                                  for x,y in endpoints], 0)
pixendpoints
pixendpoints.shape
w.wcs.cd
w.wcs.pc
w.wcs.pv
x = 5*u.arcsec
x.unit
x.unit.is_equivalent(u.arcsec)
wcs.wcs.get_cdelt()
wcs.wcs.get_cdelt() * wcs.wcs.get_pc()
cdelt = np.matrix(wcs.get_cdelt())
pc = np.matrix(wcs.get_pc())
scale = np.array(cdelt * pc).diag
get_ipython().magic(u'paste')
cdelt = np.matrix(wcs.wcs.get_cdelt())
pc = np.matrix(wcs.wcs.get_pc())
scale = np.array(cdelt * pc).diag
scale = np.array(cdelt * pc).diagonal()
scale
scale
wcs.wcs.get_pc()
cdelt
cdelt
pc
cdelt * pc
wcs.get_axis_types()
((10*u.deg/u.radian)*400*u.pc).to(u.pc)
