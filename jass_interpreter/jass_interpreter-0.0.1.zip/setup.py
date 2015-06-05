from distutils.core import setup

setup(
    name='jass_interpreter',
    version='0.0.1',
    packages=['jass_interpreter'],
    #package_dir={'': 'jass_interpreter'},
    url='http://example.com',
    license='',
    author='Joonas Liik',
    author_email='liik.joonas@gmail.com',
    description='''
        A simple and very-much half baked cross compiler from jass2 to python3.4
    ''',

    # reStructuredText
    long_description='''
        Jass Interpreter
        ================

        .. is a script that parses a script in JASS2 format (think warcraft 3 scripting) and translates it to python3.4 code


    ''',
    install_requires=[
        'pytest',
        'parsimonious',
        'docopt'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',


    ],
)
