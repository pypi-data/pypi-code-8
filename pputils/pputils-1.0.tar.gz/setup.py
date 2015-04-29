from setuptools import setup, find_packages
setup(
    name = "pputils",
    version=1.0,
    description="utils by python",
    author='Peng Jun',
    license='PJ',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': [
    'pputils = pputils.main:main']},
        )
