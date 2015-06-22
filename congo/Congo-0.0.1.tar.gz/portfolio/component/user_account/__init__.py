"""
User Account
"""

import datetime
from hashlib import sha1
import time
import base64
import hmac
import urllib
from flask import url_for, request, redirect, abort, session, jsonify, make_response
from portfolio import Portfolio, utils, route
from portfolio.ext import mailer, recaptcha, storage
from portfolio.component import ModelError, ViewError
from flask_login import (LoginManager, login_required, login_user, logout_user,
                         current_user)

from authomatic import Authomatic
from authomatic.providers import oauth1, oauth2
from authomatic.adapters import WerkzeugAdapter


Portfolio.register_component_template_static(__name__)

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

        Portfolio.__(AUTH_PROVIDERS=auth_providers)

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

# The user_model create a fully built model with social signin
def model(db):

    class UserRole(db.Model):
        name = db.Column(db.String(75), index=True)
        level = db.Column(db.Integer, index=True)

        # Primary Roles
        PRIMARY = [(99, "SUPERADMIN"),
                   (98, "ADMIN"),
                   (1, "USER")]

        @classmethod
        def new(cls, name, level):
            name = name.upper()
            role = cls.get_by_name(name)
            if not role:
                role = cls.create(name=name, level=level)
            return role

        @classmethod
        def get_by_name(cls, name):
            name = name.upper()
            return cls.all().filter(cls.name == name).first()

        @classmethod
        def get_by_level(cls, level):
            return cls.all().filter(cls.level == level).first()

    class User(db.Model):

        email = db.Column(db.String(75), index=True, unique=True)
        email_confirmed = db.Column(db.Boolean, default=False)
        password_hash = db.Column(db.String(250))
        require_password_change = db.Column(db.Boolean, default=False)
        reset_password_token = db.Column(db.String(100), index=True)
        reset_password_token_expiration = db.Column(db.DateTime)
        name = db.Column(db.String(250))
        profile_pic_url = db.Column(db.String(250))
        signup_method = db.Column(db.String(250))
        active = db.Column(db.Boolean, default=True, index=True)
        last_login = db.Column(db.DateTime)
        last_visited = db.Column(db.DateTime)
        roles = db.relationship(UserRole, secondary="user_role_role")

        # ------ FLASK-LOGIN REQUIRED METHODS ----------------------------------

        def is_active(self):
            return self.active

        def get_id(self):
            return self.id

        def is_authenticated(self):
            return True

        def is_anonymous(self):
            return False

        # ---------- END FLASK-LOGIN REQUIREMENTS ------------------------------

        @classmethod
        def get_by_email(cls, email):
            """
            Find by email. Useful for logging in users
            """
            return cls.all().filter(cls.email == email).first()

        @classmethod
        def get_by_token(cls, token):
            """
            Find by email. Useful for logging in users
            """
            user = cls.all().filter(cls.reset_password_token == token).first()
            if user:
                now = datetime.datetime.now()
                if user.require_password_change is True \
                        and user.reset_password_token_expiration > now:
                    return user
                else:
                    user.clear_reset_password_token()
            else:
                return None

        @classmethod
        def new(cls, email, password=None, role="USER", **kwargs):
            """
            Register a new user
            """
            user = cls.get_by_email(email)
            if user:
                raise ModelError("User exists already")
            user = cls.create(email=email)
            if password:
                user.set_password(password)
            if kwargs:
                user.update(**kwargs)
            if role:
                role_ = UserRole.get_by_name(role.upper())
                if role_:
                    user.update_roles([role_.id])

            return user

        def password_matched(self, password):
            """
            Check if the password matched the hash
            :returns bool:
            """
            return utils.verify_encrypted_string(password, self.password_hash)

        def set_password(self, password):
            """
            Encrypt the password and save it in the DB
            """
            self.update(password_hash=utils.encrypt_string(password))

        def set_random_password(self):
            """
            Set a random password, saves it and return the readable string
            :returns string:
            """
            password = utils.generate_random_string()
            self.set_password(password)
            return password

        def set_reset_password_token(self, expiration=24):
            """
            Generate password reset token
            It returns the token generated
            """
            expiration = datetime.datetime.now() + datetime.timedelta(hours=expiration)
            while True:
                token = utils.generate_random_string(32).lower()
                if not User.all().filter(User.reset_password_token == token).first():
                    break
            self.update(require_password_change=True,
                        reset_password_token=token,
                        reset_password_token_expiration=expiration)
            return token

        def clear_reset_password_token(self):
            self.update(require_password_change=False,
                        reset_password_token=None,
                        reset_password_token_expiration=None)

        def set_require_password_change(self, req=True):
            self.update(require_password_change=req)

        def update_last_login(self):
            self.update(last_login=datetime.datetime.now())

        def update_last_visited(self):
            self.update(last_visited=datetime.datetime.now())

        @classmethod
        def oauth_register(cls, provider, provider_user_id=None,
                          email=None, name=None, image_url=None,
                          **kwargs):
            """
            Register
            :param provider:
            :param provider_user_id:
            :param email:
            :param name:
            :param image_url:
            :param kwargs:
            :return:
            """
            oal = UserOauthLogin
            oauthuser = oal.all()\
                .filter(oal.provider == provider)\
                .filter(oal.provider_user_id == provider_user_id)\
                .first()
            if oauthuser:
                return oauthuser.user
            else:
                if not email:
                    raise ModelError("Email is missing")

                data = {
                    "provider": provider,
                    "provider_user_id": provider_user_id,
                    "email": email,
                    "name": name,
                    "image_url": image_url
                }

                user = cls.get_by_email(email)
                if user:
                    data.update({"user_id": user.id})
                    oal.create(**data)
                    return user
                else:
                    user = cls.new(email=email,
                                    name=name,
                                    profile_pic_url=image_url,
                                    signin_method=provider)
                    data.update({"user_id": user.id})
                    oal.create(**data)
                    return user

        def oauth_connect(self, provider, provider_user_id=None,
                          email=None, name=None, image_url=None,
                          **kwargs):
            """
            Connect an account an OAUTH
            :param provider:
            :param provider_user_id:
            :param email:
            :param name:
            :param image_url:
            :param kwargs:
            :return:
            """
            oal = UserOauthLogin
            oauthuser = oal.all()\
                .filter(oal.provider == provider)\
                .filter(oal.provider_user_id == provider_user_id)\
                .first()
            if oauthuser:
                if oauthuser.user_id == self.id:
                    return self
                else:
                    raise ModelError("Account is already linked to another user")
            else:
                data = {
                    "provider": provider,
                    "provider_user_id": provider_user_id,
                    "email": email,
                    "name": name,
                    "image_url": image_url,
                    "user_id": self.id
                }
                oal.create(**data)
                return self

        def update_roles(self, roles_list):
            r_list = [r.id for r in self.roles]
            del_roles = list(set(r_list) - set(roles_list))
            new_roles = list(set(roles_list) - set(r_list))
            for dc in del_roles:
                UserRoleRole.remove(user_id=self.id, role_id=dc)
            for nc in new_roles:
                UserRoleRole.add(user_id=self.id, role_id=nc)

    class UserRoleRole(db.Model):
        user_id = db.Column(db.Integer, db.ForeignKey(User.id))
        role_id = db.Column(db.Integer, db.ForeignKey(UserRole.id))

        @classmethod
        def add(cls, user_id, role_id):
            r = cls.all().filter(cls.user_id == user_id)\
                .filter(cls.role_id == role_id)\
                .first()
            if not r:
                cls.create(user_id=user_id, role_id=role_id)

        @classmethod
        def remove(cls, user_id, role_id):
            r = cls.all().filter(cls.user_id == user_id)\
                .filter(cls.role_id == role_id)\
                .first()
            if r:
                r.delete(hard_delete=True)

    class UserOauthLogin(db.Model):
        user_id = db.Column(db.Integer, db.ForeignKey(User.id))
        provider = db.Column(db.String(50), index=True)
        provider_user_id = db.Column(db.String(250))
        name = db.Column(db.String(250))
        email = db.Column(db.String(250))
        image_url = db.Column(db.String(250))
        access_token = db.Column(db.String(250))
        secret = db.Column(db.String(250))
        profile_url = db.Column(db.String(250))
        user = db.relationship(User, backref="oauth_logins")

    return utils.to_struct(User=User,
                           Role=UserRole,
                           RoleRole=UserRoleRole,
                           OauthLogin=UserOauthLogin)

