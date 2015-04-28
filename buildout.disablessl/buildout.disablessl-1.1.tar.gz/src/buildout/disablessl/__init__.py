import sys


def extension(buildout):
    """Disable SSl certificate verification in setuptools and Python."""
    import setuptools.ssl_support
    setuptools.ssl_support.is_available = False

    if sys.version_info >= (2, 7, 9):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
