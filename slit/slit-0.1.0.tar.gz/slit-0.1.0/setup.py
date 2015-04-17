from setuptools import setup, find_packages

with open('README.rst') as f:
        long_description = f.read()

setup(
        name = "slit",
        version = "0.1.0",
        author = "Brett Weir",
        author_email = "brett@lamestation.com",
        description = "A sequential lit tool",
        long_description = long_description,
        license = "GPLv3",
        url = "https://github.com/bweir/slit",
        keywords = "lit literate programming sequential tutorial education software",
        packages=find_packages(exclude=['test']),
        include_package_data=True,
        scripts=['slit'],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 2.7",
            "Topic :: Text Processing :: Markup",
            "Topic :: Text Processing",
            "Intended Audience :: Developers",
            "Topic :: Documentation",
            "Topic :: Software Development :: Pre-processors",
            ]
        )
