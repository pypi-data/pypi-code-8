# stevedore/example/setup.py
from setuptools import setup


setup(
    name='mkv',
    version='0.1',

    description='Merge and split mkv files usign mkvextract and mkvmerge.',

    author='Nekmo',
    author_email='contacto@nekmo.com',

    url='https://bitbucket.org/Nekmo/python-mkv',
    
    download_url='https://bitbucket.org/Nekmo/nekbot.protocols.irc/get/default.tar.gz',

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Multimedia :: Video',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    platforms=['any'],

    scripts=[],

    packages=['mkv'],

    keywords=['python', 'mkv', 'extract', 'merge', 'join'],


    zip_safe=False,
)