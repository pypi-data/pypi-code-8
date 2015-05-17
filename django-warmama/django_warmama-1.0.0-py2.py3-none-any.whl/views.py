import logging
import random
import requests
import six
import uuid
from datetime import timedelta
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from ipware.utils import is_valid_ipv4, is_valid_ipv6
from threading import Thread
from warmama import models, exceptions, fields
from warmama.conf import settings
from warmama import decorators
from warmama.serializers import MatchSerializer

logger = logging.getLogger(__name__)


##########
# Thread Workers - TODO move to separate file?
##########


def _remote_login(data):
    """Pass the login request to a remote url

    This asks the remote server to validate a login/password combination. It
    will send the results by calling the callback_url given.
    """
    # TODO - rewrite this and skip `requests`, its a shame to pull it in for this one function

    logger.info('Remote login sending request login: %s, handle: %d', data['login'], data['handle'])
    try:
        r = requests.post(settings.WARMAMA_AUTH_URL, timeout=5, data=data)
    except requests.ConnectionError as e:
        # TODO cleanup login session
        logger.info('Remote login request failed: %s', e)
        return
    except requests.Timeout:
        # TODO retry or cleanup login session
        logger.info('Remote login request timeout login: %s, handle: %d', data['login'], data['handle'])
        return

    logger.info('Remote login response login: %s, handle: %d, response: %s', data['login'], data['handle'], r.text)


##########
# Helpers
##########


def _ipv4_ipv6(ipaddr):
    """Determine if an address is ipv4 or ipv6

    Returns:
        The tuple `(ipv4, ipv6)` where one is the string address and the other
        is an empty string.
    """
    # TODO this is repeated in warmama.decorators, move this to a utils file?
    if is_valid_ipv4(ipaddr):
        return ipaddr, ''
    elif is_valid_ipv6(ipaddr):
        return '', ipaddr

    raise exceptions.BadRequest('Couldnt read IP address for request')


def _ip_flt(ipv4, ipv6):
    """Queryset filter to match either ipv4 or ipv6"""
    assert ipv4 or ipv6, 'One of ipv4, ipv6 must be defined'
    return Q(ip=ipv4) | Q(ipv6=ipv6)


##########
# Base View Classes
##########


class APIMeta(type):
    """Metaclass to transform the `post` method of a view.

    The `post` method is trasformed in the following way:

        - The keyword arguments `POST`, `ipv4`, and `ipv6` are added to the
          method
        - The argument `POST` is the `request.POST` data cleaned and validated
          using the form `View.PostForm`
        - The arguments `ipv4` and `ipv6` is the source ip address for the
          request. It is guaranteed that exactly one of these is a valid address
          and the other is an emtpy string.
        - View exceptions are handled by `warmama.decorators.exception_response`
          and return `View.exc_response` on errors.

    This mainly prevents having to stack infinity decorators on each post method
    """
    def __new__(cls, name, parents, attrs):
        post = attrs.pop('post')
        klass = super(APIMeta, cls).__new__(cls, name, parents, attrs)

        # order matters
        post = decorators.log_args(logger)(post)
        post = method_decorator(decorators.request_ip)(post)
        post = method_decorator(decorators.clean_post_args(klass.PostForm))(post)
        post = decorators.exception_response(klass.exc_response)(post)
        klass.post = post

        return klass


class APIView(six.with_metaclass(APIMeta, View)):
    """Base class for an API endpoint

    Offer benefits from APIMeta and disables CSRF protection.
    """
    exc_response = {'status': 0}

    class PostForm(forms.Form):
        pass

    @classmethod
    def as_view(cls, *args, **kwargs):
        """Disable csrf protection"""
        view = super(APIView, cls).as_view(*args, **kwargs)
        return csrf_exempt(view)

    def post(self, request, *args, **kwargs):
        raise NotImplemented('APIViews must implement a post method')


##########
# View Classes
##########


class ServerLogin(APIView):
    """Server Login

    This allows for one server to have multiple sessions, one session per port.
    """
    exc_response = {'id': 0}

    class PostForm(forms.Form):
        port = forms.IntegerField()
        authkey = forms.CharField(max_length=64)
        hostname = forms.CharField(max_length=64, required=False)
        demos_baseurl = forms.CharField(max_length=128, required=False)

    def post(self, request, POST=None, ipv4='', ipv6=''):
        server = models.Server.objects.get(
            _ip_flt(ipv4, ipv6),
            login=POST['authkey'],
            banned=False,
        )

        server.hostname = POST['hostname']
        server.demos_baseurl = POST['demos_baseurl']
        server.save()

        session, created = models.ServerSession.objects.get_or_create(
            user=server,
            ip=ipv4,
            ipv6=ipv6,
            defaults={'port': POST['port']},
        )

        if not created:
            session.port = POST['port']
            session.save()
            # TODO: reset state (kick players, purge player, etc...)

        return JsonResponse({'id': session.pk})


