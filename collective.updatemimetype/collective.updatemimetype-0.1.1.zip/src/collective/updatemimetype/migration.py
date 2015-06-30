import logging

from plone.app.blob.field import BlobField
from Products.CMFCore.utils import getToolByName

from Products.contentmigration.basemigrator.walker import Walker
from Products.contentmigration.common import HAS_LINGUA_PLONE

LOG = logging.getLogger('collective.updatemimetype')


class AllCatalogWalker(Walker):

    def __init__(self, portal, migrator, src_portal_type=None,
                 dst_portal_type=None, **kwargs):
        super(AllCatalogWalker, self).__init__(portal, migrator)
        self.query = kwargs.get('query', {})

    def walk(self):
        query = self.query

        catalog = self.catalog

        if HAS_LINGUA_PLONE and 'Language' in catalog.indexes():
            query['Language'] = 'all'

        brains = catalog(query)

        for brain in brains:
            try:
                obj = brain.getObject()
            except AttributeError:
                LOG.error("Couldn't access %s" % brain.getPath())
                continue
            try:
                state = obj._p_changed
            except:
                state = 0
            if obj is not None:
                yield obj
                # safe my butt
                if state is None:
                    obj._p_deactivate()


class UpdateMimetypes(object):

    src_portal_type = None
    dst_portal_type = None
    src_meta_type = None
    dst_meta_type = None

    def __init__(self, obj, src_portal_type, dst_portal_type):
        self.obj = obj

    def migrate(self):
        obj = self.obj
        mtr = getToolByName(obj, 'mimetypes_registry')
        for field in obj.Schema().fields():
            if isinstance(field, BlobField):
                update_mimetype(field, obj, mtr)


def update_mimetype(field, obj, mtr):
    blobwrapper = field.get(obj)
    try:
        blob = blobwrapper.getBlob()
        file = blob.open()
    except:
        LOG.exception(
            'Cannot get or open blob from field "%s" of %s',
            field.getName(), obj.absolute_url()
            )
        return
    body = file.read()
    filename = blobwrapper.getFilename()
    if not body:
        LOG.info(
            'Skip field "%s" of %s because it has no content',
            field.getName(),
            obj.absolute_url())
        return
    old_mime = blobwrapper.getContentType()
    LOG.debug('Filename "%s" Mimetype "%s"', filename, old_mime)
    kw = {'mimetype': None,
          'filename': filename}
    # this may split the encoded file inside a multibyte character
    try:
        d, f, mimetype = mtr(body[:8096], **kw)
    except UnicodeDecodeError:
        d, f, mimetype = mtr(len(body) < 8096 and body or '', **kw)

    if mimetype != old_mime:
        LOG.info(
            'Update to new mime_type (%s) of field "%s" of %s', mimetype,
            field.getName(),
            obj.absolute_url()
            )
        blobwrapper.setContentType(mimetype)
    else:
        LOG.debug(
            'Do not update field "%s" of %s',
            field.getName(),
            obj.absolute_url()
            )


def migrate(portal, query={}):
    walker = AllCatalogWalker(portal, UpdateMimetypes, query=query)
    walker()
