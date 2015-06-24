from textplusstuff import registry

from .models import StacksTextBlock, StacksTextBlockList
from .serializers import StacksTextBlockSerializer, \
    StacksTextBlockListSerializer


class StacksTextBlockStuff(registry.ModelStuff):
    queryset = StacksTextBlock.objects.all()
    description = 'A block of text and/or content.'
    serializer_class = StacksTextBlockSerializer
    renditions = [
        registry.Rendition(
            short_name='pullquote',
            verbose_name="Pull Quote",
            description="A block of text that prominently features "
                        "a pullquote.",
            path_to_template='stacks_textblock/stackstextblock/'
                             'stackstextblock-pullquote.html'
        ),
        registry.Rendition(
            short_name='full_width',
            verbose_name="Full-Width",
            description="A block of text that spans the full width of "
                        "the page.",
            path_to_template='stacks_textblock/stackstextblock/'
                             'stackstextblock-full_width.html'
        ),
    ]
    list_display = ('id', 'name')


class StacksTextBlockListStuff(registry.ModelStuff):
    queryset = StacksTextBlockList.objects.all()
    description = 'A block of text and/or content.'
    serializer_class = StacksTextBlockListSerializer
    renditions = [
        registry.Rendition(
            short_name='1up',
            verbose_name="Text Block List 1-Up",
            description="A list of text blocks displayed in grid with one "
                        "in each row.",
            path_to_template='stacks_textblock/stackstextblocklist/'
                             'stackstextblocklist-1up.html'
        ),
        registry.Rendition(
            short_name='2up',
            verbose_name="Text Block List 2-Up",
            description="A list of text blocks displayed in grid with two "
                        "in each row.",
            path_to_template='stacks_textblock/stackstextblocklist/'
                             'stackstextblocklist-2up.html'
        ),
        registry.Rendition(
            short_name='3up',
            verbose_name="Text Block List 3-Up",
            description="A list of text blocks displayed in grid with three "
                        "in each row.",
            path_to_template='stacks_textblock/stackstextblocklist/'
                             'stackstextblocklist-3up.html'
        ),
    ]
    list_display = ('id', 'list_name')


registry.stuff_registry.add_modelstuff(
    StacksTextBlock,
    StacksTextBlockStuff,
    groups=['stacks']
)

registry.stuff_registry.add_modelstuff(
    StacksTextBlockList,
    StacksTextBlockListStuff,
    groups=['stacks']
)