class ServerLogout(APIView):
    """Server Logout"""
    class PostForm(forms.Form):
        ssession = forms.IntegerField(min_value=1)

    def post(self, request, POST=None, ipv4='', ipv6=''):
        """
        TODO: First remove all purge_players that match this server for all
        players who's server session matches reset their servers or if their
        purgable flag is set, remove them totally
        """
        session = models.ServerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['ssession'],
        )
        logger.info('%s:%d logging off', ipv4 or ipv6, session.port)
        session.delete()
        return JsonResponse({'status': 1})


class ServerClientConnect(APIView):
    """Server client connect"""
    exc_response = {'id': 0}

    class PostForm(forms.Form):
        ssession = forms.IntegerField(min_value=1)
        csession = forms.IntegerField(min_value=1)
        cticket = forms.IntegerField(min_value=1)
        cip = fields.IPAddressField()

    def post(self, request, POST=None, ipv4='', ipv6=''):
        server_session = models.ServerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['ssession'],
        )

        caddr, _ = POST['cip']
        cipv4, cipv6 = _ipv4_ipv6(caddr)
        logger.info(
            'SCC pk %d, tid %d, ts %d, now %s',
            POST['csession'], POST['cticket'], server_session.user_id, timezone.now()
        )
        client_session = models.PlayerSession.objects \
            .select_related('user') \
            .get(
                _ip_flt(cipv4, cipv6),
                pk=POST['csession'],
                ticket_id=POST['cticket'],
                ticket_server=server_session,
                ticket_expiration__gt=timezone.now(),
            )

        logger.info(
            'Attaching client session %s to server session %s',
            client_session, server_session
        )
        client_session.ticket_id = None
        client_session.ticket_server = None
        client_session.ticket_expiration = None
        client_session.server_session = server_session
        client_session.save()

        stats = models.PlayerStat.objects \
                                 .select_related('gametype') \
                                 .filter(player_id=client_session.user_id) \
                                 .order_by('gametype__name')

        data = {
            'id': client_session.pk,
            'login': client_session.user.login,
            'ratings': [{
                'gametype': stat.gametype.name,
                'rating': float(stat.rating),
                'deviation': float(stat.deviation),
            } for stat in stats],
        }
        return JsonResponse(data)


class ServerClientDisconnect(APIView):
    """Server client disconnect"""
    class PostForm(forms.Form):
        ssession = forms.IntegerField(min_value=1)
        csession = forms.IntegerField(min_value=1)
        gameon = forms.IntegerField(required=False)

    def post(self, request, POST=None, ipv4='', ipv6=''):
        server_session = models.ServerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['ssession'],
        )
        client_session = models.PlayerSession.objects.get(
            pk=POST['csession'],
            server_session=server_session,
        )

        if POST['gameon']:
            logger.info('Adding session %d to purgables', client_session.pk)
            models.PurgePlayer.objects.create(
                player_id=client_session.user_id,
                session=client_session,
                server_session=server_session,
            )

        client_session.ticket_id = None
        client_session.ticket_server = None
        client_session.ticket_expiration = None
        client_session.server_session = None
        client_session.save()

        logger.info(
            'ServerClientDisconnect %d %d ok',
            client_session.pk, server_session.pk
        )
        return JsonResponse({'status': 1})


class ServerHeartbeat(APIView):
    """Server heartbeat"""
    class PostForm(forms.Form):
        ssession = forms.IntegerField(min_value=1)

    def post(self, request, POST=None, ipv4='', ipv6=''):
        server_session = models.ServerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['ssession'],
        )

        # this will set the `updated` time
        server_session.save()

        logger.info('Heartbeat from server: %s', ipv4 or ipv6)
        return JsonResponse({'status': 1})


