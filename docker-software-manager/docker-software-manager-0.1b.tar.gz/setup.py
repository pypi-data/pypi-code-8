from setuptools import setup

setup(name='docker-software-manager',
      version='0.1b',
      description='Manage your server software with a combination of docker, systemd, docker-compose, docker-gen and nginx ',
      url='https://github.com/robomod/docker-software-manager',
      author='Andreas Ihrig (RoboMod)',
      author_email='mod.andy@gmx.de',
      license='GPLv2',
      packages=['dsm'],
      install_requires=['Template', 'SafeConfigParser'],
      data_files=[('docker-compose', ['docker-compose/install.sh', 'docker-compose/remove.sh', 'docker-compose/update.sh']),
	    ('docker-gen', ['docker-gen/install.sh', 'docker-gen/remove.sh', 'docker-gen/update.sh'])],
      entry_points = {
        'console_scripts': ['docker-software-manager=dsm.cli:main',
                            'dsm=dsm.cli:main']
        }
        )