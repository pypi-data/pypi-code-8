from setuptools import setup, find_packages

VERSION = '0.0.4'

setup(name='influxdb-sysmond',
      version=VERSION,
      description="System monitoring daemon that logs to InfluxDB",
      author="Evan Darwin",
      author_email="evan@devil.io",
      url="https://github.com/EvanDarwin/InfluxDB-sysmond",
      license="MIT",
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'tests', 'release']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['psutil', 'docopt', 'influxdb'],
      entry_points={'console_scripts': [
          'influxdb-sysmond = sysmond.main:main']},
      data_files=[('/etc/influxdb-sysmond', ['config.ini.dist'])])
