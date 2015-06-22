
import os
import datetime

from flask import url_for, request, redirect, abort, session, jsonify
from portfolio import Portfolio, route
from portfolio.ext import storage
from flask_login import login_required, current_user

import datetime
from portfolio import utils
from portfolio.component import ModelError

def model(UserModel):
    """
    Post Model
    :param UserModel:
    """

    db = UserModel.User.db

    class SlugNameMixin(object):
        name = db.Column(db.String(250), index=True)
        slug = db.Column(db.String(250), index=True, unique=True)
        description = db.Column(db.String(250))
        image_url = db.Column(db.Text)

        @classmethod
        def get_by_slug(cls, slug=None, name=None):
            """
            Return a post by slug
            """
            if name and not slug:
                slug = utils.slugify(name)
            return cls.all().filter(cls.slug == slug).first()

        @classmethod
        def new(cls, name, slug=None):
            slug = utils.slugify(name if not slug else slug)
            return cls.create(name=name, slug=slug)

        def rename(self, name, slug=None):
            slug = utils.slugify(name if not slug else slug)
            return self.update(name=name, slug=slug)

    class CmsPostType(SlugNameMixin, db.Model):
        """
        Types
        """
        @property
        def total_posts(self):
            return CmsPost.all().filter(CmsPost.type_id == self.id).count()

    class CmsPostCategory(SlugNameMixin, db.Model):
        """
        Category
        """
        @property
        def total_posts(self):
            return CmsPostPostCategory.all()\
                .filter(CmsPostPostCategory.category_id == self.id)\
                .count()

    class CmsPostTag(SlugNameMixin, db.Model):
        """
        Tag
        """
        @property
        def total_posts(self):
            return CmsPostPostTag.all()\
                .filter(CmsPostPostTag.tag_id == self.id)\
                .count()

    class CmsPostPostTag(db.Model):
        """
        PostPostTag
        """
        post_id = db.Column(db.Integer, db.ForeignKey("cms_post.id"))
        tag_id = db.Column(db.Integer, db.ForeignKey(CmsPostTag.id))

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

    class CmsPostPostCategory(db.Model):
        post_id = db.Column(db.Integer, db.ForeignKey("cms_post.id"))
        category_id = db.Column(db.Integer, db.ForeignKey(CmsPostCategory.id))

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

    class CmsPost(db.Model):

        user_id = db.Column(db.Integer, db.ForeignKey(UserModel.User.id))
        type_id = db.Column(db.Integer, db.ForeignKey(CmsPostType.id))
        parent_id = db.Column(db.Integer)  # If the post is derived from another post
        revision_id = db.Column(db.Integer)  # When updating the post, will auto-save
        title = db.Column(db.String(250))
        name = db.Column(db.String(250), index=True)
        slug = db.Column(db.String(250), index=True)
        content = db.Column(db.Text)
        excerpt = db.Column(db.Text)
        image_url = db.Column(db.Text)  # The main post url
        meta_title = db.Column(db.Text)
        meta_description = db.Column(db.Text)
        language = db.Column(db.String(250))
        is_public = db.Column(db.Boolean, index=True, default=False)
        is_sticky = db.Column(db.Boolean, index=True, default=False)  # A sticky post usually stay on top, no matter the count
        is_featured = db.Column(db.Boolean, index=True, default=False)  # Feature post are limited
        is_published = db.Column(db.Boolean, index=True, default=True)
        is_draft = db.Column(db.Boolean, index=True, default=False)
        is_revision = db.Column(db.Boolean, default=False)
        published_at = db.Column(db.DateTime)
        published_by = db.Column(db.Integer, db.ForeignKey(UserModel.User.id))
        author = db.relationship(UserModel.User, backref="posts")
        type = db.relationship(CmsPostType, backref="posts")
        categories = db.relationship(CmsPostCategory,
                                     secondary=CmsPostPostCategory.__table__.name)
        tags = db.relationship(CmsPostTag,
                                     secondary=CmsPostPostTag.__table__.name)

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
                .join(CmsPostPostCategory)\
                .join(CmsPostCategory)\
                .filter(CmsPostCategory.slug.in_(slug))\
                .filter(cls.is_published == True)

        @classmethod
        def get_published_by_type_slug(cls, slug):
            """
            Query by type slug
            :return SQLA :
            """
            return cls.all()\
                .join(CmsPostType)\
                .filter(CmsPostType.slug.in_(slug))\
                .filter(cls.is_published == True)

        @classmethod
        def get_published_by_tag_slug(cls, slug):
            """
            Query by type slug
            :return SQLA :
            """
            return cls.all()\
                .join(CmsPostTag)\
                .filter(CmsPostTag.slug.in_(slug))\
                .filter(cls.is_published == True)

        @classmethod
        def create_slug(cls, title):
            slug_counter = 0
            _slug = utils.slugify(title).lower()
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
            slug = utils.slugify(title)
            if title and slug != self.slug:
                slug = self.create_slug(slug)
                self.update(slug=slug)

        def update_categories(self, categories_list):
            """
            Update categories by replacing existing list with new list
            :param categories_list: list. The new list of category
            """
            cats = CmsPostPostCategory.all()\
                    .filter(CmsPostPostCategory.post_id == self.id)
            cats_list = [c.category_id for c in cats]

            del_cats = list(set(cats_list) - set(categories_list))
            new_cats = list(set(categories_list) - set(cats_list))

            for dc in del_cats:
                CmsPostPostCategory.remove(post_id=self.id, category_id=dc)

            for nc in new_cats:
                CmsPostPostCategory.add(post_id=self.id, category_id=nc)

        def update_tags(self, tags_list):
            """
            Update tags by replacing existing list with new list
            :param tags_list: list. The new list of tags
            """
            tags = CmsPostPostTag.all()\
                    .filter(CmsPostPostTag.post_id == self.id)
            tags_list_ = [c.tag_id for c in tags]

            del_tags = list(set(tags_list_) - set(tags_list))
            new_tags = list(set(tags_list) - set(tags_list_))

            for dc in del_tags:
                CmsPostPostTag.remove(post_id=self.id, tag_id=dc)

            for nc in new_tags:
                CmsPostPostTag.add(post_id=self.id, tag_id=nc)

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
                CmsPost.all()\
                    .filter(CmsPost.post_id == self.id)\
                    .filter(CmsPost.is_revision == True)\
                    .delete()
                CmsPost.db.commit()
            except Exception as ex:
                CmsPost.db.rollback()

        @property
        def total_revisions(self):
            return CmsPost.all()\
                .filter(CmsPost.post_id == self.id)\
                .filter(CmsPost.is_revision == True)\
                .count()

    class CmsUploadObject(db.Model):
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

    class CmsOption(db.Model):
        name = db.Column(db.String(250))
        value = db.Column(db.Text)

    return utils.to_struct(Post=CmsPost,
                           Category=CmsPostCategory,
                           Type=CmsPostType,
                           PostCategory=CmsPostPostCategory,
                           Tag=CmsPostTag,
                           PostTag=CmsPostPostTag,
                           UploadObject=CmsUploadObject,
                           Option=CmsOption)


