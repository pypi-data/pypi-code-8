from setuptools import setup, find_packages

setup(
    name = 'nyc-crime-map',
    version = '0.3',
    description = 'Get data from the crime map',
    author = 'Thomas Levine',
    author_email = '_@thomaslevine.com',
    url = 'http://thomaslevine.com/!/nyc-crime-map/',
    entry_points = {'console_scripts': ['nyc-crime-map = nyc_crime_map:cli']},
    license = 'AGPL',
    packages = ['nyc_crime_map'],
    install_requires = [
        'requests>=2.3.0',
        'vlermv>=1.2.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
)
print('''Use nyc-crime-map like so.

    nyc-crime-map

Run this to see more options.

    nyc-crime-map -h

If you want to download the data every week, you might add this to your
crontab. (Run "crontab -e", and paste this there.)

    @weekly nyc-crime-map -d ~/nyc-crime-map-data

This will put the data in the "nyc-crime-map-data" within your home directory.

Contact Tom (_@thomaslevine.com) or the NYC crime map mailing list
(http://lists.dada.pink/listinfo/nyc-crime-map) with commentary and whatnot.

''')
