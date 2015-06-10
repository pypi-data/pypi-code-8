from django.views.generic.edit import FormView

from interim_cms.forms import ExampleForm


class ExampleTileView(FormView):
    template_name = "interim_cms/example_tile.html"
    form_class = ExampleForm
