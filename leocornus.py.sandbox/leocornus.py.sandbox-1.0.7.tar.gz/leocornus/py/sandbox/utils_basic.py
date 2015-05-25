# utils_basic.py

# the module for basic utilities functions.

# we will follow the Python code style guide,
# function name should be all lowercase letter with underscore.

# doctest only works for docstring, it will not work here.
# the following test will not be tested.
#
# >>> print(2 * 6)
# 12
#

import os
import subprocess
import shutil

# make a temp folder for testing...
def make_test_folder(folder_name="test"):
    """create a folder in current user's home folder for
    testing. The default folder name is test.
    
    it will return the absolute path to the created folder.
    """

    """
    quick test the function here::

    >>> import os
    >>> from leocornus.py.sandbox.utils_basic import make_test_folder
    >>> testFolder = make_test_folder()
    >>> os.path.exists(testFolder)
    True
    >>> os.path.isdir(testFolder)
    True

    now we need clean up.

    >>> import shutil
    >>> shutil.rmtree(testFolder)
    >>> os.path.exists(testFolder)
    False

    """

    homeFolder = os.path.expanduser("~")
    testFolder = os.path.join(homeFolder, folder_name)
    os.mkdir(testFolder)
    return testFolder

# utility function to create files for testing...
def create_file(folder, filename, content):
    """Create file with the give name in the given folder.

    If the folder is not exist, we will create it.
    """
    """
    The is quick test::

    >>> import os
    >>> import shutil
    >>> from leocornus.py.sandbox.utils_basic import create_file

    >>> homefolder = os.path.expanduser("~")
    >>> testFolder = os.path.join(homefolder, 'test123')
    >>> os.path.exists(testFolder)
    False
    >>> os.path.isdir(testFolder)
    False
    >>> filename = create_file(testFolder, 'one.txt', 'hello file!')
    >>> os.path.isdir(testFolder)
    True

    need some clean up here.

    >>> shutil.rmtree(testFolder)
    >>> os.path.exists(testFolder)
    False

    """

    if(not os.path.exists(folder)):
        # try to create this folder.
        os.mkdir(folder)

    fullName = os.path.join(folder, filename)
    os.system("touch " + fullName)
    f = open(fullName, 'r+')
    f.write(content)
    f.close()
    return fullName

def extract_wp_header(filepath, **default):
    """extract WordPress file header fields values in a dict.

    filepath should be the full path to the file.
    default will provide the available default value.
    We will support the following file header field:

    - Plugin|Theme Name as Name
    - Plugin|Theme URI as URI
    - Description
    - Version
    - Author
    - Author URI
    """
    """
    test the doc test in a py file.

    >>> print(1 + 2)
    3 

    """

    # preparing the patterns.
    patterns = ['Version:.*',
                '(Plugin|Theme) Name:.*',
                'Description:.*',
                '(Plugin|Theme) URI:.*',
                'Author:.*',
                'Author URI:.*'
               ]

    # return as a dict.
    ret = {}
    for pattern in patterns:
        # get the field name:
        field_name = pattern.split(b":")[0]
        # the grep pattern.
        grep_pattern = """grep -oE '%s' %s""" % (pattern, filepath)

        try:
            value = subprocess.check_output(grep_pattern, shell=True)
            # we will only get the first line of the reuslt.
            # this is for some package has more than one 
            # header in a file.
            value = value.splitlines()[0]
            # only split the first ":"
            value = value.strip().split(b":", 1)
            ret[field_name] = value[1].strip()
        except subprocess.CalledProcessError:
            # could NOT find the pattern.
            if default.has_key(field_name):
                ret[field_name] = default[field_name]
            else:
                ret[field_name] = ""

    return ret

def transfer_wp_header(headers, pkg_name, base_url):
    """transfer the WordPress headers to what we need.
    """

    homepage = """[%s %s]""" % (headers['(Plugin|Theme) URI'],
                                'Plugin Homepage')
    download = """[%(base)s/%(name)s.zip %(name)s.zip]""" % dict(
      base = base_url,
      name = """%s.%s""" % (pkg_name, headers['Version'])
    )
    pageTitle = headers['(Plugin|Theme) Name']

    values = dict(
      name = pageTitle,
      description = headers['Description'],
      latest_version = headers['Version'],
      internet_page = homepage,
      download = download
    )

    return values
