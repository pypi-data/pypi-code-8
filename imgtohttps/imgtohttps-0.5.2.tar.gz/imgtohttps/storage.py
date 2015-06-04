from flask.ext.redis import FlaskRedis

from imgtohttps.lib import LinkSet, LinksMapping, LinkRegistry, RedisList


storage = FlaskRedis()

secure_domains = LinkSet(storage, 'secure_domains')
insecure_domains = LinkSet(storage, 'insecure_domains')
already_uploaded_links = LinksMapping(storage, 'already_uploaded_links')
image_registry = LinkRegistry(storage, 'image_')
errors_list = RedisList(storage, 'errors')
