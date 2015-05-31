# -*- coding: utf-8 -*-
import json
import sys
from importlib import import_module
import urlparse
from django.dispatch import Signal
from redis import StrictRedis
import django
from .ws_settings import WS_SETTINGS
from websocket_channel.publisher import RedisPublisher
from websocket_channel.subscriber import RedisSubscriber
from .web_socket_message import RedisMessage
#from .publisher import RedisPublisher
import urllib
if django.VERSION[:2] >= (1, 7):
    django.setup()
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest, logger, STATUS_CODE_TEXT
from django.core.exceptions import PermissionDenied
from django import http
from django.utils.encoding import force_str

from django.utils.functional import SimpleLazyObject
from .exceptions import WebSocketError, HandshakeError, UpgradeRequiredError


class WebsocketWSGIServer(object):
    def __init__(self, redis_connection=None):
        """
        redis_connection can be overriden by a mock object.
        """
        self._redis_connection = redis_connection and redis_connection or StrictRedis(**WS_SETTINGS['WS_REDIS'])
        # self.Subscriber = RedisSubscriber
        self.online = 0

    def assure_protocol_requirements(self, environ):
        if environ.get('REQUEST_METHOD') != 'GET':
            raise HandshakeError('HTTP method must be a GET')

        if environ.get('SERVER_PROTOCOL') != 'HTTP/1.1':
            raise HandshakeError('HTTP server protocol must be 1.1')

        if environ.get('HTTP_UPGRADE', '').lower() != 'websocket':
            raise HandshakeError('Client does not wish to upgrade to a websocket')

    def process_request(self, request):
        request.session = None
        request.user = None
        if 'django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE_CLASSES:
            engine = import_module(settings.SESSION_ENGINE)
            session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
            if session_key:
                request.session = engine.SessionStore(session_key)
                if 'django.contrib.auth.middleware.AuthenticationMiddleware' in settings.MIDDLEWARE_CLASSES:
                    from django.contrib.auth import get_user
                    request.user = SimpleLazyObject(lambda: get_user(request))

    def process_subscribe(self, request, recvmsg, subscriber):
        channels = urlparse.parse_qs(recvmsg).get("channel[]")
        if channels:
            comps = str(WS_SETTINGS['CHANNEL_MIDDLEWARE']).split('.')
            module = import_module('.'.join(comps[:-1]))
            [getattr(getattr(module, comps[-1])(), 'process')(request, channel, subscriber) for channel in channels]
        else:
            view = WS_SETTINGS['OTHER_REQUET']
            if view:
                comps = str(view).split('.')
                module = import_module('.'.join(comps[:-1]))
                getattr(module, comps[-1])(request, recvmsg, subscriber)

    def __call__(self, environ, start_response):
        """
        Hijack the main loop from the original thread and listen on events on the Redis
        and the Websocket filedescriptors.
        """
        websocket = None
        subscriber = RedisSubscriber(self._redis_connection)
        try:
            self.assure_protocol_requirements(environ)

            request = WSGIRequest(environ)
            self.process_request(request)
            websocket = self.upgrade_websocket(environ, start_response)
            #监听心跳消息
            subscriber.set_pubsub_channels(request, ['HEARTBEAT'])
            websocket_fd = websocket.get_file_descriptor()
            listening_fds = [websocket_fd]
            redis_fd = subscriber.get_file_descriptor()
            if redis_fd:
                listening_fds.append(redis_fd)
            subscriber.send_persited_messages(websocket)

            self.online += 1
            while websocket and not websocket.closed:
                ready = self.select(listening_fds, [], [], 4.0)[0]
                if not ready:
                    websocket.flush()
                print ready
                for fd in ready:
                    if fd == websocket_fd:
                        recvmsg = RedisMessage(websocket.receive())
                        if recvmsg:
                            self.process_subscribe(request, recvmsg, subscriber)
                    elif fd == redis_fd:
                        sendmsg = RedisMessage(subscriber.parse_response())
                        if sendmsg:
                            websocket.send(sendmsg)
                    else:
                        logger.error('Invalid file descriptor: {0}'.format(fd))
        except WebSocketError as excpt:
            logger.warning('WebSocketError: {}'.format(excpt), exc_info=sys.exc_info())
            response = http.HttpResponse(status=1001, content='Websocket Closed')
        except UpgradeRequiredError as excpt:
            logger.info('Websocket upgrade required')
            response = http.HttpResponseBadRequest(status=426, content=excpt)
        except HandshakeError as excpt:
            logger.warning('HandshakeError: {}'.format(excpt), exc_info=sys.exc_info())
            response = http.HttpResponseBadRequest(content=excpt)
        except PermissionDenied as excpt:
            logger.warning('PermissionDenied: {}'.format(excpt), exc_info=sys.exc_info())
            response = http.HttpResponseForbidden(content=excpt)
        except Exception as excpt:
            logger.error('Other Exception: {}'.format(excpt), exc_info=sys.exc_info())
            response = http.HttpResponseServerError(content=excpt)
        else:
            response = http.HttpResponse()
        finally:
            self.online -= 1
            subscriber.release()
            if websocket:
                websocket.close(code=1001, message='Websocket Closed')
            else:
                logger.warning('Starting late response on websocket')
                status_text = STATUS_CODE_TEXT.get(response.status_code, 'UNKNOWN STATUS CODE')
                status = '{0} {1}'.format(response.status_code, status_text)
                start_response(force_str(status), response._headers.values())
                logger.info('Finish non-websocket response with status code: {}'.format(response.status_code))
        return response


    def upgrade_websocket(self, environ, start_response):
        raise WebSocketError("error")