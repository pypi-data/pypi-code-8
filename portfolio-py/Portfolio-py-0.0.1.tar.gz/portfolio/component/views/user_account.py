"""
User Account
"""

import os
import datetime
from hashlib import sha1
import time
import base64
import hmac
import urllib
from flask import make_response
from portfolio import (Portfolio, utils, route, abort, redirect, request, url_for,
                   jsonify, session, AppError)
from portfolio.component import (mailer, storage, recaptcha)
from flask_login import (LoginManager, login_required, login_user, logout_user,
                         current_user)

from authomatic import Authomatic
from authomatic.providers import oauth1, oauth2
from authomatic.adapters import WerkzeugAdapter


class PortfolioAuthomatic(object):
    auth = None
    result = None
    _user_updated = False
    config = {}

    def init_app(self, app):
        secret = app.config.get("SECRET_KEY")
        _config = app.config.get("USER_ACCOUNT_AUTH_CREDENTIALS")
        auth_providers = []

        for key, conf in _config.items():
            if "class_" not in conf:
                class_ = None
                if hasattr(oauth2, key):
                    class_ = getattr(oauth2, key)
                elif hasattr(oauth1, key):
                    class_ = getattr(oauth1, key)
                if class_:
                    conf["class_"] = class_
            _key = key.lower()
            auth_providers.append(_key)
            self.config[_key] = conf

        self.auth = Authomatic(
            config=self.config,
            secret=secret,
            session=session,
            report_errors=True
        )

        Portfolio.set_context__(AUTH_PROVIDERS=auth_providers)

    def login(self, provider):
        response = make_response()
        adapter = WerkzeugAdapter(request, response)
        return self.auth.login(adapter=adapter,
                               provider_name=provider,
                               session=session,
                               session_saver=self._session_saver)

    def _session_saver(self):
        session.modified = True

auth = PortfolioAuthomatic()
Portfolio.bind(auth.init_app)


