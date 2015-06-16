__author__ = 'Lai Tash (lai.tash@yandex.ru)'


def _extract_from_kw(instance, kw, kw_key, attr_name=None):
    """
    Sets instance.attr_name to kw[key] if key in kw, otherwise leaves
    instance.attr_name unchanged.

    Example::
        _extract_from_kw(obj, {'a': 5}, 'a') -> obj.a = 5
        _extract_from_kw(obj, {}, 'a') -> obj.a = obj.a
        _extract_from_kw(obj, {'a': 5}, 'a', 'b') -> obj.b = 5


    :raises: AttributeError if key not in kw and instance.key is undefined
    :param instance: instance to set field value to
    :param kw: values dictionary
    :param key: field name
    """

    if attr_name is None:
        attr_name = kw_key

    setattr(instance, attr_name,
            kw[kw_key] if kw_key in kw else getattr(kw, attr_name))


class ValidationError(Exception):
    pass