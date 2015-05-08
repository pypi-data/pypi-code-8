import os
from distutils.core import setup


long_description = 'Provides packaging and publishing tools for ArcGIS python toolboxes'


if os.path.exists('README.md'):
    try:
        # Use pypandoc to convert markdown readme to reStructuredText as required by pypi
        # Requires pandoc to be installed.  See: http://johnmacfarlane.net/pandoc/installing.html
        from pypandoc import convert
        read_md = lambda f: convert(f, 'rst', format='md')
        long_description = read_md('README.md')
    except:
        pass


setup(
    name='ags_tool_deploy',
    version='0.1.1',
    description='Provides packaging and publishing tools for ArcGIS python toolboxes',
    long_description=long_description,
    packages=['ags_tool_deploy'],
    requires=['lxml', 'click'],
    url='https://bitbucket.org/databasin/ags_tool_deploy',
    license='BSD',
    author='Data Basin',
    author_email='databasin@consbio.org',
    keywords='arcgis ags'
)
