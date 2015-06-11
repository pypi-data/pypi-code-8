import yaml
from django.utils import six
from django.apps import apps
from django.template import Template as DjangoTemplate, Context


def get_test_context(spec):
    result = {}
    for key, value in spec.items():
        if isinstance(value, (six.string_types,)):
            result[key] = value
            continue

        if isinstance(value, (dict,)):
            if value['type'] == 'model':
                model = apps.get_model(
                    app_label=value['app'],
                    model_name=value['model']
                )
                result[key] = model.objects.order_by('?').first()
            else:
                raise ValueError('Unknown type {0} for context key {1}'.format(
                                 value['type'], key))
            continue
        result[key] = value
    return result


def try_render_template(template_text, specs):
    context_spec = yaml.load(specs)['context']
    context = Context(get_test_context(context_spec))
    template = DjangoTemplate(template_text)
    return template.render(context)
