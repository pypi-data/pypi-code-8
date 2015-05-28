##############################################################################
#
# Copyright (c) 2015, 2degrees Limited.
# All Rights Reserved.
#
# This file is part of twapi-authn
# <https://github.com/2degrees/twapi-authn>, which is subject to the
# provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

from twapi_connection.exc import NotFoundError


class AccessTokenError(NotFoundError):
    pass


def claim_access_token(connection, access_token):
    """
    Claim the session identified by access_token and return the associated
    user’s Id (integer).

    """
    path_info = '/sessions/{}/'.format(access_token)
    try:
        user_id = connection.send_post_request(path_info)
    except NotFoundError:
        raise AccessTokenError()

    return user_id


def is_session_active(connection, access_token):
    """Check whether the session identified by access_token is still active."""

    path_info = '/sessions/{}/'.format(access_token)
    try:
        connection.send_head_request(path_info)
    except NotFoundError:
        is_active = False
    else:
        is_active = True

    return is_active
