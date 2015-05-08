from setuptools import setup
#from distutils.core import setup # distutils no longer recommended

setup(
    name='argus',
    version='0.0.4',
    packages=['argus'],
    scripts=['bin/argus_audio_sync2','bin/argus_initial_calibrate',
             'bin/argus_refine','bin/argus_detect_patterns',
             'bin/argus_undistort','bin/argus_simplified',
             'bin/argus_summarize'],
 
    # dependencies
    install_requires=[
        #"cv2 >= 2.4.9", # setuptools doesn't handle this gracefully see below 
        "numpy >= 1.9.1",
        "pandas >= 0.15.2",
        "scipy >= 0.15.1",
    ],
    dependency_links=[
        #'http://opencv.org/downloads.html',
        'http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.9/opencv-2.4.9.zip/download',
        # should add avconv or ffmpeg to this list depending
    ],
    
    # metadata for PyPI
    author='Brandon Jackson and Dennis Evangelista',
    author_email='devangel77b@gmail.com',
    description='Helper routines for using multiple, inexpensive calibrated and synchronized cameras for 3D scientific use.',
    license = 'GNU GPLv3',
    keywords = 'calibration, camera, camera calibration, photogrammetry',
    url = 'https://bitbucket.org/devangel77b/argus',

    # could also include long_description, download_url, classifiers, etc.
    long_description=file('README.md','r').read(),
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Operating System :: OS Independent',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Multimedia :: Graphics',
                 'Topic :: Multimedia :: Graphics :: 3D Modeling',
                 'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
                 'Topic :: Multimedia :: Video',
                 'Topic :: Scientific/Engineering'],
)
