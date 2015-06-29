from jobvite.models import Position, Category
from django.http import HttpResponse, HttpResponseNotFound
from django.core.serializers.json import DjangoJSONEncoder

try:
    import json
except:
    import simplejson as json


def _cleanse_params(params):
    """
    Convert a ``QueryDict`` into a dictionary of parameters ready
    for a call to ``filter``. Remove any keys that are not fields
    to prevent a ``FieldError``. Also exclude primary keys.
    """
    cleansed = {}
    field_names = [field.name for field in Position._meta.fields
                   if not field.primary_key]
    for k, v in params.iteritems():
        if k in field_names:
            cleansed[k + '__icontains'] = v
    return cleansed


def json_dumps(iterable):
    return HttpResponse(json.dumps(iterable, cls=DjangoJSONEncoder), content_type='application/json')


def positions(request, job_id=None):
    positions_qs = Position.objects

    if job_id:
        positions = positions_qs.filter(job_id=job_id)
    
    else:
        params = _cleanse_params(request.GET)
        positions = positions_qs.filter(**params)

    positions = [p.to_dict() for p in positions]
    return json_dumps(positions)


def categories(request, category_id=None):

    categories_qs = Category.objects

    if category_id:
        categories = categories_qs.filter(pk=category_id)
    else:
        params = _cleanse_params(request.GET)
        categories = categories_qs.filter(**params)
    
    categories = [c.to_dict() for c in Category.objects.filter(**params)]
    return json_dumps(categories)
