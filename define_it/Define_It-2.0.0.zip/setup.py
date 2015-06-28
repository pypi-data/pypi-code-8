from setuptools import setup

setup(name='Define_It',
	version='2.0.0',
	description='Responds to mentions and keyword "define" with a definition of the word/phrase',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Topic :: Internet',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	url='https://github.com/Spedwards/RedditBots/tree/master/Define_It',
	author='Spedwards',
	author_email='improbablepuzzle@gmail.com',
	license='MIT',
	packages=['Define_It'],
	install_requires=[
		'praw>=3.0.0',
		'wordnik-py3>=2.1.2',
		'praw-oauth2util>=0.1',
	],
	zip_safe=False)