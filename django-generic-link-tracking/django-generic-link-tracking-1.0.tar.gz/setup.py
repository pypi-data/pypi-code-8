from distutils.core import setup

setup(name='django-generic-link-tracking',
      version='1.0',
      description='Generic trackable links for django',
      author='Jonatron',
      author_email='jon4tron@gmail.com',
      license='MIT License',
      url='https://github.com/jonatron/django-generic-link-tracking',
      packages=['generic_link_tracking'],
      install_requires=[
        'numconv==2.1.1'
      ],
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
     )