class ServerMatchReport(APIView):
    """Server match report"""
    class PostForm(forms.Form):
        ssession = forms.IntegerField()
        data = fields.GzipJsonField()

    def post(self, request, POST=None, ipv4='', ipv6=''):
        server_session = models.ServerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['ssession'],
        )

        serializer = MatchSerializer(data=POST['data'])
        if not serializer.is_valid():
            raise exceptions.BadRequest(serializer.errors)

        matchresult, matchplayers = serializer.save(server_session=server_session)
        ratings = {
            'gametype': matchresult.gametype.name,
            'ratings': [
                [sessionid, float(matchplayer.newrating)]
                for sessionid, matchplayer in matchplayers.items()
            ]
        }

        # delete purgables, this cascade deletes PurgePlayer objects
        models.PlayerSession.objects \
                            .filter(server_session=server_session, purgable=True) \
                            .delete()

        # TODO: clear server_session.next_match_uuid?

        return JsonResponse({'status': 1, 'ratings': ratings})


class ServerMatchUUID(APIView):
    """Server Match UUID"""
    exc_response = {'uuid': ''}

    class PostForm(forms.Form):
        ssession = forms.IntegerField()

    def post(self, request, POST=None, ipv4='', ipv6=''):
        server_session = models.ServerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['ssession'],
        )

        # TODO: collision check - probably not necessary
        # also, why do we even need to do this here. Best I can tell, gameserver
        # sets this to a configstring which is never actually used.
        server_session.next_match_uuid = str(uuid.uuid4())
        server_session.save()
        logger.info(
            'MatchUUID request from %s, returning %s',
            ipv4 or ipv6, server_session.next_match_uuid
        )
        return JsonResponse({'uuid': server_session.next_match_uuid})


class ClientLogin(APIView):
    """Client Login"""
    exc_response = {'ready': 2, 'id': 0}

    class PostForm(forms.Form):
        login = forms.CharField(max_length=64, required=False)
        passwd = forms.CharField(max_length=64, required=False)
        handle = forms.IntegerField(required=False)

    def _step_one(self, request, POST=None, ipv4='', ipv6=''):
        """Start the login process"""
        logger.info(
            'Clientlogin 1 login: %s, ip: %s',
            POST['login'], ipv4 or ipv6
        )

        # Create LoginPlayer for the login process, handle is pk for this
        # If one already exists for the login, let it error
        login_player = models.LoginPlayer.objects.create(login=POST['login'], ready=False, valid=False)

        if settings.WARMAMA_REMOTE_CLIENTAUTH:
            # Use remote authentication
            # TODO - digest should be a unique identifier to associate the
            # callbacks with this request, need to move `digest` field from
            # PlayerSession to LoginPlayer to do that
            thread_args = ({
                'login': POST['login'],
                'passwd': POST['passwd'],
                'handle': '%d' % login_player.pk,
                'digest': 'something',
                'url': request.build_absolute_uri(reverse('warmama:auth', current_app=request.resolver_match.namespace)),
            },)
            Thread(target=_remote_login, args=thread_args).start()
        else:
            # Use local authentication
            user = authenticate(username=POST['login'], password=POST['passwd'])
            login_player.ready = True
            login_player.valid = bool(user)
            login_player.save()

        return JsonResponse({'ready': -1, 'handle': login_player.pk, 'id': 0})

    def _step_two(self, request, POST=None, ipv4='', ipv6=''):
        """Complete the login process"""
        logger.info(
            'Clientlogin 2 handle: %d, ip: %s',
            POST['handle'], ipv4 or ipv6
        )

        # TODO - ip validation should be done here, but that means modifying
        # the DB schema
        login_player = models.LoginPlayer.objects.get(pk=POST['handle'])

        if not login_player.ready:
            logger.info(
                'Clientlogin 2 not ready. handle: %d, ip: %s',
                POST['handle'], ipv4 or ipv6
            )
            return JsonResponse({'ready': 1, 'id': 0})

        login_player.delete()

        if not login_player.valid:
            raise exceptions.Forbidden('User failed to authenticate')

        # Valid login, make a player session
        # TODO add session digest, still don't know what its used for
        player = models.Player.objects.get(login=login_player.login)
        player_session, created = models.PlayerSession.objects.get_or_create(user=player)

        if not created:
            if player_session.server_session_id:
                raise exceptions.Forbidden('User on server for existing session')

            if player_session.ip != ipv4 and player_session.ipv6 != ipv6:
                raise exceptions.Forbidden('Different IP for existing session')

        player_session.ip = ipv4
        player_session.ipv6 = ipv6
        player_session.purgable = False
        player_session.server_session = None
        player_session.save()

        # Calculate player profile
        stats = models.PlayerStat.objects \
                                 .select_related('gametype') \
                                 .filter(player=player) \
                                 .order_by('gametype__name')
        urlargs = {'session': player_session.pk}

        data = {
            'ready': 2,
            'id': player_session.pk,
            'ratings': [{
                'gametype': stat.gametype.name,
                'rating': float(stat.rating),
                'deviation': float(stat.deviation),
            } for stat in stats],
            'profile_url': login_player.profile_url.format(**urlargs),
            'profile_url_rml': login_player.profile_url_rml.format(**urlargs),
        }
        return JsonResponse(data)

    def post(self, request, POST=None, ipv4='', ipv6=''):
        """
        Returns {'ready': value, 'id': value} for one of the following cases:
            `{'ready': -1, 'handle': handle, 'id': 0}` - handle for the login process
            `{'ready': 1, 'id': 0} - login session isn't ready
            `{'ready': 2, 'id': sessionid } - login session is ready with id `id`
        """
        if POST.get('handle', None):
            return self._step_two(request, POST, ipv4, ipv6)
        else:
            if not POST.get('login', '') or not POST.get('passwd', ''):
                raise exceptions.BadRequest('Login and passwd fields are required')
            return self._step_one(request, POST, ipv4, ipv6)


