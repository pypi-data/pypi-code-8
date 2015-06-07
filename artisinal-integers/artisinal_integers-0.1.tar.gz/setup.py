from setuptools import setup

setup(name='artisinal_integers',
                        version='0.1',
                        description='get a unique artisinal integer from one of many providers',
                        url='http://github.com/micahwalter/artisinal_integers',
                        author='Micah Walter',
                        author_email='micah@micahwalter.com',
                        license='MIT',
                        packages=['artisinal_integers'],
			install_requires=[
                          'requests',
                        ],
                        zip_safe=False)
