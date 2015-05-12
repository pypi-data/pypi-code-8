from setuptools import setup

setup(name='TheCannon',
        version='0.2.4',
        description='Data-driven stellar parameters and abundances from spectra',
        url='http://github.com/annayqho/TheCannon',
        author='Anna Y. Q. Ho',
        author_email='annayqho@gmail.com',
        license='MIT',
        packages=['helpers', 'example_DR10'],
        package_dir={
            'helpers': 'TheCannon/helpers', 
            'example_DR10': 'TheCannon/example_DR10'},
        package_data={'helpers': ['triangle/*.py']},
        zip_safe=False)
