import os
import platform
from setuptools import setup, Extension, find_packages


top_dir = os.path.dirname(os.path.realpath(__file__))
inc_dir = os.path.join(top_dir, "include")
lib_dir = os.path.join(top_dir, "lib")
libcrm114_obj = [
    os.path.join(top_dir, "lib", f) for f in (
        "crm114_base.c",
        "crm114_markov.c",
        "crm114_markov_microgroom.c",
        "crm114_bit_entropy.c",
        "crm114_hyperspace.c",
        "crm114_svm.c",
        "crm114_svm_lib_fncts.c",
        "crm114_svm_quad_prog.c",
        "crm114_fast_substring_compression.c",
        "crm114_pca.c",
        "crm114_pca_lib_fncts.c",
        "crm114_matrix.c",
        "crm114_matrix_util.c",
        "crm114_datalib.c",
        "crm114_vector_tokenize.c",
        "crm114_strnhash.c",
        "crm114_util.c",
        "crm114_regex_tre.c",
    )
]
if platform.uname()[0] in ['Darwin', 'BSD']:
    libcrm114_obj.insert(0, 'lib/memstream.c')
    libcrm114_obj.insert(0, 'lib/fmemopen.c')

pycrm114_module = Extension('pycrm114._binding',
                            sources=libcrm114_obj + ['pycrm114/pycrm114_module.c'],
                            include_dirs=[inc_dir],
                            library_dirs=[lib_dir],
                            runtime_library_dirs=[lib_dir],
                            libraries=['tre'],
                            extra_compile_args=['-std=c99', '-g', '-pedantic', '-Wall', '-Wextra', '-Wpointer-arith',
                                                '-Wstrict-prototypes', '-fpic'])

requirements = filter(None, open(
    os.path.join(top_dir, 'requirements', 'main.txt')).read().splitlines())

import versioneer

versioneer.versionfile_source = "pycrm114/_version.py"
versioneer.versionfile_build = "pycrm114/version.py"
versioneer.tag_prefix = ""
versioneer.parentdir_prefix = "pycrm114-"


setup(
    name='pycrm114',
    version=versioneer.get_version(),
    description='Python interface to libcrm114',
    long_description=open('README.rst').read() + open('HISTORY.rst').read(),
    author='Prashanth Mundkur',
    author_email='prashanth.mundkur at gmail.com',
    maintainer='Ali-Akber Saifee',
    maintainer_email='ali at indydevs.org',
    url='https://github.com/alisaifee/pycrm114',
    license=open('LICENSE.txt').read(),
    classifiers=[k for k in open('CLASSIFIERS').read().split('\n') if k],
    install_requires=requirements,
    ext_modules=[pycrm114_module],
    packages=find_packages(exclude=["tests*"]),
    cmdclass=versioneer.get_cmdclass(),
)
