# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud.model_shortcuts import get_or_none
from assetcloud.models import Account, DomainPartValidator, ReservedDomainValidator, get_user_profile_class
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views, load_backend, login as auth_login
from django.contrib.auth.views import logout as logout_user
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from assetcloud.views.decorators import public
import assetcloud_auth
import assetcloud_auth.forms
import json
import logging
import social_auth.views


UserProfile = get_user_profile_class()


@public
def login(request):
    return views.login(request,
                       template_name='assetcloud/pages/logged_out/login.html',
                       authentication_form=assetcloud_auth.forms.LoginForm)


@public
def register(request):
    post_data = request.POST or None

    account_form = assetcloud_auth.forms.AccountForm(post_data)
    register_user_form = assetcloud_auth.forms.RegisterUserForm(post_data)

    if account_form.is_valid() and register_user_form.is_valid():
        account = account_form.save()

        user = UserProfile.register_new_user(
            account=account,
            request=request,
            **register_user_form.cleaned_data)

        profile = user.get_profile()
        if profile.activation_email_sent:
            return render(request,
                          'assetcloud/pages/registration/activation_sent.html',
                          {'email': user.email})
        elif profile.is_complete:
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            logging.error('Incomplete profile at register but not email sent? User Id: %s' % user.id)

    return render(request,
                  'assetcloud/pages/registration/register.html',
                  {'account_form': account_form,
                   'register_user_form': register_user_form})


@public
def logout(request):
    redirect_url = getattr(settings,
                           'LOGOUT_REDIRECT_URL',
                           settings.LOGIN_URL)
    return logout_user(request, redirect_url)


@public
def forgotten_password(request):
    form = assetcloud_auth.forms.ForgottenPasswordForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        user.get_profile().send_forgotten_password_email(request)
        return redirect('forgotten-password-email-sent')

    context = {'form': form}
    return render(request, 'assetcloud/pages/user_profile/forgotten_password.html', context)


@public
def forgotten_password_email_sent(request):
    return render(request,
                  'assetcloud/pages/user_profile/forgotten_password_email_sent.html')


@public
def password_reset(request, key):
    profile = get_or_none(UserProfile, activation_key=key)
    if profile is None:
        return render(request,
                      'assetcloud/pages/registration/invalid_reactivation_key.html')

    user = profile.user
    form = assetcloud_auth.forms.ResetPasswordForm(user, request.POST or None)

    if form.is_valid():
        form.save()  # TODO: return (user, password)
        assetcloud_auth.login_user(request, user)
        assetcloud_auth.notify_password_change(request)
        return redirect(settings.LOGIN_REDIRECT_URL)

    context = dict(form=form)
    return render(request, 'assetcloud/pages/logged_out/password_reset.html', context)


def change_password(request, section):
    form = assetcloud_auth.forms.ChangePasswordForm(request.user, request.POST or None)

    if form.is_valid():
        form.save()
        assetcloud_auth.notify_password_change(request)
        return redirect(settings.LOGIN_REDIRECT_URL)

    context = {'form': form, 'section': section}
    return render(request, 'assetcloud/pages/user_profile/password_change_form.html', context)


@public
def activate_user(request, key, form=None):
    profile = get_or_none(UserProfile, activation_key=key)
    if profile is None:
        return render(request, 'assetcloud/pages/registration/invalid_activation_key.html')

    user = profile.user

    form = assetcloud_auth.forms.ActivateUserForm(user, request.POST or None)

    if form.is_valid():
        password = form.cleaned_data['new_password1']
        if password:
            user.set_password(password)

    if profile.can_be_activated():
        profile.activate(request)
        assetcloud_auth.login_user(request, user)
        messages.add_message(request, messages.SUCCESS,
                             'Your %s account is now active!' % settings.PROJECT_NAME)
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'assetcloud/pages/registration/activate_user.html', {
            'form': form,
            'user': user
            })


@assetcloud_auth.require_account_admin
def user_add(request):
    form = assetcloud_auth.forms.CreateUserForm(
        request.POST or None,
        initial={
            'role': UserProfile.ROLE_VIEWER
    })
    if request.POST:
        if form.is_valid(request.account):
            user = UserProfile.create_account_user(
                account=request.account,
                request=request,
                **form.cleaned_data)

            if user.get_profile().activation_email_sent:
                messages.add_message(request, messages.SUCCESS,
                                     'Created user "%s". The user will need to '
                                     'check their email, and activate '
                                     'their account.' % user.email)
            else:
                messages.add_message(request, messages.ERROR,
                                     'There was a problem creating the user - an activation email may not have been sent. Please contact support.')
                logging.error('Error - created user but activation not sent? Creator Id: %s, New user id: %s' % (request.user.id, user.id))
            return http.HttpResponse('OK')

    context = {'form': form}
    return render(request, 'assetcloud/forms/update_user_form.html', context)


