from setuptools import setup, find_packages
setup(
  name="cloudbot",
  version=1.2,
  packages=["cb"],
  install_requires=[
    "docopt",
    "boto",
  ],
  entry_points={
    "console_scripts": [
      "cloudbot=cb.cloudbot:main"
    ]
  }
)
