from setuptools import setup, find_packages
setup(
    name="FallingRocks",
    version="2.0",
    packages=find_packages(),
    data_files={'images': ['images/*.png']},
    author="hristy93",
    author_email="hristy93@gmail.com",
    description="Implementation of the game FallingRocks in Python",
    license="PSF",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Environment :: X11 Applications :: Qt',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment'
    ],
    keywords="falling rocks falllingrocks"
)

# data_files=[('images', ['images/rock1.png', 'images/rock2.png',
#     'images/rock3.png', 'images/rock4.png', 'images/rock5.png',
#     'images/rock6.png', 'images/rock7.png', 'images/rock8.png',
#     'images/icon.png', 'images/rock.png', 'images/smile.png',
#     'images/small_icon.png', 'images/slow_down_rocks.png',
#     'images/big_bomb.png', 'images/invinciblility.png',
#     'images/bullet.png'])],
