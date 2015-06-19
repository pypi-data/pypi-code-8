from textplusstuff import registry

from .models import Snippet
from .serializers import SnippetSerializer


class SnippetStuff(registry.ModelStuff):
    queryset = Snippet.objects.all()
    verbose_name = 'HTML Snippet'
    verbose_name_plural = 'HTML Snippets'
    description = 'Add a HTML Snippet'
    serializer_class = SnippetSerializer
    renditions = [
        registry.Rendition(
            short_name='full_width',
            verbose_name="Snippet Full Width",
            description='Displays an HTML Snippet that spans the full '
                        'width of the page.',
            path_to_template='stacks_snippet/snippet-full_width.html',
            rendition_type='block'
        ),
    ]
    list_display = ('id', 'name')

registry.stuff_registry.add_modelstuff(
    Snippet,
    SnippetStuff,
    groups=['stacks', ]
)