@assetcloud_auth.require_account_admin
def user_update(request, id=None):
    user = get_user_or_404(id)

    if not request.user.get_profile().can_update_user(user):
        return http.HttpResponseForbidden()

    form = assetcloud_auth.forms.UpdateUserForm(
        initial={
            'role': user.get_profile().role
            },
        data=request.POST or None)

    form.user = user

    if request.POST:
        if form.is_valid():
            form.save(user)
            messages.add_message(
                request, messages.SUCCESS,
                'Updated user "%s".' % user.email)
        else:
            messages.add_message(
                request, messages.ERROR,
                'Unable to edit user "%s". Please contact support' % user.email)

        return http.HttpResponse('OK')

    context = {'form': form}
    return render(request, 'assetcloud/forms/update_user_form.html', context)


@assetcloud_auth.require_account_admin
def delete_user(request, id):
    """
    The user is not actually deleted from the system, they are merely
    de-activated.
    """
    user = get_or_none(User, id=id)
    if user is None:
        return http.HttpResponseNotFound()

    if not request.user.get_profile().can_delete_user(user):
        return http.HttpResponseForbidden()

    user.get_profile().delete_user(domain=get_current_site(request).domain)
    assetcloud_auth.notify_user_deleted(request, user)

    if user == request.user:
        logout(request)
        return redirect('login')

    return redirect('account-users')


@public
def complete_profile(request, user_id, key):
    try:
        user = User.objects.get(pk=user_id)
        profile = user.get_profile()

        if profile.activation_key == key:
            if not profile.is_registered:
                account_form = assetcloud_auth.forms.AccountForm(
                    request.POST or None,
                    instance=profile.account)
                register_user_form = assetcloud_auth.forms.SocialRegisterUserForm(
                    request.POST or None,
                    initial={'email': user.email})
                if request.POST and account_form.is_valid() and register_user_form.is_valid():
                    account_form.save()

                    profile.complete_profile(
                        request=request,
                        **register_user_form.cleaned_data)
                    if profile.activation_email_sent:
                        return render(request,
                                      'assetcloud/pages/registration/activation_sent.html',
                                      {'email': user.email})
                    else:
                        return activate_user(request, profile.activation_key)
                return render(request,
                              'assetcloud/pages/registration/social_register.html',
                              {'account_form': account_form,
                               'register_user_form': register_user_form})

            else:
                assetcloud_auth.notify_login_error_message(request, user)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        pass  # Fall through to login view

    return redirect('login')


@public
def social_login(request, backend=''):
    # Log user out before beginning social auth to prevent confusion
    # where the user has multiple social auth grants to the current app
    logout(request)
    request.session['trying_to_log_in'] = True
    return social_auth.views.auth(request, backend=backend)


@public
def social_register(request, backend=''):
    logout(request)
    return social_auth.views.auth(request, backend=backend)


@public
def social_associate(request, backend='', user_id=None, key=None):
    try:
        assoc_user = User.objects.get(pk=user_id)
        profile = assoc_user.get_profile()

        if profile.activation_key == key and profile.is_pending:
            logout(request)

            # Store assoc assoc_user in the session
            request.session['social_assoc_user'] = assoc_user

            return social_auth.views.auth(request, backend=backend)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        pass  # Fall through to login view

    return redirect('login')


def get_user_or_404(id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise http.Http404
    return user


@public
def subdomain_available(request):
    subdomain = request.GET.get('subdomain')
    status = 'invalid'
    if subdomain:
        try:
            DomainPartValidator()(subdomain)
            status = 'unavailable'
            ReservedDomainValidator()(subdomain)
        except ValidationError:
            pass
        else:
            try:
                Account.objects.get(subdomain=subdomain)
            except Account.DoesNotExist:
                status = 'available'
    return http.HttpResponse(json.dumps({'status': status}))


def login_as_user(request, id):
    target_user = get_object_or_404(User, pk=id)
    if request.user.get_profile().can_login_as(target_user):
        if not hasattr(target_user, 'backend'):
            for backend in settings.AUTHENTICATION_BACKENDS:
                if target_user == load_backend(backend).get_user(id):
                    target_user.backend = backend
                    break
        if hasattr(target_user, 'backend'):
            auth_login(request, target_user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return http.HttpResponseForbidden()
