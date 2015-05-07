# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com


from assetcloud.models import Asset, IndexState
from haystack import connections
import datetime
import logging
import threading


log = logging.getLogger('assetcloud')


status = threading.local()


STATUS_IN_PROGRESS = 'in progress'
STATUS_IN_PROGRESS_UPDATE_NEEDED = 'update needed'


class UpdateIndexMiddleware(object):
    """
    Middleware that updates the index at the end of the request instead of
    during the request. Allows index updates to be batched up.

    Used by DeferredSearchIndex.

    Must come ABOVE TransactionMiddleware (if present) in MIDDLEWARE_CLASSES
    so that UpdateIndexMiddleware.process_response() is run without a
    transaction.

    Hmm, actually might be OK for it to be above OR below, not sure, my brain
    hurts so I am just going to put it above for now.
    """

    def process_request(self, request):
        status.status = STATUS_IN_PROGRESS

        return None

    def process_response(self, request, response):
        if getattr(status, 'status', None) is None:
            log.warning("process_response() was called without process_request(), "
                        "which means that some indexing may have been done during the request instead of at the end. "
                        "This can happen if another middleware's process_request() returned non-None "
                        "(see https://docs.djangoproject.com/en/1.4/topics/http/middleware/#process-request)")
        elif status.status == STATUS_IN_PROGRESS_UPDATE_NEEDED:
            update_index()

        status.status = None  # not in progress

        return response


def update_index_maybe_later():
    if getattr(status, 'status', None) is None:
        # No request in progress or UpdateIndexMiddleware not in use, update now
        update_index()
    else:
        # Request in progress, get UpdateIndexMiddleware to update index at
        # end of request
        status.status = STATUS_IN_PROGRESS_UPDATE_NEEDED


def update_index():
    start_time = datetime.datetime.now()

    assets = get_assets_to_index()
    connections['default'].get_unified_index().get_index(Asset).update_objects(assets)

    set_index_last_updated(start_time)


def get_assets_to_index():
    last_updated = index_last_updated()
    return Asset.unrestricted_objects.filter(modified__gte=last_updated)


def index_last_updated():
    return IndexState.objects.get().updated


def set_index_last_updated(time):
    state = IndexState.objects.get()
    state.updated = time
    state.save()
