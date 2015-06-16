import os

from portfolio import (Portfolio, utils, route, abort, redirect, request, url_for,
                   jsonify, session, AppError)

from portfolio.component import (mailer, storage, recaptcha)
from flask_login import (LoginManager, login_required, login_user, logout_user,
                         current_user)

def user_admin(model, **kwargs):

    def wrapper(view):

        Portfolio.set_context__(COMPONENT_USER_ADMIN=True)
        User = model.UserModel.User
        Role = model.UserModel.Role
        RoleRole = model.UserModel.RoleRole

        template_dir = kwargs["template_dir"] if "template_dir" \
                                                 in kwargs else "Portfolio/UserAdmin"
        template_page = template_dir + "/%s.html"

        @view.extends__
        class UserAdmin(object):
            route_base = "user-admin"
            per_page = 25

            @classmethod
            def _validate_admin_roles(cls, user):
                admin = current_user

            @classmethod
            def _user_roles_options(cls):
                return [(r.id, r.name) for r in Role.all().order_by(Role.level.desc())]

            @route("/", endpoint="UserAdmin:index")
            def index(self):
                self.set_meta__(title="Users - User Admin")
                per_page = self.get_config__("PAGINATION_PER_PAGE", 25)

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
                self.set_meta__(title="User Info - Users Admin")
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
                        self.flash_error__("Can't change user info. Invalid user")
                        return redirect(url_for("UserAdmin:index"))

                    email = request.form.get("email", "").strip()
                    name = request.form.get("name")
                    user_roles = request.form.getlist("user_roles")
                    action = request.form.get("action")

                    if action == "activate":
                        user.update(active=True)
                        self.flash_success__("User has been ACTIVATED")
                    elif action == "deactivate":
                        user.update(active=False)
                        self.flash_success__("User is now DEACTIVATED")
                    elif action == "delete":
                        user.delete()
                        self.flash_success__("User has been deleted")
                    elif action == "undelete":
                        user.delete(False)
                        self.flash_success__("User is now active")
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

                        self.flash_success__("User's Info updated successfully!")
                except Exception as ex:
                    self.flash_error__("Error: %s " % ex.message)
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
                        raise AppError("Invalid User")

                    method_ = self.get_config__("LOGIN_RESET_PASSWORD_METHOD", "").upper()
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

                    self.flash_success__("Password Reset instruction is sent to email")
                except Exception as ex:
                    self.flash_error__("Error: %s " % ex.message)
                return redirect(url_for("UserAdmin:get", id=id))

            @route("create", methods=["POST"], endpoint="UserAdmin:create")
            def create(self):
                try:
                    email = request.form.get("email")
                    name = request.form.get("name")
                    user_roles = request.form.getlist("user_roles")
                    if not name:
                        raise AppError("Name is required")
                    elif not email:
                        raise AppError("Email is required")
                    elif not utils.is_valid_email(email):
                        raise AppError("Invalid email address")
                    if User.get_by_email(email):
                        raise AppError("Email '%s' exists already" % email)
                    else:
                        user = User.new(email=email, name=name, signup_method="EMAIL - FROM ADMIN")
                        if user:
                            self.flash_success__("User created successfully!")

                            if user_roles:
                                user.update_roles(map(int, user_roles))

                            return redirect(url_for("UserAdmin:get", id=user.id))
                        else:
                            raise AppError("Couldn't create new user")
                except Exception as ex:
                    self.flash_error__("Error: %s" % ex.message)
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
                                raise AppError("Can't modify PRIMARY Roles - name: %s, level: %s " % (name, level))
                            else:
                                if id:
                                    role = Role.get(id)
                                    if role:
                                        if action == "delete":
                                            role.delete()
                                            self.flash_success__("Role '%s' deleted successfully!" % role.name)
                                        elif action == "update":
                                            if role.level != level and Role.get_by_level(level):
                                                raise AppError("Role Level '%s' exists already" % level)
                                            elif role.name != name and Role.get_by_name(name):
                                                raise AppError("Role Name '%s'  exists already" % name)
                                            else:
                                                role.update(name=name, level=level)
                                                self.flash_success__("Role '%s (%s)' updated successfully" % (name, level))
                                    else:
                                        raise AppError("Role doesn't exist")
                                else:
                                    if Role.get_by_level(level):
                                        raise AppError("Role Level '%s' exists already" % level)
                                    elif Role.get_by_name(name):
                                        raise AppError("Role Name '%s'  exists already" % name)
                                    else:
                                        Role.new(name=name, level=level)
                                        self.flash_success__("New Role '%s (%s)' addedd successfully" % (name, level))
                    except Exception as ex:
                        self.flash_error__("Error: %s" % ex.message)
                    return redirect(url_for("UserAdmin:roles"))
                else:
                    self.set_meta__(title="User Roles - Users Admin")
                    roles = Role.all().order_by(Role.level.desc())

                    allocated_levels = [r.level for r in roles]
                    levels_options = [(l, l) for l in range(1, roles_rage_max) if l not in allocated_levels]

                    return self.render(roles=roles,
                                       levels_options=levels_options,
                                       view_template=template_page % "roles")
        return view
    return wrapper