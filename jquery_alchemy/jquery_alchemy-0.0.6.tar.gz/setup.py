import setuptools
import subprocess

pkg_name = 'jquery_alchemy'
pkg_url = 'http://www.github.com/mrichar1/jquery_alchemy'
pkg_license = 'GNU AGPL v3'
pkg_description = 'A package which creates jquery_validation rules from sqlalchemy columns for use with web forms.'
pkg_author = 'Matthew Richardson.'
pkg_author_email = 'm.richardson@ed.ac.uk'

pkg_classifiers = [
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 3',
            ]

install_requires = ['sqlalchemy', 'sqlalchemy_utils']


def call_git_describe():
    try:
        p = subprocess.Popen(['git', 'describe'],
                             stdout=subprocess.PIPE)
        return p.communicate()[0].split('\n')[0].strip()
    except Exception:
        return None

def read_release_version():
    try:
        with open("RELEASE-VERSION") as f:
            return f.readlines()[0].strip()
    except Exception:
        return None

def write_release_version(version):
    with open("RELEASE-VERSION", "w") as f:
        f.write("%s\n" % version)

def get_git_version():
    version = call_git_describe()
    release_version = read_release_version()
    if version is None:
        version = release_version

    if version is None:
        raise ValueError("Unable to determine the version number!")

    if version != release_version:
        write_release_version(version)

    return version


def main():

    setuptools.setup(
        name=pkg_name,
        version=get_git_version(),
        url=pkg_url,
        license=pkg_license,
        description=pkg_description,
        classifiers=pkg_classifiers,
        author=pkg_author,
	author_email=pkg_author_email,
        packages=setuptools.find_packages(),
        include_package_data=True,
        package_data={'': ['LICENSE', 'RELEASE-VERSION']},
        install_requires=install_requires,
        )


if __name__ == "__main__":
    main()