def view(model, **kwargs):
    """
    Access a post by slug or id
    By default it will be accessed at /post/<slug>

    :params model: The module containing the PostModel
    :params kwargs:
        route_read - A custom route for read
        route_list - A custome route for list
        template_dir - A directory containing post_list.html and post_read.html
        types = [] - All the types slugs allowed. ie ['blog', 'article']
    """

    route_read = kwargs["route_read"] if "route_read" in kwargs else "post"
    route_read = "%s/<slug>" % route_read

    route_list = kwargs["route_list"] if "route_list" in kwargs else "posts"
    template_dir = kwargs["template_dir"] if "template_dir" in kwargs else "CmsPost"
    types = kwargs["types"] if "types" in kwargs else []

    Post = model.CmsPostModel.Post
    Type = model.CmsPostModel.Type

    def wrapper(view):
        view_name = view.__name__

        @view.extends__
        class CmsPost(object):

            def _prepare_post(self, post):
                """
                Prepare the post data
                """
                url = url_for("%s:post_read" % view_name, slug=post.slug,
                              _external=True)
                post.url = url
                return post

            def _get_prev_next_post(self, post, position):
                """
                Return previous or next post based on the current post
                """
                _post = Post.all()\
                    .join(Type)\
                    .filter(Post.is_published == True)\
                    .filter(Type.slug.in_(types))
                if position == "prev":
                    _post = _post.filter(Post.id < post.id)
                elif position == "next":
                    _post = _post.filter(Post.id > post.id)
                else:
                    raise ValueError("Invalid position. Must be 'PREV' or 'NEXT'")

                return _post.first()

            @route(route_list)
            def post_list(self):
                _posts = Post.get_published_by_type_slug(types)

                posts = []
                for _p in _posts:
                    posts.append(self._prepare_post(_p))

                return self.render(posts=posts,
                                   view_template="%s/post_list.html" % template_dir)

            @route(route_read)
            def post_read(self, slug):
                if slug.isdigit():
                    post = Post.get(slug)
                else:
                    post = Post.get_by_slug(slug)

                if not post or not post.is_published:
                    abort(404, "Post doesn't exist")
                else:
                    if post.type.slug.lower() not in [t.lower() for t in types]:
                        abort(400, "Invalid post")

                return self.render(post=self._prepare_post(post),
                                   prev_post=self._get_prev_next_post(post, "prev"),
                                   next_post=self._get_prev_next_post(post, "next"),
                                   view_template="%s/post_read.html" % template_dir)
        return view
    return wrapper


