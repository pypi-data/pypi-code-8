from textplusstuff import registry

from .models import StacksFeaturedLink, StacksFeaturedLinkList
from .serializers import StacksFeaturedLinkSerializer, \
    StacksFeaturedLinkListSerializer


class StacksFeaturedLinkListStuff(registry.ModelStuff):
    queryset = StacksFeaturedLinkList.objects.prefetch_related(
        'stacksfeaturedlinklistlink_set',
        'stacksfeaturedlinklistlink_set__link'
    )

    description = 'A list of links with optional image and/or content.'
    serializer_class = StacksFeaturedLinkListSerializer
    renditions = [
        registry.Rendition(
            short_name='1up',
            verbose_name="Featured Link List 1-Up",
            description="A list of links displayed in grid with one link "
                        "in each row.",
            path_to_template='stacks_featuredlink/stacksfeaturedlinklist/'
                             'stacksfeaturedlinklist-1up.html'
        ),
        registry.Rendition(
            short_name='2up',
            verbose_name="Featured Link List 2-Up",
            description="A list of links displayed in grid with two links "
                        "in each row.",
            path_to_template='stacks_featuredlink/stacksfeaturedlinklist/'
                             'stacksfeaturedlinklist-2up.html'
        ),
        registry.Rendition(
            short_name='3up',
            verbose_name="Featured Link List 3-Up",
            description="A list of links displayed in grid with three links "
                        "in each row.",
            path_to_template='stacks_featuredlink/stacksfeaturedlinklist/'
                             'stacksfeaturedlinklist-3up.html'
        )
    ]
    list_display = ('id', 'name')


class StacksFeaturedLinkStuff(registry.ModelStuff):
    queryset = StacksFeaturedLink.objects.all()

    description = 'A link with an optional image and/or content.'
    serializer_class = StacksFeaturedLinkSerializer
    renditions = [
        registry.Rendition(
            short_name='button',
            verbose_name="Featured Link Button",
            description="A single link displayed as a button (without image "
                        "or optional content included).",
            path_to_template='stacks_featuredlink/stacksfeaturedlink/'
                             'stacksfeaturedlink-button.html'
        ),
    ]
    list_display = ('id', 'list_name')


registry.stuff_registry.add_modelstuff(
    StacksFeaturedLinkList,
    StacksFeaturedLinkListStuff,
    groups=['stacks']
)


registry.stuff_registry.add_modelstuff(
    StacksFeaturedLink,
    StacksFeaturedLinkStuff,
    groups=['stacks']
)
