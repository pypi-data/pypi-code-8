from distutils.core import setup
import pydoc

import clictk

long_desc = pydoc.getdoc(clictk)

setup(
    name='pyclictk',
    version=clictk.__version__,
    packages=['clictk'],
    provides=['clictk'],
    url='http://github.com/CognitionGuidedSurgery/pyclictk',
    license='LGPLv3',
    author='Alexander Weigl',
    author_email='uiduw@student.kit.edu',
    description='Python Support Common Toolkit\'s (CTK) Command Line Interface (CLI)',
    long_description=long_desc,
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console"
    ]
)
