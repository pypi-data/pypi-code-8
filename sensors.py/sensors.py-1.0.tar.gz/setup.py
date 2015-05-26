from setuptools import setup, find_packages

setup(
    name="sensors.py",
    version="1.0",
    description="python bindings using ctypes for libsensors3",
    url="https://github.com/paroj/sensors.py",
    author="Pavel Rojtberg",
    license="LGPLv2",
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    py_modules=["sensors"]
)
