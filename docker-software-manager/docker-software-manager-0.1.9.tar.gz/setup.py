from setuptools import setup

setup(name='docker-software-manager',
      version='0.1.9',
      description='Manage your server software with a combination of docker, systemd, docker-compose, docker-gen and nginx ',
      url='https://github.com/robomod/docker-software-manager',
      author='Andreas Ihrig (RoboMod)',
      author_email='mod.andy@gmx.de',
      license='GPLv2',
      packages=['dsm'],
      install_requires=['docker-compose'],
      package_data={
        'dsm': ['defaults.conf', 
                'docker-gen/install.sh', 
                'docker-gen/remove.sh', 
                'docker-gen/update.sh']
        },
      data_files=[('/etc/docker-software-manager/', ['dsm/docker-gen/nginx.tmpl'])],
      entry_points = {
        'console_scripts': ['dsm=dsm.cli:main']
        }
      )