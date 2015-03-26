from setuptools import setup, find_packages

version = '3.0.1'

setup(name='plone.app.controlpanel',
      version=version,
      description="Formlib-based controlpanels for Plone.",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='plone controlpanel formlib',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.controlpanel',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'plone.app.form',
        'plone.app.vocabularies',
        'plone.app.workflow',
        'plone.fieldsets',
        'plone.memoize',
        'plone.protect',
        'plone.locking',
        'zope.annotation',
        'zope.cachedescriptors',
        'zope.component',
        'zope.event',
        'zope.formlib',
        'zope.i18n',
        'zope.interface',
        'zope.ramcache',
        'zope.publisher',
        'zope.schema',
        'zope.site',
        'zope.testing',
        'Acquisition',
        'Products.CMFPlone',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.PlonePAS',
        'Products.PortalTransforms',
        'Products.statusmessages',
        'Zope2>=2.13.0',
        'ZODB3',
      ],
      extras_require={
        'test': [
        ]
      }
      )
