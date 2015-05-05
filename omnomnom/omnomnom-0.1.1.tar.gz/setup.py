from setuptools import setup, find_packages

requires = [
    'nanomsg',
    'futures'
]

test_requires = [
    'mock',
    'nose',
    'coverage'
]

setup(
    name='omnomnom',
    install_requires=requires,
    tests_require=test_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="nose.collector",
    version='0.1.1',
    description=(
        'Microservice framework with reasonable defaults'
        'using nanomsg under the hood.'
    ),
    author='jnosal',
    author_email='jacek.nosal@outlook.com',
    url='https://github.com/jnosal/omnomnom',
    keywords=[
        'nanomsg', 'microservices'
    ],
    entry_points={
        'console_scripts': [
            'omnomnom-worker = omnomnom.runners.run_worker:main',
            'omnomnom-queue = omnomnom.runners.run_queue:main',
            'omnomnom-service = omnomnom.runners.run_service:main'
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
