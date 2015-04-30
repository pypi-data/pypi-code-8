from distutils.core import setup

setup(
    name = 'robotframework-uiautomatorlibrary',
    packages = ['uiautomatorlibrary'],
    version = '0.4',
    author='ming060',
    author_email = 'lym060@gmail.com',
    url = 'https://github.com/ming060/robotframework-uiautomatorlibrary',
    license='MIT',
    platforms='any',
    description = 'Robot Framework Android Test Library Based on Python uiautomator',
    long_description = 
    """
    This is a test library for `Robot Framework <https://pypi.python.org/pypi/robotframework>`_ to bring keyword-driven testing to Android apps..

    It uses by using `Python uiautomator <https://pypi.python.org/pypi/uiautomator>`_ internally.
    """,
    install_requires = [
                        'uiautomator >= 0.1.30'
                        ],
    classifiers  = [
                    'Development Status :: 3 - Alpha',
                    'License :: OSI Approved :: MIT License',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Operating System :: POSIX :: Linux',
                    'Programming Language :: Python :: 2.7',
                    'Topic :: Software Development :: Testing'
                    ]
)