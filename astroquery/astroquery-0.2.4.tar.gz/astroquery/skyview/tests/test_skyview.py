# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os.path
from astropy.tests.helper import pytest

from ...utils.testing_tools import MockResponse
from ...skyview import SkyView


class MockResponseSkyView(MockResponse):
    def __init__(self):
        super(MockResponseSkyView, self).__init__()

    def get_content(self):
        return self.content

class MockResponseSkyviewForm(MockResponse):
    def __init__(self, method, url, cache=False, params=None, **kwargs):
        super(MockResponseSkyviewForm, self).__init__(**kwargs)
        self.content = self.get_content(method, url)

    def get_content(self, method, url):
        if 'basicform.pl' in url and method=='GET':
            with open(data_path('query_page.html'),'r') as f:
                return f.read()
        elif 'runquery.pl' in url and method =='GET':
            with open(data_path('results.html'), 'r') as f:
                return f.read()
        else:
            raise ValueError("Invalid method/url passed to "
                             "Mock Skyview request")


def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    return os.path.join(data_dir, filename)


@pytest.fixture
def patch_get(request):
    mp = request.getfuncargvalue("monkeypatch")
    mp.setattr(SkyView, '_request', MockResponseSkyviewForm)
    return mp

def test_get_image_list_local(patch_get):
    urls = SkyView.get_image_list(position='Eta Carinae',
                                  survey=['Fermi 5', 'HRI', 'DSS'])
    assert len(urls) == 3
    for url in urls:
        assert url.startswith('../../tempspace/fits/')

def test_survey_validation(patch_get):
    with pytest.raises(ValueError) as ex:
        urls = SkyView.get_image_list(position='doesnt matter',
                                      survey=['not_a_valid_survey'])
    assert str(ex.value) == ("Survey is not among the surveys hosted "
                             "at skyview.  See list_surveys or "
                             "survey_dict for valid surveys.")
