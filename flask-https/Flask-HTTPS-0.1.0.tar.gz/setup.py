from setuptools import setup, find_packages

setup(
    name='Flask-HTTPS',
    version='0.1.0',
    url='https://github.com/onenameio/flask-https',
    license='MIT',
    author='Onename',
    author_email='hello@onename.com',
    description='Make HTTPS required on any Flask app',
    keywords='https ssl tls',
    py_modules=['flask_https'],
    zip_safe=False,
    install_requires=[
        'Flask>=0.10.1'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
