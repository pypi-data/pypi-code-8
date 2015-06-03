import requests
from flask import current_app

from imgtohttps import storage
from imgtohttps.lib import Link


def has_secure_domain(link):
    """ Check if given link can be served over HTTPS

    :type link: Link
    :param link: Link to check
    :return: Existence of secure domain
    :rtype: bool
    """

    try:
        resp = requests.head(link.secure, timeout=3)
    except requests.exceptions.RequestException:
        storage.insecure_domains.add(link)
        return False

    if resp.status_code == 200:
        storage.secure_domains.add(link)
        return True
    else:
        storage.insecure_domains.add(link)
        return False


def upload(link):
    """ Upload image to Imgur

    :type link: Link
    :param link: Link instance
    :return: Link to uploaded image
    :rtype: Link
    :raise ImgError:
    """

    result = current_app.imgur_client.upload_from_url(link.url)
    uploaded = Link(result['link'])
    storage.image_registry.update(result)
    storage.already_uploaded_links.add(link, uploaded)
    return uploaded


def process(raw_link):
    """ Process URL and return possible secure alternative
    or url for uploaded image

    :type raw_link: str
    :param raw_link: Raw url
    :return: Processed url
    :rtype: str
    """

    link = Link(raw_link)

    if link in storage.already_uploaded_links:
        result = storage.already_uploaded_links[link]
    elif link in storage.insecure_domains:
        result = upload(link)
    elif link.is_secure or link in storage.secure_domains or has_secure_domain(link):
        result = link
    else:
        result = upload(link)
    return result.secure
