from distutils.core import setup

setup(
    name='planarradpy',
    version='0.0.1-1',
    packages=['planarradpy.gui', 'planarradpy.log', 'planarradpy.docs', 'planarradpy.tests', 'planarradpy.inputs',
              'planarradpy.inputs.iop_files', 'planarradpy.inputs.sky_files', 'planarradpy.inputs.phase_files',
              'planarradpy.inputs.bottom_files', 'planarradpy.inputs.surface_files', 'planarradpy.outputs',
              'planarradpy.scripts', 'planarradpy.libplanarradpy'],
    url='https://marrabld.github.io/planarradpy/',
    license='GPL',
    scripts=['planarradpy/planarrad.run'],
    include_package_data=True,
    author='Dan Marrable',
    author_email='marrabld+planarradpy@gmail.com',
    description='Tool for batch running PlanarRad across multiple CPUs', requires=['PyQt4'],
)
