
import datetime
from pylot import utils

class ModelError(Exception):
    pass


# The user_model create a fully built model with social signin
def user_model(db):

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

def post_model(UserModel):
    """
    Post Model
    :param UserModel:
    """

    db = UserModel.User.db

    class SlugNameMixin(object):
        name = db.Column(db.String(250), index=True)
        slug = db.Column(db.String(250), index=True, unique=True)

        @classmethod
        def get_by_slug(cls, slug=None, name=None):
            """
            Return a post by slug
            """
            if name and not slug:
                slug = utils.slug(name)
            return cls.all().filter(cls.slug == slug).first()

        @classmethod
        def new(cls, name, slug=None):
            slug = utils.slug(name if not slug else slug)
            return cls.create(name=name, slug=slug)

        def rename(self, name, slug=None):
            slug = utils.slug(name if not slug else slug)
            return self.update(name=name, slug=slug)

    class PostType(SlugNameMixin, db.Model):
        """
        Types
        """
        @property
        def total_posts(self):
            return Post.all().filter(Post.type_id == self.id).count()

    class PostCategory(SlugNameMixin, db.Model):
        """
        Category
        """
        @property
        def total_posts(self):
            return PostPostCategory.all()\
                .filter(PostPostCategory.category_id == self.id)\
                .count()

    class PostTag(SlugNameMixin, db.Model):
        """
        Tag
        """
        @property
        def total_posts(self):
            return PostPostTag.all()\
                .filter(PostPostTag.tag_id == self.id)\
                .count()

    class PostPostTag(db.Model):
        """
        PostPostTag
        """
        post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
        tag_id = db.Column(db.Integer, db.ForeignKey(PostTag.id))

        @classmethod
        def add(cls, post_id, tag_id):
            c = cls.all().filter(cls.post_id == post_id)\
                .filter(cls.tag_id == tag_id)\
                .first()
            if not c:
                cls.create(post_id=post_id, tag_id=tag_id)

        @classmethod
        def remove(cls, post_id, tag_id):
            c = cls.all().filter(cls.post_id == post_id)\
                .filter(cls.tag_id == tag_id)\
                .first()
            if c:
                c.delete(hard_delete=True)

    class PostPostCategory(db.Model):
        post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
        category_id = db.Column(db.Integer, db.ForeignKey(PostCategory.id))

        @classmethod
        def add(cls, post_id, category_id):
            c = cls.all().filter(cls.post_id == post_id)\
                .filter(cls.category_id == category_id)\
                .first()
            if not c:
                cls.create(post_id=post_id, category_id=category_id)

        @classmethod
        def remove(cls, post_id, category_id):
            c = cls.all().filter(cls.post_id == post_id)\
                .filter(cls.category_id == category_id)\
                .first()
            if c:
                c.delete(hard_delete=True)

    class Post(db.Model):

        user_id = db.Column(db.Integer, db.ForeignKey(UserModel.User.id))
        type_id = db.Column(db.Integer, db.ForeignKey(PostType.id))
        parent_id = db.Column(db.Integer)
        revision_id = db.Column(db.Integer)
        title = db.Column(db.String(250))
        slug = db.Column(db.String(250), index=True)
        content = db.Column(db.Text)
        excerpt = db.Column(db.Text)
        is_public = db.Column(db.Boolean, index=True, default=False)
        is_sticky = db.Column(db.Boolean, index=True, default=False)
        is_published = db.Column(db.Boolean, index=True, default=True)
        is_draft = db.Column(db.Boolean, index=True, default=False)
        is_revision = db.Column(db.Boolean, default=False)
        published_date = db.Column(db.DateTime)
        author = db.relationship(UserModel.User, backref="posts")
        type = db.relationship(PostType, backref="posts")
        categories = db.relationship(PostCategory,
                                     secondary=PostPostCategory.__table__.name)
        tags = db.relationship(PostTag,
                                     secondary=PostPostTag.__table__.name)

        @classmethod
        def new(cls, title, **kwargs):
            """
            Insert a new post
            """
            published_date = None
            is_revision = False
            is_published = False
            is_draft = False
            is_public = kwargs["is_public"] if "is_public" in kwargs else True
            parent_id = int(kwargs["parent_id"]) if "parent_id" in kwargs else None
            if "is_revision" in kwargs and kwargs["is_revision"] is True:
                if not parent_id:
                    raise ModelError("'parent_id' is missing for revision")
                is_revision =True
                is_public = False
            elif "is_draft" in kwargs and kwargs["is_draft"] is True:
                is_draft = True
                is_public = False
            elif "is_published" in kwargs and kwargs["is_published"] is True:
                is_published = True
                published_date = datetime.datetime.now()

            slug = ""
            if is_published or is_draft:
                slug = cls.create_slug(title if "slug" not in kwargs else kwargs["slug"])

            data = {
                "title": title,
                "slug": slug,
                "content": kwargs["content"] if "content" in kwargs else "",
                "excerpt": kwargs["excerpt"] if "excerpt" in kwargs else "",
                "is_published": is_published,
                "published_date": published_date,
                "is_draft": is_draft,
                "is_revision": is_revision,
                "is_public": is_public,
                "parent_id": parent_id,
                "type_id": kwargs["type_id"] if "type_id" in kwargs else None
            }
            return cls.create(**data)

        @classmethod
        def get_published(cls, id=None, slug=None):
            """
            Get a published post by id or slug
            :param id: The id of the post
            :param slug: str - The slug to look for
            """
            post = None
            if id:
                post = cls.get(id)
            elif slug:
                post = cls.get_by_slug(slug)
            return post if post and post.is_published else None

        @classmethod
        def get_published_by_category_slug(cls, slug):
            """
            Query by category slug
            :return SQLA :
            """
            return cls.all()\
                .join(PostPostCategory)\
                .join(PostCategory)\
                .filter(PostCategory.slug.in_(slug))\
                .filter(cls.is_published == True)

        @classmethod
        def get_published_by_type_slug(cls, slug):
            """
            Query by type slug
            :return SQLA :
            """
            return cls.all()\
                .join(PostType)\
                .filter(PostType.slug.in_(slug))\
                .filter(cls.is_published == True)

        @classmethod
        def get_published_by_tag_slug(cls, slug):
            """
            Query by type slug
            :return SQLA :
            """
            return cls.all()\
                .join(PostTag)\
                .filter(PostTag.slug.in_(slug))\
                .filter(cls.is_published == True)

        @classmethod
        def create_slug(cls, title):
            slug_counter = 0
            _slug = utils.slug(title).lower()
            while True:
                slug = _slug
                if slug_counter > 0:
                    slug += str(slug_counter)
                    slug_counter += 1
                if not cls.get_by_slug(slug):
                    break
            return slug

        @classmethod
        def get_by_slug(cls, slug):
            """
            Return a post by slug
            """
            return cls.all().filter(cls.slug == slug).first()

        def publish(self, published_date=None):
            if self.is_draft:
                data = {
                    "is_draft": False,
                    "is_published": True,
                    "published_date": published_date or datetime.datetime.now()
                }
                self.update(**data)

        def set_type(self, type_id):
            self.update(type_id=type_id)

        def set_slug(self, title):
            slug = utils.slug(title)
            if title and slug != self.slug:
                slug = self.create_slug(slug)
                self.update(slug=slug)

        def update_categories(self, categories_list):
            """
            Update categories by replacing existing list with new list
            :param categories_list: list. The new list of category
            """
            cats = PostPostCategory.all()\
                    .filter(PostPostCategory.post_id == self.id)
            cats_list = [c.category_id for c in cats]

            del_cats = list(set(cats_list) - set(categories_list))
            new_cats = list(set(categories_list) - set(cats_list))

            for dc in del_cats:
                PostPostCategory.remove(post_id=self.id, category_id=dc)

            for nc in new_cats:
                PostPostCategory.add(post_id=self.id, category_id=nc)

        def update_tags(self, tags_list):
            """
            Update tags by replacing existing list with new list
            :param tags_list: list. The new list of tags
            """
            tags = PostPostTag.all()\
                    .filter(PostPostTag.post_id == self.id)
            tags_list_ = [c.tag_id for c in tags]

            del_tags = list(set(tags_list_) - set(tags_list))
            new_tags = list(set(tags_list) - set(tags_list_))

            for dc in del_tags:
                PostPostTag.remove(post_id=self.id, tag_id=dc)

            for nc in new_tags:
                PostPostTag.add(post_id=self.id, tag_id=nc)

        @property
        def status(self):
            if self.is_published:
                return "Published"
            elif self.is_draft:
                return "Draft"
            elif self.is_revision:
                return "Revision"

        def delete_revisions(self):
            """
            Delete all revisions
            """
            try:
                Post.all()\
                    .filter(Post.post_id == self.id)\
                    .filter(Post.is_revision == True)\
                    .delete()
                Post.db.commit()
            except Exception as ex:
                Post.db.rollback()

        @property
        def total_revisions(self):
            return Post.all()\
                .filter(Post.post_id == self.id)\
                .filter(Post.is_revision == True)\
                .count()

    class PostUploadObject(db.Model):
        parent_id = db.Column(db.Integer, index=True)
        user_id = db.Column(db.Integer, index=True)
        provider = db.Column(db.String(250))
        container = db.Column(db.String(250))
        local_path = db.Column(db.Text)
        name = db.Column(db.Text)
        description = db.Column(db.String(250))
        size = db.Column(db.Integer)
        extension = db.Column(db.String(10), index=True)
        type = db.Column(db.String(25), index=True)
        object_path = db.Column(db.Text)
        object_url = db.Column(db.Text)
        is_private = db.Column(db.Boolean, index=True, default=False)

    return utils.to_struct(Post=Post,
                           Category=PostCategory,
                           Type=PostType,
                           PostCategory=PostPostCategory,
                           Tag=PostTag,
                           PostTag=PostPostTag,
                           UploadObject=PostUploadObject
                           )
