from django.shortcuts import redirect
from assetcloud.models import get_user_profile_class
import assetcloud_auth

UserProfile = get_user_profile_class()

import social_auth.exceptions


def pickup_assoc_user(*args, **kwargs):
    assoc_user = kwargs['request'].session.get('social_assoc_user')
    if assoc_user:
        kwargs['request'].session['social_assoc_user'] = None
        assoc_user.get_profile().activate()
        # Settings this will prevent social auth from creating a user
        kwargs['user'] = assoc_user
    return kwargs


def intercept_login(**kwargs):
    if not kwargs.get('user') and kwargs['request'].session.get('trying_to_log_in'):
        assetcloud_auth.notify_no_known_social_account(kwargs['request'], kwargs['backend'])
        raise social_auth.exceptions.StopPipeline()
    return kwargs


def redirect_to_complete_profile(user):
    return redirect('complete_profile_action',
                    user_id=user.id,
                    key=user.get_profile().activation_key)


def login_or_complete_user(*args, **kwargs):
    user = kwargs.get('user')
    if user:
        try:
            profile = user.get_profile()

            # User has a profile - check if their details are complete
            if not profile.is_registered:
                if kwargs.get('details', {}).get('email', '') != '':
                    user.email = kwargs['details']['email']
                    user.save()
                return redirect_to_complete_profile(user)

        except UserProfile.DoesNotExist:
            # User has just been created by social auth
            user = UserProfile.initialise_social_auth_user(user)
            if not user.get_profile().is_registered:
                return redirect_to_complete_profile(user)

    # User is fully registered - notify of any error messages
    assetcloud_auth.notify_login_error_message(kwargs['request'], user)
    return kwargs