def view(model, **kwargs):
    """
    This view is extendable

    kwargs:
        - on_signin_view
        - on_signout_view
        - template_dir

    """
    def wrapper(view):

        Portfolio.__(COMPONENT_LOGIN=True)
        view_name = view.__name__
        User = model.UserModel.User

        # Login
        login_view = "UserAccount:login"
        on_signin_view = kwargs["on_signin_view"] if "on_signin_view" \
                                                     in kwargs else "Index:index"
        on_signout_view = kwargs["on_signout_view"] if "on_signout_view" \
                                                       in kwargs else "Index:index"
        template_dir = kwargs["template_dir"] if "template_dir" \
                                                 in kwargs else "UserAccount"
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
                if not self.get_config("LOGIN_EMAIL_ENABLE"):
                    abort(403)

            def _can_oauth_login(self):
                if not self.get_config("LOGIN_OAUTH_ENABLE"):
                    abort(403)

            def _can_signup(self):
                if not self.get_config("LOGIN_SIGNUP_ENABLE"):
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
                AWS_ACCESS_KEY = self.get_config('AWS_ACCESS_KEY_ID')
                AWS_SECRET_KEY = self.get_config('AWS_SECRET_ACCESS_KEY')
                S3_BUCKET = self.get_config('AWS_S3_BUCKET_NAME')

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
                self.meta_data(title="Login")
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
                self.flash_success("Logout successfully!")
                return redirect(url_for(on_signout_view or login_view))

            @route("signup/", methods=["GET", "POST"], endpoint="UserAccount:signup")
            def signup(self):
                self._can_login()
                self._can_signup()
                self.meta_data(title="Signup")
                if request.method == "POST":
                    # reCaptcha
                    if not recaptcha.verify():
                        self.flash_error("Invalid Security code")
                        return redirect(url_for("UserAccount:signup", next=request.form.get("next")))
                    try:
                        new_account = self.signup_handler()
                        login_user(new_account)
                        self.flash_success("Congratulations! ")
                        return redirect(request.form.get("next") or url_for(on_signin_view))
                    except Exception as ex:
                        self.flash_error(ex.message)
                    return redirect(url_for("%s:signup" % view_name, next=request.form.get("next")))

                logout_user()
                return self.render(login_url_next=request.args.get("next", ""),
                                   view_template=template_page % "signup")

            @route("lost-password/", methods=["GET", "POST"], endpoint="UserAccount:lost_password")
            def lost_password(self):
                self._can_login()
                self.meta_data(title="Lost Password")
                if request.method == "POST":
                    email = request.form.get("email")
                    user = User.get_by_email(email)
                    if user:
                        delivery = self.get_config("LOGIN_RESET_PASSWORD_DELIVERY")
                        self.reset_password_handler(user_context=user, delivery=delivery)
                        self.flash_success("A new password has been sent to '%s'" % email)
                    else:
                        self.flash_error("Invalid email address")
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
                    self.flash_error("Email or Password is empty")
                    return redirect(url_for(login_view, next=request.form.get("next")))
                account = User.get_by_email(email)
                if account and account.password_matched(password):
                    self._login_user(account)
                    return redirect(request.form.get("next") or url_for(on_signin_view))
                else:
                    self.flash_error("Email or Password is invalid")
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
                    self.flash_error("Invalid reset password token. Please try again")
                    return redirect(url_for("%s:lost_password" % view_name))
                else:
                    self._login_user(user)
                    return redirect(url_for("%s:reset_password" % view_name))

            @route("reset-password/", methods=["GET", "POST"], endpoint="UserAccount:reset_password")
            @login_required
            def reset_password(self):
                self._can_login()
                self.meta_data(title="Reset Password")
                if current_user.require_password_change:
                    if request.method == "POST":
                        try:
                            self.change_password_handler()
                            current_user.clear_reset_password_token()
                            self.flash_success("Password updated successfully!")
                            return redirect(url_for(on_signin_view))
                        except Exception as ex:
                            self.flash_error("Error: %s" % ex.message)
                            return redirect(url_for("%s:reset_password" % view_name))
                    return self.render(view_template=template_page % "reset_password")
                return redirect(url_for(on_signin_view))

            @route("set-email/", methods=["GET", "POST"], endpoint="UserAccount:set_email")
            @login_required
            def set_email(self):
                self._can_login()
                self.meta_data(title="Set Email")

                # Only user without email can set email
                if current_user.email:
                    return redirect(url_for("%s:account_settings" % view_name))

                if request.method == "POST":
                    email = request.form.get("email")
                    if not utils.is_valid_email(email):
                        self.flash_error("Invalid email address '%s'" % email)
                        return redirect(url_for(login_view))

                    if email and self.SESSION_KEY_SET_EMAIL_DATA in session:
                        _data = session[self.SESSION_KEY_SET_EMAIL_DATA]
                        user = User.get_by_email(email)
                        if user:
                            self.flash_error("An account is already using '%s'" % email)
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
                self.meta_data(title="Account Settings")
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
                    self.flash_error("Unable to link your account")

                return redirect(url_for("%s:account_settings" % view_name))

            @route("change-login", methods=["POST"], endpoint="UserAccount:change_login")
            @login_required
            def change_login(self):
                confirm_password = request.form.get("confirm-password").strip()
                try:
                    if current_user.password_matched(confirm_password):
                        self.change_login_handler()
                        self.flash_success("Login Info updated successfully!")
                    else:
                        self.flash_error("Invalid password")
                except Exception as ex:
                    self.flash_error("Error: %s" % ex.message)
                return redirect(url_for("UserAccount:account_settings"))

            @route("change-password", methods=["POST"], endpoint="UserAccount:change_password")
            @login_required
            def change_password(self):
                try:
                    confirm_password = request.form.get("confirm-password").strip()
                    if current_user.password_matched(confirm_password):
                        self.change_password_handler()
                        self.flash_success("Password updated successfully!")
                    else:
                        self.flash_error("Invalid password")
                except Exception as ex:
                    self.flash_error("Error: %s" % ex.message)
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
                    self.flash_success("Account info updated successfully!")
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


