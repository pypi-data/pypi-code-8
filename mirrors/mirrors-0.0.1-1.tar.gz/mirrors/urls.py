from django.conf.urls import include, patterns, url

from mirrors import views

# this is the regexp that indicates a component with the year and month set
COMPONENT_RE = '^component/(?P<slug>[-\w]+)'

# this is the regexp that indicates a component without a year and month set
COMPONENT_SLUG_RE = '^component/(?P<slug>[-\w]+)'

urlpatterns = patterns(
    'mirrors.views',
    url(r'^component$',
        views.ComponentList.as_view(),
        name='component-list'),

    # here are URLs for components that only have a slug
    url(r"{}$".format(COMPONENT_RE),
        views.ComponentDetail.as_view(),
        name='component-detail'),
    url(r"{}/attribute$".format(COMPONENT_SLUG_RE),
        views.ComponentAttributeList.as_view(),
        name='component-attribute-list'),
    url(r"{}/attribute/(?P<name>[-\w_]+)$".format(COMPONENT_SLUG_RE),
        views.ComponentAttributeDetail.as_view(),
        name='component-attribute-detail'),
    url(r"{}/data$".format(COMPONENT_RE),
        views.ComponentData.as_view(),
        name='component-data'),
    url(r"{}/lock$".format(COMPONENT_SLUG_RE),
        views.ComponentLock.as_view(),
        name='component-lock'),
    url(r"{}/revision$".format(COMPONENT_SLUG_RE),
        views.ComponentRevisionList.as_view(),
        name='component-revision-list'),
    url(r"{}/valid$".format(COMPONENT_SLUG_RE),
        views.ComponentValidity.as_view(),
        name='component-validity'),
    url(r"{}/revision/(?P<version>[\d]+)$".format(COMPONENT_SLUG_RE),
        views.ComponentRevisionDetail.as_view(),
        name='component-revision-detail'),
    url(r"{}/revision/(?P<version>[\d]+)/data$".format(COMPONENT_SLUG_RE),
        views.ComponentRevisionData.as_view(),
        name='component-revision-data'),

    url(r'^autocomplete$',
        views.ComponentAutocomplete.as_view(),
        name='autocomplete'),

    url(r'^schemas$',
        views.component_schemas,
        name='component-schemas'),

    url(r'api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),

    url(r'^user$',
        views.UserDetail.as_view(),
        name='user-detail'),
)
