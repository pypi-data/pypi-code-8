from setuptools import setup, find_packages

setup(
    name='gaetasks',
    version='0.0.2',
    description='Better google appengine deferred lib',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='appengine gae defer deferred',
    author='Konrad Rotkiewicz',
    author_email='konrad.rotkiewicz@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
