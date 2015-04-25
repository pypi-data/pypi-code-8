'''GitHub Sloth CI validator that validates the `GitHub <https://github.com/>`_ payload against username and repo name (obtained from the Sloth app config).

Usage in the app config::

    provider:
        github:
            # Repository owner. Mandatory parameter.
            owner: moigagoo

            # Repository title as it appears in the URL, i.e. slug.
            # Mandatory parameter.
            repo: sloth-ci

            # Only pushes to these branches will initiate a build.
            # Skip this parameter to allow all branches to fire builds.
            branches:
                - master
                - staging
'''


__title__ = 'sloth-ci.validators.github'
__description__ = 'GitHub validator for Sloth CI'
__version__ = '1.0.6'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def validate(request, validation_data):
    '''Validate GitHub payload against repo name (obtained from the Sloth app config).

    :param request_params: payload to validate
    :param validation_data: dictionary with the keys ``owner``, ``repo``, and ``branches``

    :returns: (status, message, list of extracted param dicts)
    '''

    from json import loads

    from ipaddress import ip_network

    if request.method != 'POST':
        return (405, 'Payload validation failed: Wrong method, POST expected, got %s.' % request.method, [])

    trusted_ips = ip_network('192.30.252.0/22')

    remote_ip = request.remote.ip

    if remote_ip not in trusted_ips:
        return (403, 'Payload validation failed: Unverified remote IP: %s.' % remote_ip, [])

    try:
        payload = request.params.get('payload')

        parsed_payload = loads(payload)

        owner = parsed_payload['repository']['owner']['name']

        if owner != validation_data['owner']:
            return (403, 'Payload validation failed: wrong owner: %s' % owner, [])

        repo = parsed_payload['repository']['name']

        if repo != validation_data['repo']:
            return (403, 'Payload validation failed: wrong repository: %s' % repo, [])

        branch = {parsed_payload['ref'].split('/')[-1]}

        allowed_branches = set(validation_data.get('branches', branches))

        if not branches & allowed_branches:
            return (403, 'Payload validation failed: wrong branches: %s' % branches, [])

        return (200, 'Payload validated. Branch: %s' % branch, [{'branch': branch}])

    except Exception as e:
        return (400, 'Payload validation failed: %s' % e, [])