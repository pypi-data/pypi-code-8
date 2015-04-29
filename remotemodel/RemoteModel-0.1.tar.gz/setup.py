from distutils.core import setup

setup(name='RemoteModel',
      version='0.1',
      description='API Clients via Dict-like object',
      author='Sam Fries',
      author_email='samuelbfries@gmail.com',
      url="https://github.com/chaosphere2112/RemoteModel",
      install_requires=["requests"],
      download_url="https://github.com/chaosphere2112/RemoteModel/tarball/0.1",
      keywords=["api", "restful", "hypermedia"],
      packages=['remote_model', 'remote_model.github'],)