def user_account(model, **kwargs):
    """
    This view is extendable

    kwargs:
        - on_signin_view
        - on_signout_view
        - template_dir

    """
    def wrapper(view):

        Portfolio.set_context__(COMPONENT_LOGIN=True)
        view_name = view.__name__
        User = model.UserModel.User

        # Login
        login_view = "%s:login" % view_name
        on_signin_view = kwargs["on_signin_view"] if "on_signin_view" \
                                                     in kwargs else "Index:index"
        on_signout_view = kwargs["on_signout_view"] if "on_signout_view" \
                                                       in kwargs else "Index:index"
        template_dir = kwargs["template_dir"] if "template_dir" \
                                                 in kwargs else "Portfolio/UserAccount"
        template_page = template_dir + "/%s.html"

        login_manager = LoginManager()
        login_manager.login_view = login_view
        login_manager.login_message_category = "error"
        Portfolio.bind(login_manager.init_app)

        @login_manager.user_loader
        def load_user(userid):
            return User.get(userid)

        @view.extends__
        class Login(object):

            SESSION_KEY_SET_EMAIL_DATA = "set_email_tmp_data"

            def _can_login(self):
                if not self.get_config__("LOGIN_EMAIL_ENABLE"):
                    abort(403)

            def _can_oauth_login(self):
                if not self.get_config__("LOGIN_OAUTH_ENABLE"):
                    abort(403)

            def _can_signup(self):
                if not self.get_config__("LOGIN_SIGNUP_ENABLE"):
                    abort(403)

            def _login_user(self, user_context):
                login_user(user_context)
                user_context.update_last_login()
                user_context.update_last_visited()

            @classmethod
            def signup_handler(cls):
                """
                To handle the signup process. Must still bind to the app
                 :returns User object:
                """
                if request.method == "POST":
                    name = request.form.get("name")
                    email = request.form.get("email")
                    password = request.form.get("password")
                    password2 = request.form.get("password2")
                    profile_pic_url = request.form.get("profile_pic_url", None)

                    if not name:
                        raise UserWarning("Name is required")
                    elif not utils.is_valid_email(email):
                        raise UserWarning("Invalid email address '%s'" % email)
                    elif not password.strip() or password.strip() != password2.strip():
                        raise UserWarning("Passwords don't match")
                    elif not utils.is_valid_password(password):
                        raise UserWarning("Invalid password")
                    else:
                        return User.new(email=email,
                                        password=password.strip(),
                                        name=name,
                                        profile_pic_url=profile_pic_url,
                                        signup_method="EMAIL")

            @classmethod
            def change_login_handler(cls, user_context=None, email=None):
                if not user_context:
                    user_context = current_user
                if not email:
                    email = request.form.get("email").strip()

                if not utils.is_valid_email(email):
                    raise UserWarning("Invalid email address '%s'" % email)
                else:
                    if email != user_context.email and User.get_by_email(email):
                        raise UserWarning("Email exists already '%s'" % email)
                    elif email != user_context.email:
                        user_context.update(email=email)
                        return True
                return False

            @classmethod
            def change_password_handler(cls, user_context=None, password=None,
                                        password2=None):
                if not user_context:
                    user_context = current_user
                if not password:
                    password = request.form.get("password").strip()
                if not password2:
                    password2 = request.form.get("password2").strip()

                if password:
                    if password != password2:
                        raise UserWarning("Password don't match")
                    elif not utils.is_valid_password(password):
                        raise UserWarning("Invalid password")
                    else:
                        user_context.set_password(password)
                        return True
                else:
                    raise UserWarning("Password is empty")

            @classmethod
            def reset_password_handler(cls, user_context=None,
                                       delivery=None,
                                       send_notification=True):
                """
                Reset the password
                :returns string: The new password string
                """
                if not user_context:
                    user_context = current_user

                user = user_context
                method_ = cls.get_config__("LOGIN_RESET_PASSWORD_METHOD", "").upper()
                new_password = None
                if method_ == "TOKEN":
                    token = user.set_reset_password_token()
                    url = url_for("UserAccount:reset_password_token",
                                  token=token,
                                  _external=True)
                else:
                    new_password = user.set_random_password()
                    url = url_for("UserAccount:login", _external=True)

                mailer.send_template("reset-password.txt",
                                     method_=method_,
                                     to=user.email,
                                     name=user.email,
                                     url=url,
                                     new_password=new_password)

            @route("sign_s3_upload", endpoint="UserAccount:sign_s3_upload")
            def sign_s3_upload(self):
                """
                Allow to create Signed object to upload to S3 via JS
                """
                AWS_ACCESS_KEY = self.get_config__('AWS_ACCESS_KEY_ID')
                AWS_SECRET_KEY = self.get_config__('AWS_SECRET_ACCESS_KEY')
                S3_BUCKET = self.get_config__('AWS_S3_BUCKET_NAME')

                object_name = request.args.get('s3_object_name')
                mime_type = request.args.get('s3_object_type')
                expires = long(time.time()+10)
                amz_headers = "x-amz-acl:public-read"
                put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)
                signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
                signature = urllib.quote(urllib.quote_plus(signature.strip()))
                url = 'https://s3.amazonaws.com/%s/%s' % (S3_BUCKET, object_name)
                return jsonify({
                    'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
                     'url': url
                  })

            @route("login/", endpoint="UserAccount:login")
            def login(self):
                """ Login page """
                self._can_login()
                logout_user()
                self.set_meta__(title="Login")
                return self.render(login_url_next=request.args.get("next", ""),
                                   view_template=template_page % "login")

            @route("login/auth/<provider>", endpoint="UserAccount:login_auth", methods=["GET", "POST"])
            def login_auth(self, provider):
                provider = provider.lower()
                result = auth.login(provider)
                print result
                if result:
                    print result.error
                    return self.render(popup_js=result.popup_js(),
                                       view_template=template_page % "login_auth")

                    auth_user = result.user
                    if auth_user:
                        auth_user.update()
                    return self.render(result=result)
                print(result)
                return make_response()
                return provider

            @route("logout/", endpoint="UserAccount:logout")
            def logout(self):
                logout_user()
                self.flash_success__("Logout successfully!")
                return redirect(url_for(on_signout_view or login_view))

            @route("signup/", methods=["GET", "POST"], endpoint="UserAccount:signup")
            def signup(self):
                self._can_login()
                self._can_signup()
                self.set_meta__(title="Signup")
                if request.method == "POST":
                    # reCaptcha
                    if not recaptcha.verify():
                        self.flash_error__("Invalid Security code")
                        return redirect(url_for("UserAccount:signup", next=request.form.get("next")))
                    try:
                        new_account = self.signup_handler()
                        login_user(new_account)
                        self.flash_success__("Congratulations! ")
                        return redirect(request.form.get("next") or url_for(on_signin_view))
                    except Exception as ex:
                        self.flash_error__(ex.message)
                    return redirect(url_for("%s:signup" % view_name, next=request.form.get("next")))

                logout_user()
                return self.render(login_url_next=request.args.get("next", ""),
                                   view_template=template_page % "signup")

            @route("lost-password/", methods=["GET", "POST"], endpoint="UserAccount:lost_password")
            def lost_password(self):
                self._can_login()
                self.set_meta__(title="Lost Password")
                if request.method == "POST":
                    email = request.form.get("email")
                    user = User.get_by_email(email)
                    if user:
                        delivery = self.get_config__("LOGIN_RESET_PASSWORD_DELIVERY")
                        self.reset_password_handler(user_context=user, delivery=delivery)
                        self.flash_success__("A new password has been sent to '%s'" % email)
                    else:
                        self.flash_error__("Invalid email address")
                    return redirect(url_for(login_view))
                else:
                    logout_user()
                    return self.render(view_template=template_page % "lost_password")

            @route("email-login/", methods=["POST"], endpoint="UserAccount:email_login")
            def email_login(self):
                """ login via email """
                self._can_login()

                email = request.form.get("email").strip()
                password = request.form.get("password").strip()

                if not email or not password:
                    self.flash_error__("Email or Password is empty")
                    return redirect(url_for(login_view, next=request.form.get("next")))
                account = User.get_by_email(email)
                if account and account.password_matched(password):
                    self._login_user(account)
                    return redirect(request.form.get("next") or url_for(on_signin_view))
                else:
                    self.flash_error__("Email or Password is invalid")
                    return redirect(url_for(login_view, next=request.form.get("next")))

            # OAUTH Login
            @route("oauth-login/", methods=["POST"], endpoint="UserAccount:oauth_login")
            def oauth_login(self):
                """ To login via social """
                self._can_oauth_login()

                email = request.form.get("email").strip()
                name = request.form.get("name").strip()
                provider = request.form.get("provider").strip()
                provider_user_id = request.form.get("provider_user_id").strip()
                image_url = request.form.get("image_url").strip()
                next = request.form.get("next", "")
                # save to session and redirect to enter email address
                if not email:
                    session[self.SESSION_KEY_SET_EMAIL_DATA] = {
                        "type": "social_login",
                        "email": email,
                        "name": name,
                        "provider": provider,
                        "provider_user_id": provider_user_id,
                        "image_url": image_url,
                        "next": next,
                        "signup_method": "SOCIAL:%s" % provider.upper()
                    }
                    return redirect(url_for("UserAccount:set_email", next=request.form.get("next", "")))
                else:
                    user = User.oauth_register(provider=provider,
                                               provider_user_id=provider_user_id,
                                               email=email,
                                               name=name,
                                               image_url=image_url,
                                               signup_method="SOCIAL:%s" % provider.upper())
                    if user:
                        self._login_user(user)
                        return redirect(request.form.get("next") or url_for(on_signin_view))

                return redirect(url_for(login_view, next=request.form.get("next", "")))

            @route("reset-password-token/<token>", endpoint="UserAccount:reset_password_token")
            def reset_password_token(self, token):
                self._can_login()
                user = User.get_by_token(token)
                if not user:
                    self.flash_error__("Invalid reset password token. Please try again")
                    return redirect(url_for("%s:lost_password" % view_name))
                else:
                    self._login_user(user)
                    return redirect(url_for("%s:reset_password" % view_name))

            @route("reset-password/", methods=["GET", "POST"], endpoint="UserAccount:reset_password")
            @login_required
            def reset_password(self):
                self._can_login()
                self.set_meta__(title="Reset Password")
                if current_user.require_password_change:
                    if request.method == "POST":
                        try:
                            self.change_password_handler()
                            current_user.clear_reset_password_token()
                            self.flash_success__("Password updated successfully!")
                            return redirect(url_for(on_signin_view))
                        except Exception as ex:
                            self.flash_error__("Error: %s" % ex.message)
                            return redirect(url_for("%s:reset_password" % view_name))
                    return self.render(view_template=template_page % "reset_password")
                return redirect(url_for(on_signin_view))

            @route("set-email/", methods=["GET", "POST"], endpoint="UserAccount:set_email")
            @login_required
            def set_email(self):
                self._can_login()
                self.set_meta__(title="Set Email")

                # Only user without email can set email
                if current_user.email:
                    return redirect(url_for("%s:account_settings" % view_name))

                if request.method == "POST":
                    email = request.form.get("email")
                    if not utils.is_valid_email(email):
                        self.flash_error__("Invalid email address '%s'" % email)
                        return redirect(url_for(login_view))

                    if email and self.SESSION_KEY_SET_EMAIL_DATA in session:
                        _data = session[self.SESSION_KEY_SET_EMAIL_DATA]
                        user = User.get_by_email(email)
                        if user:
                            self.flash_error__("An account is already using '%s'" % email)
                        else:
                            User.new(email=email,
                                     name=_data["name"],
                                     signup_method=_data["signup_method"] if "signup_method" in _data else "" )

                            if "type" in _data:
                                if _data["type"] == "social_login":
                                    user = User.social_login(provider=_data["provider"],
                                                             provider_user_id=_data["provider_user_id"],
                                                             email=email,
                                                             name=_data["name"],
                                                             image_url=_data["image_url"])
                                    return redirect(request.form.get("next") or url_for(on_signin_view))

                        return redirect(url_for("%s:set_email" % view_name,
                                                next=request.form.get("next", "")))
                else:
                    return self.render(view_template=template_page % "set_email")

            @route("account-settings", endpoint="UserAccount:account_settings")
            @login_required
            def account_settings(self):
                self.set_meta__(title="Account Settings")
                return self.render(view_template=template_page % "account_settings")

            @route("oauth-connect", methods=["POST"], endpoint="UserAccount:oauth_connect")
            @login_required
            def oauth_connect(self):
                """ To login via social """
                email = request.form.get("email").strip()
                name = request.form.get("name").strip()
                provider = request.form.get("provider").strip()
                provider_user_id = request.form.get("provider_user_id").strip()
                image_url = request.form.get("image_url").strip()
                next = request.form.get("next", "")
                try:
                    current_user.oauth_connect(provider=provider,
                                             provider_user_id=provider_user_id,
                                             email=email,
                                             name=name,
                                             image_url=image_url)
                except Exception as ex:
                    self.flash_error__("Unable to link your account")

                return redirect(url_for("%s:account_settings" % view_name))

            @route("change-login", methods=["POST"], endpoint="UserAccount:change_login")
            @login_required
            def change_login(self):
                confirm_password = request.form.get("confirm-password").strip()
                try:
                    if current_user.password_matched(confirm_password):
                        self.change_login_handler()
                        self.flash_success__("Login Info updated successfully!")
                    else:
                        self.flash_error__("Invalid password")
                except Exception as ex:
                    self.flash_error__("Error: %s" % ex.message)
                return redirect(url_for("UserAccount:account_settings"))

            @route("change-password", methods=["POST"], endpoint="UserAccount:change_password")
            @login_required
            def change_password(self):
                try:
                    confirm_password = request.form.get("confirm-password").strip()
                    if current_user.password_matched(confirm_password):
                        self.change_password_handler()
                        self.flash_success__("Password updated successfully!")
                    else:
                        self.flash_error__("Invalid password")
                except Exception as ex:
                    self.flash_error__("Error: %s" % ex.message)
                return redirect(url_for("UserAccount:account_settings"))

            @route("change-info", methods=["POST"], endpoint="UserAccount:change_info")
            @login_required
            def change_info(self):
                name = request.form.get("name").strip()
                profile_pic_url = request.form.get("profile_pic_url", "").strip()

                data = {}
                if name and name != current_user.name:
                    data.update({"name": name})
                if profile_pic_url:
                    data.update({"profile_pic_url": profile_pic_url})
                if data:
                    current_user.update(**data)
                    self.flash_success__("Account info updated successfully!")
                return redirect(url_for("UserAccount:account_settings"))

            @route("change-profile-pic", methods=["POST"], endpoint="UserAccount:change_profile_pic")
            @login_required
            def change_profile_pic(self):
                profile_pic_url = request.form.get("profile_pic_url").strip()
                _ajax = request.form.get("_ajax", None)
                if profile_pic_url:
                    current_user.update(profile_pic_url=profile_pic_url)
                if _ajax:
                    return jsonify({})
                return redirect(url_for("UserAccount:account_settings"))

        return view
    return wrapper

