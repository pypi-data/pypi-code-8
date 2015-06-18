from datetime import datetime
from .base import configure_app, create_app, flush_db_changes
from turbopress import model


class TurboPressControllerTests(object):
    def setup(self):
        self.app = create_app(self.app_config, False)

    def test_articles(self):
        a = model.provider.create(model.Article, {'title': 'Hello',
                                                  'content': 'World',
                                                  'published': True})
        flush_db_changes()

        res = self.app.get('/call_partial', {
            'partial': 'turbopress.partials:articles'
        })
        assert 'Hello' in res.text
        assert 'World' in res.text
        assert res.text.count('class="turbopress_article"') == 1, res.text

    def test_articles_multiple(self):
        a = model.provider.create(model.Article, {'title': 'Hello1',
                                                  'content': 'World',
                                                  'published': True})
        a = model.provider.create(model.Article, {'title': 'Hello2',
                                                  'content': 'World',
                                                  'published': True})
        a = model.provider.create(model.Article, {'title': 'Hello3',
                                                  'content': 'World',
                                                  'published': False})
        flush_db_changes()

        res = self.app.get('/call_partial', {
            'partial': 'turbopress.partials:articles'
        })
        assert res.text.count('class="turbopress_article"') == 2

    def test_article_preview(self):
        a = model.provider.create(model.Article, {'title': 'Hello',
                                                  'content': 'World',
                                                  'published': True})
        article_uid = a.uid
        flush_db_changes()

        res = self.app.get('/call_partial', {
            'partial': 'turbopress.partials:article_preview',
            'article': article_uid
        })
        assert '<a href="/press/view/' in res.text, res.text
        assert 'Hello' in res.text, res.text
        assert res.text.count('class="turbopress_article"') == 1, res.text

    def test_articles_search(self):
        a = model.provider.create(model.Article, {'title': 'Hello1',
                                                  'content': 'World',
                                                  'published': True})
        a = model.provider.create(model.Article, {'title': 'Hello2',
                                                  'content': 'World',
                                                  'published': True})
        a = model.provider.create(model.Article, {'title': 'Hello3',
                                                  'content': 'World',
                                                  'published': False})
        flush_db_changes()

        res = self.app.get('/call_partial', {
            'partial': 'turbopress.partials:search',
            'blog': '',
            'value': 'Hello2'
        })
        assert 'action="/press/search"' in res.text, res.text
        assert 'name="text"' in res.text
        assert 'name="blog"' in res.text
        assert 'value="Hello2"' in res.text

    def test_articles_tagcloud(self):
        a = model.provider.create(model.Article, {'title': 'Hello1',
                                                  'content': 'World',
                                                  'published': True})
        a = model.provider.create(model.Article, {'title': 'Hello2',
                                                  'content': 'World',
                                                  'published': True})
        a = model.provider.create(model.Article, {'title': 'Hello3',
                                                  'content': 'World',
                                                  'published': False})
        flush_db_changes()

        res = self.app.get('/call_partial', {
            'partial': 'turbopress.partials:tagcloud',
            'blog': '',
            'tags': 'first,second,third'
        })
        assert '<h3>Tags</h3>' in res.text, res.text
        assert res.text.count('href="/press/search') == 3
        assert 'tags=first' in res.text
        assert 'tags=second' in res.text
        assert 'tags=third' in res.text

    def test_articles_excerpts(self):
        a = model.provider.create(model.Article, {'title': 'Hello1',
                                                  'content': 'World',
                                                  'published': True})
        a = model.provider.create(model.Article, {'title': 'Hello2',
                                                  'content': 'World',
                                                  'published': True})
        a = model.provider.create(model.Article, {'title': 'Hello3',
                                                  'content': 'World',
                                                  'published': False})
        flush_db_changes()

        res = self.app.get('/call_partial', {
            'partial': 'turbopress.partials:excerpts'
        })
        assert res.text.count('class="turbopress_articles_excerpt"') == 2, res.text
        assert 'Hello2' in res.text, res.text
        assert 'Hello1' in res.text, res.text
        assert 'Hello3' not in res.text, res.text
        assert 'World' not in res.text, res.text

    def test_articles_excerpt(self):
        a = model.provider.create(model.Article, {'title': 'Hello1',
                                                  'content': 'World',
                                                  'published': True})
        article_uid = a.uid
        flush_db_changes()

        res = self.app.get('/call_partial', {
            'partial': 'turbopress.partials:excerpt',
            'article': article_uid
        })
        assert res.text.count('class="turbopress_articles_excerpt"') == 1, res.text
        assert 'Hello1' in res.text, res.text
        assert 'World' not in res.text, res.text


class TestTurboPressControllerSQLA(TurboPressControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestTurboPressControllerMing(TurboPressControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')

