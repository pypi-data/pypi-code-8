from setuptools import setup, find_packages

setup(name="myls",
      version="0.0.1",
      description='UNIX command ls python wrapper',
      long_description='',
      url="https://github.com/chkumar/myls.git",
      author="Chandan Kumar",
      author_email="chandankumar.093047@gmail.com",
      license="GPL",
      # packages=['myls'],
      classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',

      # Indicate who your project is intended for
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',

      # Pick your license as you wish (should match "license" above)
      'License :: OSI Approved :: MIT License',

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
    ],

     # What does your project relate to?
    keywords='sample python ls development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['setuptools'],

    #data_files=[('my_data', ['data/data_file'])],
    # config files

    entry_points={
        'console_scripts': [
            'python-ls=myls.utils.main',
        ],
    },
 )
