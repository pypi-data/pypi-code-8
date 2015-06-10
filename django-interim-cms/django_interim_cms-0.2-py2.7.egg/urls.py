from django.conf.urls import patterns, url

from interim_cms.views import ExampleTileView


urlpatterns = patterns("",
    url(r"^example-tile/$", ExampleTileView.as_view(), name="example-tile"),
)
