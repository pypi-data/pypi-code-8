
PROVIDERS = [

    'allauth.socialaccount.providers.bitbucket',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google'
]

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
     {'SCOPE': ['email', 'public_profile', 'user_friends'],
      'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
      'METHOD': 'oauth2',
      'LOCALE_FUNC': 'path.to.callable',
      'VERIFIED_EMAIL': False,
      'VERSION': 'v2.3'}}

SOCIALACCOUNT_PROVIDERS = \
    {'google':
        {'SCOPE': ['profile', 'email'],
         'AUTH_PARAMS': {'access_type': 'online'}}}
