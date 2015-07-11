import os
import pytest
import reseasdk


@pytest.fixture(scope='session')
def package(request):
    """ Creates a package named sandbox. """

    if not os.path.exists('sandbox'):
        reseasdk.main(['new', 'sandbox'])

    os.chdir('sandbox')

    def fin():
        os.chdir('..')
    request.addfinalizer(fin)
