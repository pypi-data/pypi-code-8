import flattrclient.things
import flattrclient.resource

class Subscription(flattrclient.resource.Resource):
    """ One of your `subscription
    http://developers.flattr.net/api/resources/subscriptions/`_ """

    def __init__(self, session=None, active=True, created_at=None,
                 started_at=None, thing={}, **kwargs):
        """ Initialize with data of an dictionary

        :param session: `requests.session.Session`.
        :param active: Is this subscription active or paused.
        :param created_at: ...
        :param started_at: started or resumed.
        :param thing: Related thing.
        """
        # ignored fields: kwargs
        # so lib will not break if flattr-api adds a new field
        super(Subscription, self).__init__(session)
        # ro fields
        # Do not check any types.
        self._active = active
        self._created_at = created_at
        self._started_at = started_at
        if thing:
            self._thing = flattrclient.things.Thing(session=session, **thing)

    def __repr_helper__(self):
        thing = getattr(self, '_thing', {})
        return getattr(thing, '_title', None) or 'at %s' % id(self)

    # Most of the fields are readonly since you can not modify them on flattr
    @property
    def active(self):
        """ Returns active """
        return getattr(self, '_active', None)

    @property
    def created_at(self):
        """ Returns created_at """
        return getattr(self, '_created_at', None)

    @property
    def started_at(self):
        """ Returns started_at """
        return getattr(self, '_started_at', None)

    @property
    def thing(self):
        """ Returns the subscribed thing """
        return getattr(self, '_thing', None)