class ClientLogout(APIView):
    """Client Logout"""
    class PostForm(forms.Form):
        csession = forms.IntegerField(min_value=1)

    def post(self, request, POST=None, ipv4='', ipv6=''):
        client_session = models.PlayerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['csession'],
        )

        logger.info('Client %s logging off', ipv4 or ipv6)

        if hasattr(client_session, 'purge_player'):
            logger.info('Marking session %d purgable', client_session.pk)
            client_session.purgable = True
            client_session.ticket_id = None
            client_session.ticket_server = None
            client_session.ticket_expiration = None
            client_session.server_session = None
            client_session.save()
        else:
            logger.info('Removing session %d', client_session.pk)
            client_session.delete()

        return JsonResponse({'status': 1})


class ClientConnect(APIView):
    """Client Connect"""
    exc_response = {'ticket': 0}

    class PostForm(forms.Form):
        csession = forms.IntegerField(min_value=1)
        saddr = fields.IPAddressField()

    def post(self, request, POST=None, ipv4='', ipv6=''):
        sipv4, sipv6 = _ipv4_ipv6(POST['saddr'][0])  # TODO
        port = POST['saddr'][1] or settings.WARMAMA_DEFAULT_SERVER_PORT

        server_session = models.ServerSession.objects.get(
            _ip_flt(sipv4, sipv6),
            port=port
        )

        client_session = models.PlayerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['csession'],
        )

        logger.info(
            'Found server %d for client %d (addr %s)',
            server_session.pk, client_session.pk, sipv4 or sipv6
        )

        client_session.ticket_id = random.randint(1, 0xfffffff)
        client_session.ticket_server = server_session
        client_session.ticket_expiration = timezone.now() + timedelta(seconds=settings.WARMAMA_TICKET_EXPIRATION)
        client_session.server_session = None
        client_session.save()

        return JsonResponse({'ticket': client_session.ticket_id})


class ClientHeartbeat(APIView):
    """Client Heartbeat"""
    class PostForm(forms.Form):
        csession = forms.IntegerField(min_value=1)

    def post(self, request, POST=None, ipv4='', ipv6=''):
        client_session = models.PlayerSession.objects.get(
            _ip_flt(ipv4, ipv6),
            pk=POST['csession'],
        )

        # this will set the `updated` time
        client_session.save()

        logger.info('Heartbeat from client: %s', ipv4 or ipv6)
        return JsonResponse({'status': 1})


class ClientAuthenticate(APIView):
    """Client Authenticate

    This is the callback endpoint for remote client auth requests
    """
    class PostForm(forms.Form):
        handle = forms.IntegerField(min_value=1)
        digest = forms.CharField(max_length=64)
        valid = forms.BooleanField()
        profile_url = forms.CharField(max_length=255, required=False)
        profile_url_rml = forms.CharField(max_length=255, required=False)

    def post(self, request, POST=None, ipv4='', ipv6=''):
        # TODO validate this with digest

        handle = POST.pop('handle')
        POST.pop('digest')

        models.LoginPlayer.objects.filter(pk=handle).update(**POST)

        return JsonResponse({'status': 1})
