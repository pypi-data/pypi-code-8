from __future__ import absolute_import

__all__ = ['DocSection', 'Endpoint', 'StatsMixin']

import logging

from datetime import datetime, timedelta
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
from enum import Enum
from pytz import utc
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from sentry.app import tsdb
from sentry.utils.cursors import Cursor

from .authentication import ApiKeyAuthentication, ProjectKeyAuthentication
from .paginator import Paginator
from .permissions import NoPermission


ONE_MINUTE = 60
ONE_HOUR = ONE_MINUTE * 60
ONE_DAY = ONE_HOUR * 24

LINK_HEADER = '<{uri}&cursor={cursor}>; rel="{name}"; results="{has_results}"; cursor="{cursor}"'

DEFAULT_AUTHENTICATION = (
    ApiKeyAuthentication,
    ProjectKeyAuthentication,
    SessionAuthentication
)


class DocSection(Enum):
    ACCOUNTS = 'Accounts'
    EVENTS = 'Events'
    ORGANIZATIONS = 'Organizations'
    PROJECTS = 'Projects'
    RELEASES = 'Releases'
    TEAMS = 'Teams'


class Endpoint(APIView):
    authentication_classes = DEFAULT_AUTHENTICATION
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)
    permission_classes = (NoPermission,)

    def build_cursor_link(self, request, name, cursor):
        querystring = u'&'.join(
            u'{0}={1}'.format(urlquote(k), urlquote(v))
            for k, v in request.GET.iteritems()
            if k != 'cursor'
        )
        base_url = request.build_absolute_uri(request.path)
        if querystring:
            base_url = '{0}?{1}'.format(base_url, querystring)
        else:
            base_url = base_url + '?'

        return LINK_HEADER.format(
            uri=base_url,
            cursor=str(cursor),
            name=name,
            has_results='true' if bool(cursor) else 'false',
        )

    def convert_args(self, request, *args, **kwargs):
        return (args, kwargs)

    def handle_exception(self, exc):
        try:
            return super(Endpoint, self).handle_exception(exc)
        except Exception as exc:
            logging.exception(unicode(exc))
            return Response({'detail': 'Internal Error'}, status=500)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """
        Identical to rest framework's dispatch except we add the ability
        to convert arguments (for common URL params).
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)

                (args, kwargs) = self.convert_args(request, *args, **kwargs)
                self.args = args
                self.kwargs = kwargs
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def paginate(self, request, on_results=None, paginator_cls=Paginator,
                 **kwargs):
        per_page = int(request.GET.get('per_page', 100))
        input_cursor = request.GET.get('cursor')
        if input_cursor:
            input_cursor = Cursor.from_string(input_cursor)

        assert per_page <= 100

        paginator = paginator_cls(**kwargs)
        cursor_result = paginator.get_result(
            limit=per_page,
            cursor=input_cursor,
        )

        # map results based on callback
        if on_results:
            results = on_results(cursor_result.results)

        headers = {}
        headers['Link'] = ', '.join([
            self.build_cursor_link(request, 'previous', cursor_result.prev),
            self.build_cursor_link(request, 'next', cursor_result.next),
        ])

        return Response(results, headers=headers)


class StatsMixin(object):
    def _parse_args(self, request):
        resolution = request.GET.get('resolution')
        if resolution:
            resolution = self._parse_resolution(resolution)

            assert any(r for r in tsdb.rollups if r[0] == resolution)

        end = request.GET.get('until')
        if end:
            end = datetime.fromtimestamp(float(end)).replace(tzinfo=utc)
        else:
            end = datetime.utcnow().replace(tzinfo=utc)

        start = request.GET.get('since')
        if start:
            start = datetime.fromtimestamp(float(start)).replace(tzinfo=utc)
        else:
            start = end - timedelta(days=1, seconds=-1)

        return {
            'start': start,
            'end': end,
            'rollup': resolution,
        }

    def _parse_resolution(self, value):
        if value.endswith('h'):
            return int(value[:-1]) * ONE_HOUR
        elif value.endswith('d'):
            return int(value[:-1]) * ONE_DAY
        elif value.endswith('m'):
            return int(value[:-1]) * ONE_MINUTE
        elif value.endswith('s'):
            return int(value[:-1])
        else:
            raise ValueError(value)
