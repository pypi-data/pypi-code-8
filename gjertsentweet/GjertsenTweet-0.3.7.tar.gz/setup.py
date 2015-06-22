"""
Welcome to GjertsenTweet's documentation!
=========================================

**GjertsenTweet** is a twitter client built for the command line.
It has been built with npyscreen to create a simple text-based user interface.

It lets you read the tweets from your feed, search and post tweets.

Usage
-----
When launched for the first you will be asked to open a link in your browser
in order to approve the app and login.

When logged in, you can simply use the keys or enter to move around.
Note that once you have moved down to feed, you can't move back up with
the keys. You have to either press cancel or ok to go back to the top.

When cancel is pressed it will ask you if you wanna quit or not. If you say no,
the cursor will jump back to the top.

When you have entered something under 'What's happening', and press ok
it will first check if your tweet have a valid size (>= 140 characters).
If it's more than 140 characters it will delete what you have written and jump
back to the top.

If the tweet has a valid length, it will ask you wether you wanna post this or
not.

If you have entered somehting to search it will simply search for this and
update you feed without asking.

The twitter feed will be updated on the fly.

Note that you have to press enter when the dialog boxes pops up in order
to move the cursor to the button/buttons
"""

from setuptools import setup

setup(name='GjertsenTweet',
      version='0.3.7',
      description='A simple twitter client for the terminal',
      long_description = __doc__,
      author='Fredrik Gjertsen',
      author_email='f.gjertsen@gmail.com',
      url='https://github.com/fredgj/GjertsenTweet',
      packages=['GjertsenTweet'],
      license='GNU General Public License',
      install_requires=['npyscreen==4.9.1',
                        'twitter==1.17.0'],
      entry_points={
          'console_scripts':
            ['gjertsentweet=GjertsenTweet.client:main'],
          },
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Utilities'],
      keywords='twitter, command-line tools')


__author__ = 'Fredrik Gjertsen'

