from setuptools import setup

setup(
    name='Flask-Crossdomain2',
    version='0.1.0',
    description='Module for enabling cross-site/cross-origin HTTP requests on Flask app endpoints.',
    url='http://github.com/onenameio/flask-crossdomain',
    author='Onename',
    author_email='hello@onename.com',
    license='MIT',
    py_modules=['flask_crossdomain'],
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
