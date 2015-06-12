import flask.signals


_signals = flask.signals.Namespace()
signal = _signals.signal


def listens_to(name, sender=None, weak=True):
    """Listens to a named signal
    """
    def decorator(f):
        if sender:
            return signal(name).connect(f, sender=sender, weak=weak)
        return signal(name).connect(f, weak=weak)
    return decorator
