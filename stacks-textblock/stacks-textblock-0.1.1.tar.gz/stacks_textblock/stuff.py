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
    ]
    list_display = ('id', 'name')


class StacksTextBlockListStuff(registry.ModelStuff):
    queryset = StacksTextBlockList.objects.all()
    description = 'A block of text and/or content.'
    serializer_class = StacksTextBlockListSerializer
    renditions = [
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
