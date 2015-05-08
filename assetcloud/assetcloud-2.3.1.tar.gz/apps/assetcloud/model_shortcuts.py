def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def max_field_length(model, field):
    """
    Shortcut to return a given field's max length.
    """
    return model._meta.get_field(field).max_length
