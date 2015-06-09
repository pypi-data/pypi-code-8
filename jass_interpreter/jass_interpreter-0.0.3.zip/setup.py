from distutils.core import setup

setup(
    name='jass_interpreter',
    version='0.0.3',
    packages=['jass_interpreter', 'jass_runtime'],
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

        now with a stub implementation of the standard library (3 functions or so..)
        not very useful yet, but can at least poke at it :)


    ''',
    install_requires=[
        'pytest',
        'parsimonious',
        'docopt',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],
    keywords="jass jass2 vjass compiler interpreter war3 warcraft Waffle",
)
