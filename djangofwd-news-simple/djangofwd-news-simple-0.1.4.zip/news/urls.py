
from django.conf import settings
from django.conf.urls import patterns, url

# Views
from views import NewsList, NewsDetail, NewsListCategory, NewsListCategories, NewsDetailCategory


urlpatterns = patterns('',
    url('^categories/list/$', NewsListCategories.as_view(), name='news_list_categories'),
    url('^category/detail/(?P<slug>[\w-]+)/$', NewsDetailCategory.as_view(), name='news_detail_category'),
    url('^category/list/(?P<slug>[\w-]+)/$', NewsListCategory.as_view(), name='news_list_category'),
    url('^(?P<slug>[\w-]+)/$', NewsDetail.as_view(), name='news_detail'),
    url('^$', NewsList.as_view(), name='news_list'),
)
