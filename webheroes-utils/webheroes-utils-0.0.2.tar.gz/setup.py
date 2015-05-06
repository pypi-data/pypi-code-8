from setuptools import setup

setup(
    name                        = "webheroes-utils",
    packages                    = [
        "WHIutils",
    ],
    package_dir                 = {
        "WHIutils":		".",
        "WHIutils.testing":	"testing",
    },
    version                     = "0.0.2",
    include_package_data        = True,
    author                      = "Matthew Brisebois",
    author_email                = "matthew@webheroes.ca",
    url                         = "https://github.com/webheroesinc/python-utils",
    license                     = "Dual License; GPLv3 and Proprietary",
    description                 = "Set of python utils made specifically for Web Heroes Inc.",
    keywords                    = [],
    classifiers                 = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
)
