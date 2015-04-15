import flattrclient.resource

class Flattr(flattrclient.resource.Resource):
    def __init__(self, session=None, thing=None, owner=None, created_at=None,
                 **kwargs):
        """A flattr/support object

        :params session: `requests.session.Session`.
        :params thing: flattr belong to this thing.
        :params owner: owner of the thing.
        :params created_at: means flattred at.
        """
        # ignored fields: kwargs
        # so lib will not break if flattr-api adds a new field
        self._thing = thing
        self._owner = owner
        self._created_at = created_at

    @property
    def thing(self):
        """ Returns thing """
        return getattr(self, '_thing', None)

    @property
    def owner(self):
        """ Returns owner """
        return getattr(self, '_owner', None)

    @property
    def created_at(self):
        """ Returns created_at """
        return getattr(self, '_created_at', None)
