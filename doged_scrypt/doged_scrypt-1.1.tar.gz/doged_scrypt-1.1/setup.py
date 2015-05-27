from distutils.core import setup, Extension

doged_scrypt_module = Extension('doged_scrypt',
                              sources=['./scryptmodule.c',
                                       './scrypt.c'],
                              include_dirs=['./doged_scrypt'])

setup(name='doged_scrypt',
      version='1.1',
      description='Bindings for scrypt proof of work used by DogecoinDark',
      ext_modules=[doged_scrypt_module])