# ---

# ADMIN

ADMIN_ROUTE_BASE = "cms-post-admin"

def admin_view(model, **kwargs):

    def wrapper(view):
        template_dir = kwargs["template_dir"] if "template_dir" \
                                                 in kwargs else "CmsPostAdmin"
        template_page = template_dir + "/%s.html"
        PostModel = model.CmsPostModel

        Portfolio.__(COMPONENT_POST_ADMIN=True)

        @view.extends__
        class PostAdmin(object):

            route_base = ADMIN_ROUTE_BASE
            decorators = view.decorators + [login_required]

            __session_edit_key = "admin_post_edit_post"

            @route("/", endpoint="PostAdmin:index")
            def index(self):
                """
                List all posts
                """
                self.meta_data(title="All Posts")
                per_page = self.get_config("PAGINATION_PER_PAGE", 25)
                page = request.args.get("page", 1)
                id = request.args.get("id", None)
                slug = request.args.get("slug", None)
                status = request.args.get("status", "all")
                user_id = request.args.get("user_id", None)
                type_id = request.args.get("type_id", None)
                category_id = request.args.get("category_id", None)
                tag_id = request.args.get("tag_id", None)

                posts = PostModel.Post.all()

                if id:
                    posts = posts.filter(PostModel.Post.id == id)
                if slug:
                    posts = posts.filter(PostModel.Post.slug == slug)
                if user_id:
                    posts = posts.filter(PostModel.Post.user_id == user_id)
                if type_id:
                    posts = posts.filter(PostModel.Post.type_id == type_id)
                if category_id:
                    posts = posts.join(PostModel.PostCategory)\
                        .join(PostModel.Category)\
                        .filter(PostModel.Category.id == category_id)
                if tag_id:
                    posts = posts.join(PostModel.PostTag)\
                        .join(PostModel.Tag)\
                        .filter(PostModel.Tag.id == tag_id)
                if status == "publish":
                    posts = posts.filter(PostModel.Post.is_published == True)
                elif status == "draft":
                    posts = posts.filter(PostModel.Post.is_draft == True)
                elif status == "revision":
                    posts = posts.filter(PostModel.Post.is_revision == True)

                posts = posts.order_by(PostModel.Post.id.desc())
                posts = posts.paginate(page=page, per_page=per_page)

                return self.render(posts=posts,
                                   query_vars={
                                       "id": id,
                                       "slug": slug,
                                       "user_id": user_id,
                                       "type_id": type_id,
                                       "status": status
                                   },
                                   view_template=template_page % "index")

            @route("read/<id>", endpoint="PostAdmin:read")
            def read(self, id):
                """
                Read Post
                """
                post = PostModel.Post.get(id)
                if not post:
                    abort(404, "Post doesn't exist")

                self.meta_data(title="Read: %s " % post.title)

                return self.render(post=post,
                                   view_template=template_page % "read")

            @route("new", defaults={"id": None}, endpoint="PostAdmin:new")
            @route("edit/<id>", endpoint="PostAdmin:edit")
            def edit(self, id):
                """
                Create / Edit Post
                """
                self.meta_data(title="Edit Post")

                types = [(t.id, t.name) for t in PostModel.Type.all().order_by(PostModel.Type.name.asc())]
                categories = [(c.id, c.name) for c in PostModel.Category.all().order_by(PostModel.Category.name.asc())]
                checked_cats = []
                post = {
                    "id": 0,
                    "title": "",
                    "content": "",
                    "slug": "",
                    "type_id": 0
                }

                # saved in session
                if request.args.get("error") and self.__session_edit_key in session:
                    post = session[self.__session_edit_key]
                    checked_cats = post["post_categories"]
                    del session[self.__session_edit_key]

                elif id:
                    post = PostModel.Post.get(id)
                    if not post or post.is_revision:
                        abort(404, "Post doesn't exist")
                    checked_cats = [c.id for c in post.categories]

                images = PostModel.UploadObject.all()\
                    .filter(PostModel.UploadObject.type == "IMAGE")\
                    .order_by(PostModel.UploadObject.name.asc())

                images_list = [{"id": img.id, "url": img.object_url} for img in images]
                return self.render(post=post,
                                   types=types,
                                   categories=categories,
                                   checked_categories=checked_cats,
                                   view_template=template_page % "edit",
                                   images_list=images_list
                                  )

            @route("post", methods=["POST"], endpoint="PostAdmin:post")
            def post(self):
                id = request.form.get("id", None)
                title = request.form.get("title", None)
                slug = request.form.get("slug", None)
                content = request.form.get("content", None)
                type_id = request.form.get("type_id", None)
                post_categories = request.form.getlist("post_categories")
                published_date = request.form.get("published_date", None)
                status = request.form.get("status", "draft")
                is_published = True if status == "publish" else False
                is_draft = True if status == "draft" else False
                is_public = request.form.get("is_public", True)
                tags = list(set(request.form.get("tags", "").split(",")))

                if status in ["draft", "publish"] and (not title or not type_id):
                    if not title:
                        self.flash_error("Post Title is missing ")
                    if not type_id:
                        self.flash_error("Post type is missing")

                    session[self.__session_edit_key] = {
                        "id": id,
                        "title": title,
                        "content": content,
                        "slug": slug,
                        "type_id": type_id,
                        "published_date": published_date,
                        "post_categories": post_categories
                    }
                    if id:
                        url = url_for("PostAdmin:edit", id=id, error=1)
                    else:
                        url = url_for("PostAdmin:new", error=1)
                    return redirect(url)

                data = {
                    "title": title,
                    "content": content,
                    "type_id": type_id
                }

                if published_date:
                    published_date = datetime.datetime.strptime(published_date, "%Y-%m-%d %H:%M:%S")
                else:
                    published_date = datetime.datetime.now()

                if id and status in ["delete", "revision"]:
                    post = PostModel.Post.get(id)
                    if not post:
                        abort(404, "Post '%s' doesn't exist" % id)

                    if status == "delete":
                        post.delete()
                        self.flash_success("Post deleted successfully!")
                        return redirect(url_for("PostAdmin:index"))

                    elif status == "revision":
                        data.update({
                            "user_id": current_user.id,
                            "parent_id": id,
                            "is_revision": True,
                            "is_draft": False,
                            "is_published": False,
                            "is_public": False
                        })
                        post = PostModel.Post.create(**data)
                        return jsonify({"revision_id": post.id})

                elif status in ["draft", "publish"]:
                    data.update({
                        "is_published": is_published,
                        "is_draft": is_draft,
                        "is_revision": False,
                        "is_public": is_public
                    })
                    if id:
                        post = PostModel.Post.get(id)
                        if not post:
                            abort(404, "Post '%s' doesn't exist" % id)
                        elif post.is_revision:
                            abort(403, "Can't access this post")
                        else:
                            post.update(**data)
                    else:
                        data["user_id"] = current_user.id
                        if is_published:
                            data["published_date"] = published_date
                        post = PostModel.Post.create(**data)

                    # prepare tags
                    _tags = []
                    for tag in tags:
                        tag = tag.strip().lower()
                        _tag = PostModel.Tag.get_by_slug(name=tag)
                        if tag and not _tag:
                            _tag = PostModel.Tag.new(name=tag)
                        if _tag:
                            _tags.append(_tag.id)
                    post.update_tags(_tags)

                    post.set_slug(slug or title)

                    post.update_categories(map(int, post_categories))

                    if post.is_published and not post.published_date:
                        post.update(published_date=published_date)

                    self.flash_success("Post saved successfully!")

                    endpoint = "read" if post.is_published else "edit"
                    return redirect(url_for("PostAdmin:%s" % endpoint, id=post.id))

                else:
                    abort(400, "Invalid post status")

            @route("categories", methods=["GET", "POST"], endpoint="PostAdmin:categories")
            def categories(self):
                self.meta_data(title="Post Categories")
                if request.method == "POST":
                    id = request.form.get("id", None)
                    action = request.form.get("action")
                    name = request.form.get("name")
                    slug = request.form.get("slug", None)
                    ajax = request.form.get("ajax", False)
                    try:
                        if not id:
                            cat = PostModel.Category.new(name=name, slug=slug)
                            if ajax:
                                return jsonify({
                                    "id": cat.id,
                                    "name": cat.name,
                                    "slug": cat.slug,
                                    "status": "OK"
                                })
                            self.flash_success("New category '%s' added" % name)
                        else:
                            post_cat = PostModel.Category.get(id)
                            if post_cat:
                                if action == "delete":
                                    post_cat.delete()
                                    self.flash_success("Category '%s' deleted successfully!" % post_cat.name)
                                else:
                                    post_cat.update(name=name, slug=slug)
                                    self.flash_success("Category '%s' updated successfully!" % post_cat.name)
                    except Exception as ex:
                        if ajax:
                            return jsonify({
                                "error": True,
                                "error_message": ex.message
                            })

                        self.flash_error("Error: %s" % ex.message)
                    return redirect(url_for("PostAdmin:categories"))

                else:
                    cats = PostModel.Category.all().order_by(PostModel.Category.name.asc())
                    return self.render(categories=cats,
                                       view_template=template_page % "categories")

            @route("types", methods=["GET", "POST"], endpoint="PostAdmin:types")
            def types(self):
                self.meta_data(title="Post Types")
                if request.method == "POST":
                    try:
                        id = request.form.get("id", None)
                        action = request.form.get("action")
                        name = request.form.get("name")
                        slug = request.form.get("slug", None)
                        if not id:
                            PostModel.Type.new(name=name, slug=slug)
                            self.flash_success("New type '%s' added" % name)
                        else:
                            post_type = PostModel.Type.get(id)
                            if post_type:
                                if action == "delete":
                                    post_type.delete()
                                    self.flash_success("Type '%s' deleted successfully!" % post_type.name)
                                else:
                                    post_type.update(name=name, slug=slug)
                                    self.flash_success("Type '%s' updated successfully!" % post_type.name)
                    except Exception as ex:
                        self.flash_error("Error: %s" % ex.message)
                    return redirect(url_for("PostAdmin:types"))
                else:
                    types = PostModel.Type.all().order_by(PostModel.Type.name.asc())
                    return self.render(types=types,
                                       view_template=template_page % "types")

            @route("tags", methods=["GET", "POST"], endpoint="PostAdmin:tags")
            def tags(self):
                self.meta_data(title="Post Tags")
                if request.method == "POST":
                    id = request.form.get("id", None)
                    action = request.form.get("action")
                    name = request.form.get("name")
                    slug = request.form.get("slug", None)
                    ajax = request.form.get("ajax", False)
                    try:
                        if not id:
                            tag = PostModel.Tag.new(name=name, slug=slug)
                            if ajax:
                                return jsonify({
                                    "id": tag.id,
                                    "name": tag.name,
                                    "slug": tag.slug,
                                    "status": "OK"
                                })
                            self.flash_success("New Tag '%s' added" % name)
                        else:
                            post_tag = PostModel.Tag.get(id)
                            if post_tag:
                                if action == "delete":
                                    post_tag.delete()
                                    self.flash_success("Tag '%s' deleted successfully!" % post_tag.name)
                                else:
                                    post_tag.update(name=name, slug=slug)
                                    self.flash_success("Tag '%s' updated successfully!" % post_tag.name)
                    except Exception as ex:
                        if ajax:
                            return jsonify({
                                "error": True,
                                "error_message": ex.message
                            })

                        self.flash_error("Error: %s" % ex.message)
                    return redirect(url_for("PostAdmin:tags"))

                else:
                    tags = PostModel.Tag.all().order_by(PostModel.Tag.name.asc())
                    return self.render(tags=tags,
                                       view_template=template_page % "tags")

            @route("images", methods=["GET", "POST"], endpoint="PostAdmin:images")
            def images(self):
                self.meta_data(title="Images")
                if request.method == "POST":
                    id = request.form.get("id", None)
                    action = request.form.get("action")
                    description = request.form.get("description")
                    if id:
                        image = PostModel.UploadObject.get(id)
                        if image:
                            if action == "delete":
                                image.delete()
                                obj = storage.get(image.name)
                                if obj:
                                    obj.delete()
                                self.flash_success("Image deleted successfully!")
                            else:
                                image.update(description=description)
                                self.flash_success("Image updated successfully!")
                    else:
                        abort(404, "No image ID provided")
                    return redirect(url_for("PostAdmin:images"))

                else:
                    page = request.args.get("page", 1)
                    per_page = self.get_config("PAGINATION_PER_PAGE", 25)
                    images = PostModel.UploadObject.all()\
                        .filter(PostModel.UploadObject.type == "IMAGE")\
                        .order_by(PostModel.UploadObject.name.asc())
                    images = images.paginate(page=page, per_page=per_page)
                    return self.render(images=images,
                                       view_template=template_page % "images")

            @route("upload-image", methods=["POST"], endpoint="PostAdmin:upload_image")
            def upload_image(self):
                """
                Placeholder for markdown
                """
                try:
                    ajax = request.form.get("ajax", False)
                    allowed_extensions = ["gif", "png", "jpg", "jpeg"]

                    if request.files.get("file"):
                        _file = request.files.get('file')
                        obj = storage.upload(_file,
                                             prefix="post",
                                             allowed_extensions=allowed_extensions,
                                             acl="public-read")

                        if obj:
                            obj_url = obj.get_url()
                            description = os.path.basename(obj.name)
                            description = description.replace(".%s" % obj.extension, "")
                            description = description.split("__")[0]
                            upload_object = PostModel.UploadObject.create(name=obj.name,
                                                                          provider=obj.provider_name,
                                                                          container=obj.container_name,
                                                                          local_path=obj.local_path,
                                                                          extension=obj.extension,
                                                                          type=obj.type,
                                                                          object_path=obj.object_path,
                                                                          object_url=obj_url,
                                                                          size=obj.size,
                                                                          description=description)
                            if ajax:
                                print upload_object.object_url
                                return jsonify({
                                    "id": upload_object.id,
                                    "url": upload_object.object_url
                                })
                            else:
                                self.flash_success("Image '%s' uploaded successfully!" % upload_object.name)

                    else:
                        self.flash_error("Error: Upload object file is invalid or doesn't exist")
                except Exception as e:
                    self.flash_error("Error: %s" % e.message)
                return redirect(url_for("PostAdmin:images"))

        return view
    return wrapper