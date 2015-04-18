import flattrclient
import flattrclient.flattrs
import flattrclient.resource
from flattrclient.validators import validate
from flattrclient.validators import isStr
from flattrclient.validators import isStrList
from flattrclient.validators import isUrl
from flattrclient.validators import isBool

class Thing(flattrclient.resource.Resource):
    """ flattr able `thing.
    http://developers.flattr.net/api/resources/things/`_ """

    _endpoint = 'rest/v2/things'

    def __init__(self, session=None, resource=None, link=None, id=None,
                 flattrs=None, flattrs_user_count=None, created_at=None,
                 owner=None, image=None, flattred=None, last_flattr_at=None,
                 updated_at=None, title=None, description=None, url=None,
                 tags=None, category=None, language=None, hidden=False,
                 subscribed=False, dirty=True, **kwargs):
        """ Initialize with data of an dictionary

        :param session: `requests.session.Session`.
        :param resource: URI in flattrs api.
        :param link: URI in flattrs web-ui.
        :param id: flattr id.
        :param owner: ...
        :param image: ...
        :param flattred: If already supported.
        :param last_flattr_at: ...
        :param updated_at: ...
        :param title: Main title.
        :param description: A little more than a title.
        :param url: Real url of the thing in the web.
        :param tags: Some keywords.
        :param categories: ...
        :param language: ...
        :param hidden: Is this thing public available.
        :param subscribed: Are you subscribed to it.
        :param dirty: Internal flag to detect necessary updates.
        """
        # ignored fields: kwargs
        # so lib will not break if flattr-api adds a new field
        super(Thing, self).__init__(session)
        # ro fields
        # Do not check any types.
        self._resource = resource
        self._link = link
        self._id = id
        self._flattrs = flattrs
        self._flattrs_user_count = flattrs_user_count
        self._created_at = created_at
        self._owner = owner
        self._image = image
        self._flattred = flattred
        self._last_flattr_at = last_flattr_at
        self._updated_at = updated_at
        self._subscribed = subscribed
        # rw fields
        # Checking types. Implicit via validate on fields.
        if title:
            self.title = title
        if description:
            self.description = description
        if url:
            self.url = url
        if tags:
            self.tags = tags
        if language:
            self.language = language
        if category:
            self.category = category
        self.hidden = hidden

        self._dirty = dirty

    def __repr_helper__(self):
        return getattr(self, '_title', None) or 'at %s' % id(self)

    # Most of the fields are readonly since you can not modify them on flattr
    @property
    def resource(self):
        """ Returns resource """
        return getattr(self, '_resource', None)

    @property
    def link(self):
        """ Returns link """
        return getattr(self, '_link', None)

    @property
    def id(self):
        """ Returns id """
        return getattr(self, '_id', None)

    @property
    def flattrs(self):
        """ Returns flattrs """
        return getattr(self, '_flattrs', None)

    @property
    def flattrs_user_count(self):
        """ Returns flattrs_user_count """
        return getattr(self, '_flattrs_user_count', None)

    @property
    def created_at(self):
        """ Returns created_at """
        return getattr(self, '_created_at', None)

    @property
    def owner(self):
        """ Returns owner """
        return getattr(self, '_owner', None)

    @property
    def image(self):
        """ Returns image """
        return getattr(self, '_image', None)

    @property
    def flattred(self):
        """ Returns flattred """
        return getattr(self, '_flattred', None)

    @property
    def last_flattr_at(self):
        """ Returns last_flattr_at """
        return getattr(self, '_last_flattr_at', None)

    @property
    def updated_at(self):
        """ Returns updated_at """
        return getattr(self, '_updated_at', None)

    @property
    def subscribed(self):
        """ Returns subscribed """
        return getattr(self, '_subscribed', False)

    # Some fields are writeable. Only those are submitted to the flattr api.
    @property
    def url(self):
        """ Returns url """
        return getattr(self, '_url', None)

    @url.setter
    @validate(isUrl)
    def url(self, v):
        """ set url

        :param v: value
        """
        self._url = v
        self._dirty = True

    @property
    def title(self):
        """ Returns title """
        return getattr(self, '_title', None)

    @title.setter
    @validate(isStr)
    def title(self, v):
        """ set title

        :param v: value
        """
        self._title = v
        self._dirty = True

    @property
    def description(self):
        """ Returns description """
        return getattr(self, '_description', None)

    @description.setter
    @validate(isStr)
    def description(self, v):
        """ set description

        :param v: value
        """
        self._description = v
        self._dirty = True

    @property
    def tags(self):
        """ Returns tags """
        return getattr(self, '_tags', None)

    @tags.setter
    @validate(isStrList)
    def tags(self, v):
        """ set tags

        :param v: value
        """
        self._tags = v
        self._dirty = True

    @property
    def language(self):
        """ Returns language """
        return getattr(self, '_language', None)

    @language.setter
    @validate(isStr)
    def language(self, v):
        """ set language

        :param v: value
        """
        self._language = v
        self._dirty = True

    @property
    def category(self):
        """ Returns category """
        return getattr(self, '_category', None)

    @category.setter
    @validate(isStr)
    def category(self, v):
        """ set category

        :param v: value
        """
        self._category = v
        self._dirty = True

    @property
    def hidden(self):
        """ Returns hidden """
        return getattr(self, '_hidden', False)

    @hidden.setter
    @validate(isBool)
    def hidden(self, v):
        """ set hidden

        :param v: value
        """
        self._hidden = v
        self._dirty = True

    # we also need some functionality
    @flattrclient.just_json
    @flattrclient.post('/:id/flattr')
    def support(self):
        """ Flattr this particular thing.
        Will not work if it's your thing. """
        return {}

    def commit(self):
        """ Create thing, or update if existing. """
        if not getattr(self, '_id', None):
            return self._create()
        res = self._update()
        self._dirty = False
        return res

    @flattrclient.refresh_thing_id
    @flattrclient.post('/')
    def _create(self):
        """ Create thing """
        return self._to_flattr_dict()

    @flattrclient.just_json
    @flattrclient.patch('/:id')
    def _update(self):
        """ Returns flattr result or None.
        None if nothing to do since object is not dirty. """
        if self._dirty:
            return self._to_flattr_dict()
        return False

    def refresh(self):
        """ Refresh this particular thing. Only works if it exists already on
        flattr (id, resource, etc. obtained from flattr) """
        raise NotImplementedError

    def subscribe(self):
        """ Subscribe to this thing, if currently unsubscribed. """
        res = self._subscribe()
        if res is not None:
            self._subscribed = True
        return res

    @flattrclient.just_json
    @flattrclient.post('/:id/subscriptions')
    def _subscribe(self):
        """ Subscribe to this thing, if currently unsubscribed. """
        if self.subscribed:
            return False
        return {}

    def pause_subscription(self):
        """ Pause or resume your subscription of the thing. """
        res = self._pause_subscription()
        self._subscribed = not self.subscribed
        return res

    @flattrclient.just_json
    @flattrclient.put('/:id/subscriptions')
    def _pause_subscription(self):
        """ Pause or resume your subscription of the thing. """
        return {}

    def unsubscribe(self):
        """ Unsubscribe from thing, if currently subscribed. """
        res = self._unsubscribe()
        if res is not None:
            self._subscribed = False
        return res

    @flattrclient.just_json([204])
    @flattrclient.delete('/:id/subscriptions')
    def _unsubscribe(self):
        """ Unsubscribe from thing, if currently subscribed. """
        if not self.subscribed:
            return False
        return {}

    def delete(self):
        """ Delete this thing. """
        res = self._delete()
        self._dirty = True
        self._id = None
        return res

    @flattrclient.just_json([204])
    @flattrclient.delete('/:id')
    def _delete(self):
        return {}

    def _to_flattr_dict(self):
        """ Returns flattr compatible dict for posts """
        if not self.url:
            raise AttributeError('url is required')
        if self.tags:
            tags = ','.join(self.tags)
        else:
            tags = None
        return flattrclient._get_query_dict(
                url=self.url,
                hidden=self.hidden,
                title=self.title,
                description=self.description,
                category=self.category,
                tags=tags
                )

    @flattrclient.result(flattrclient.flattrs.Flattr)
    @flattrclient.get('/:id/flattrs')
    def get_flattrs(self, count=None, page=None, full=False):
        """ Get flattrs of this thing.

        :param page: (Optional) - integer The result page to show
        :param count: (Optional) - integer Number of items per page
        :param full: ( Optional ) - Receive full user object instead of small
        """
        return flattrclient._get_query_dict(count=count, page=page, full=full)
