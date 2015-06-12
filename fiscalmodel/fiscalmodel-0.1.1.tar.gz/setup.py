from setuptools import setup, find_packages


setup(
    name='fiscalmodel',
    version='0.1.1',
    description="Reference data for fiscal data classification",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7'
    ],
    keywords='reference data budgets spending revenue fiscal',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/pudo/fiscalmodel',
    license='MIT',
    packages=['fiscalmodel'],
    include_package_data=True,
    package_data={
        'fiscalmodel': ['data/*.csv', 'data/*.json']
    },
    zip_safe=True,
    install_requires=[
        'six',
        'normality'
    ],
    tests_require=[],
    test_suite='test',
    entry_points={
    }
)
