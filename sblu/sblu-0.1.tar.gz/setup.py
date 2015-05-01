from setuptools import setup
import sblu


with open("requirements.txt", "r") as requirements_file:
    requirements = [x.strip() for x in requirements_file.readlines()]

scripts = (
    'scripts/cl_load_job',
    'scripts/pdbclean',
    'scripts/pdbsplitsegs',
    'scripts/srmsd',
    'scripts/cluspro_local.py',
    'scripts/cluster.py',
    'scripts/ftrmsd.py',
    'scripts/pwrmsd.py',
)

setup(
    name="sblu",
    version=sblu.__version__,
    packages=['sblu'],
    description="Library for munging data files from ClusPro/FTMap/etc.",
    license="MIT",

    author="Bing Xia",
    author_email="sixpi@bu.edu",

    install_requires=requirements,

    scripts=scripts,

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ]
)