# ----
# ADMIN

ADMIN_ROUTE_BASE = "user-admin"

def admin_view(model, **kwargs):

    def wrapper(view):

        Portfolio.__(COMPONENT_USER_ADMIN=True)
        User = model.UserModel.User
        Role = model.UserModel.Role
        RoleRole = model.UserModel.RoleRole

        template_dir = kwargs["template_dir"] if "template_dir" \
                                                 in kwargs else "UserAdmin"
        template_page = template_dir + "/%s.html"

        @view.extends__
        class UserAdmin(object):

            route_base = ADMIN_ROUTE_BASE
            decorators = view.decorators + [login_required]

            @classmethod
            def _validate_admin_roles(cls, user):
                admin = current_user

            @classmethod
            def _user_roles_options(cls):
                return [(r.id, r.name) for r in Role.all().order_by(Role.level.desc())]

            @route("/", endpoint="UserAdmin:index")
            def index(self):
                self.meta_data(title="Users - User Admin")
                per_page = self.get_config("PAGINATION_PER_PAGE", 25)

                page = request.args.get("page", 1)
                include_deleted = True if request.args.get("include-deleted") == "y" else False
                name = request.args.get("name")
                email = request.args.get("email")
                role = request.args.get("role")
                sorting = request.args.get("sorting", "name__asc")

                users = User.all(include_deleted=include_deleted)

                if name:
                    users = users.filter(User.name.contains(name))
                if email:
                    users = users.filter(User.email.contains(email))
                if role:
                    users = users.join(RoleRole)\
                        .join(Role)\
                        .filter(Role.id == role)
                if sorting and "__" in sorting:
                    col, dir = sorting.split("__", 2)
                    users = users.order_by(getattr(User, col) + " %s" % dir)

                users = users.paginate(page=page, per_page=per_page)

                sorting = [("name__asc", "Name ASC"),
                           ("name__desc", "Name DESC"),
                           ("email__asc", "Email ASC"),
                           ("email__DESC", "Email DESC"),
                           ("created_at__asc", "Signup ASC"),
                           ("created_at__desc", "Signup Desc"),
                           ("last_login__asc", "Login ASC"),
                           ("last_login__desc", "Login Desc"),
                           ]
                return self.render(user_roles_options=self._user_roles_options(),
                                   sorting_options=sorting,
                                   users=users,
                                   search_query={
                                       "include-deleted": request.args.get("include-deleted", "n"),
                                       "role": int(request.args.get("role")) if request.args.get("role") else "",
                                       "status": request.args.get("status"),
                                       "name": request.args.get("name", ""),
                                       "email": request.args.get("email", ""),
                                       "sorting": request.args.get("sorting")},
                                   view_template=template_page % "index")

            @route("/<id>", endpoint="UserAdmin:get")
            def get(self, id):
                self.meta_data(title="User Info - Users Admin")
                user = User.get(id, include_deleted=True)
                if not user:
                    abort(404, "User doesn't exist")

                user_roles = [r.id for r in user.roles]
                user_roles_name = [r.name for r in user.roles]

                return self.render(user=user,
                                   user_roles_name=user_roles_name,
                                   user_roles=user_roles,
                                   user_roles_options=self._user_roles_options(),
                                   view_template=template_page % "get")

            @route("/post", methods=["POST"], endpoint="UserAdmin:post")
            def post(self):
                try:
                    id = request.form.get("id")
                    user = User.get(id, include_deleted=True)
                    if not user:
                        self.flash_error("Can't change user info. Invalid user")
                        return redirect(url_for("UserAdmin:index"))

                    email = request.form.get("email", "").strip()
                    name = request.form.get("name")
                    user_roles = request.form.getlist("user_roles")
                    action = request.form.get("action")

                    if action == "activate":
                        user.update(active=True)
                        self.flash_success("User has been ACTIVATED")
                    elif action == "deactivate":
                        user.update(active=False)
                        self.flash_success("User is now DEACTIVATED")
                    elif action == "delete":
                        user.delete()
                        self.flash_success("User has been deleted")
                    elif action == "undelete":
                        user.delete(False)
                        self.flash_success("User is now active")
                    else:
                        if email and email != user.email:
                            if not utils.is_valid_email(email):
                                raise UserWarning("Invalid email address '%s'" % email)
                            else:
                                if User.get_by_email(email):
                                    raise UserWarning("Email exists already '%s'" % email)
                                user.update(email=email)
                        if name != user.name:
                            user.update(name=name)

                        if user_roles:
                            user.update_roles(map(int, user_roles))

                        self.flash_success("User's Info updated successfully!")
                except Exception as ex:
                    self.flash_error("Error: %s " % ex.message)
                return redirect(url_for("UserAdmin:get", id=id))

            @route("reset-password", methods=["POST"], endpoint="UserAdmin:reset_password")
            def reset_password(self):
                """
                Reset the password
                :returns string: The new password string
                """
                try:
                    id = request.form.get("id")
                    user = User.get(id)
                    if not user:
                        raise ViewError("Invalid User")

                    method_ = self.get_config("LOGIN_RESET_PASSWORD_METHOD", "").upper()
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

                    self.flash_success("Password Reset instruction is sent to email")
                except Exception as ex:
                    self.flash_error("Error: %s " % ex.message)
                return redirect(url_for("UserAdmin:get", id=id))

            @route("create", methods=["POST"], endpoint="UserAdmin:create")
            def create(self):
                try:
                    email = request.form.get("email")
                    name = request.form.get("name")
                    user_roles = request.form.getlist("user_roles")
                    if not name:
                        raise ViewError("Name is required")
                    elif not email:
                        raise ViewError("Email is required")
                    elif not utils.is_valid_email(email):
                        raise ViewError("Invalid email address")
                    if User.get_by_email(email):
                        raise ViewError("Email '%s' exists already" % email)
                    else:
                        user = User.new(email=email, name=name, signup_method="EMAIL - FROM ADMIN")
                        if user:
                            self.flash_success("User created successfully!")

                            if user_roles:
                                user.update_roles(map(int, user_roles))

                            return redirect(url_for("UserAdmin:get", id=user.id))
                        else:
                            raise ViewError("Couldn't create new user")
                except Exception as ex:
                    self.flash_error("Error: %s" % ex.message)
                return redirect(url_for("UserAdmin:index"))

            @route("roles", methods=["GET", "POST"], endpoint="UserAdmin:roles")
            def roles(self):
                """
                Only admin and super admin can add/remove roles
                RESTRICTED ROLES CAN'T BE CHANGED
                """
                roles_rage_max = 11
                if request.method == "POST":
                    try:
                        id = request.form.get("id")
                        name = request.form.get("name")
                        level = request.form.get("level")
                        action = request.form.get("action")

                        if name and level:
                            level = int(level)
                            name = name.upper()
                            _levels = [r[0] for r in Role.PRIMARY]
                            _names = [r[1] for r in Role.PRIMARY]
                            if level in _levels or name in _names:
                                raise ViewError("Can't modify PRIMARY Roles - name: %s, level: %s " % (name, level))
                            else:
                                if id:
                                    role = Role.get(id)
                                    if role:
                                        if action == "delete":
                                            role.delete()
                                            self.flash_success("Role '%s' deleted successfully!" % role.name)
                                        elif action == "update":
                                            if role.level != level and Role.get_by_level(level):
                                                raise ViewError("Role Level '%s' exists already" % level)
                                            elif role.name != name and Role.get_by_name(name):
                                                raise ViewError("Role Name '%s'  exists already" % name)
                                            else:
                                                role.update(name=name, level=level)
                                                self.flash_success("Role '%s (%s)' updated successfully" % (name, level))
                                    else:
                                        raise ViewError("Role doesn't exist")
                                else:
                                    if Role.get_by_level(level):
                                        raise ViewError("Role Level '%s' exists already" % level)
                                    elif Role.get_by_name(name):
                                        raise ViewError("Role Name '%s'  exists already" % name)
                                    else:
                                        Role.new(name=name, level=level)
                                        self.flash_success("New Role '%s (%s)' addedd successfully" % (name, level))
                    except Exception as ex:
                        self.flash_error("Error: %s" % ex.message)
                    return redirect(url_for("UserAdmin:roles"))
                else:
                    self.meta_data(title="User Roles - Users Admin")
                    roles = Role.all().order_by(Role.level.desc())

                    allocated_levels = [r.level for r in roles]
                    levels_options = [(l, l) for l in range(1, roles_rage_max) if l not in allocated_levels]

                    return self.render(roles=roles,
                                       levels_options=levels_options,
                                       view_template=template_page % "roles")
        return view
    return wrapper
