from setuptools import setup


version = '0.0.1'


setup(
    author='Charlie Denton',
    author_email='charlie@meshy.co.uk',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
    ],
    description='Represents and converts quantities of measurement.',
    license='MIT',
    name='meshy-quantities',
    packages=['quantities'],
    py_modules=['quantities'],
    url='https://bitbucket.org/meshy/meshy-quantities',
    version=version,
)
