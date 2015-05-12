from setuptools import setup

setup(name='TheCannon',
        version='0.2.2',
        description='Data-driven stellar parameters and abundances from spectra',
        url='http://github.com/annayqho/TheCannon',
        author='Anna Y. Q. Ho',
        author_email='annayqho@gmail.com',
        license='MIT',
        packages=['helpers'],
        package_dir={'helpers': 'TheCannon/helpers'},
        package_data={'helpers': ['triangle/*.py']},
        zip_safe=False)
