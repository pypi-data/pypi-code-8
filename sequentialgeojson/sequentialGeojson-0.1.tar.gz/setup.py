from setuptools import setup

def readme():
    with open('readme.rst') as f:
        return f.read()

setup(name='sequentialGeojson',
    version='0.1',
    description='A python generator object that provides sequential access to features inside a FeatureCollection of a GeoJson file.',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3.2',
    ],
    keywords='json sequential generator geojson',
    url='https://github.com/scubbx/sequential-geojson',
    author='Markus Mayr',
    author_email='markusmayr@gmx.net',
    license='MIT',
    packages=['sequentialGeojson'],
    zip_safe=False)
