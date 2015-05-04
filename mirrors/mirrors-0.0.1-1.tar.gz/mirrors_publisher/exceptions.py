class UnpublishedAttributeError(Exception):
    """This error is raised when some one attempts to publish a :class:`Component`
    before they've published the component's attributes.
    """
    missing_attribute = None

    def __init__(self, *args, **kwargs):
        if 'missing_attribute' in kwargs:
            self.missing_attribute = kwargs['missing_attribute']
            del kwargs['missing_attribute']

        super().__init__(*args, **kwargs)
