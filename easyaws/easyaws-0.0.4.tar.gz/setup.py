from setuptools import setup

setup(name='easyaws',
      version='0.0.4',
      description='Easy to use AWS commands for developers (currently supports EC2; tools for S3 coming soon)',
      packages=['easyaws'],
      install_requires = ['awscli>=1.7.30'],
      url='http://github.com/amberj/easyaws',
      scripts = ["easyaws/ec2ssh", "easyaws/ec2list", "easyaws/easyaws"],
      author='Amber Jain',
      author_email='i.amber.jain@gmail.com',
      license='ISC',
      keywords = ["amazon", "aws", "ec2", "ami", "ssh", "cloud", "boto", "easy", "tools", "tool", "cli", "command", "devs", "developers"],
      classifiers = [
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: Console",
        "Topic :: Utilities"
        ],
      zip_safe=False)
