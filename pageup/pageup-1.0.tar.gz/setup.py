from distutils.core import setup


setup(
    name='pageup',
    version='1.0',
    packages=['pageup'],
    author='Elijah Caine',
    author_email='elijahcainemv@gmail.com',
    url='https://elijahcaine.me/bookclub/',
    description='A small package for throwing together single page static sites',
    install_requires=['docutils==0.12',
                      'Jinja2==2.7.3',
                      'MarkupSafe==0.23',
                      'requests==2.7.0',],
    scripts=['pageup/pageup'],
    download_url='https://elijahcaine.me/bookclub/',
    classifiers=['License :: OSI Approved :: MIT License'],
)
