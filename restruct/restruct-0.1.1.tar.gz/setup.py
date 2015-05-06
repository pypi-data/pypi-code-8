from setuptools import setup

setup(
    name                        = "restruct",
    packages                    = [
        "ReStruct",
    ],
    package_dir                 = {
        "ReStruct":		".",
    },
    version                     = "0.1.1",
    include_package_data        = True,
    author                      = "Matthew Brisebois",
    author_email                = "matthew@webheroes.ca",
    url                         = "https://github.com/webheroesinc/restruct",
    license                     = "Dual License; GPLv3 and Proprietary",
    description                 = "Python implementation for turning SQL results into beautiful JSON structures.",
    long_description		= """ReStruct is an easy light-weight formatting library that simplifies the process of representing
SQL results in a human readable format (JSON).  Pass the restruct method your SQL results and a
formatting structure and voila, you have turned your complex SQL result into beautiful JSON.  One of
the best features of ReStruct is squashing all the duplicate entries from SQL joins into a sub
section of your JSON structure.

===============
 Usage examples
===============

*Lets assume we have an SQL join for a 1 to 1 relationship and that all the format variables used
represent columns in the select tables.*

::
  
      SELECT user_id,
             user_level,
             level_name,
             first_name,
             last_name,
             email
        FROM users
        JOIN user_levels USING (user_level_id)

Formatting
=============

*An example format structure for results from the above query:*

::

    {
        ".single": true,
        ".key": "{user_id}",
        "id": ": {user_id}", 
        "level": {
            "id": ": {user_level}", 
            "name": ": {user_level_name}"
        },
        "name": {
            "first": ":< first_name",
            "last": ":< last_name", 
            "full": "{first_name} {last_name}"
        },
        "email": true
    }

    """,
    keywords                    = ["mysql", "sqlite", "sql", "json"],
    classifiers                 = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
)
