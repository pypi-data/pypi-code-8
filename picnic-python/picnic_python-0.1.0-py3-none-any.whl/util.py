__all__ = ['json']

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise ImportError("Either json or simplejson is required.")

