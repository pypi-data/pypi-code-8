"""
Post Admin
"""

import datetime

from pylot import (Pylot,
                   utils,
                   route,
                   abort,
                   redirect,
                   request,
                   url_for,
                   jsonify,
                   session,
                   AppError)

from pylot.component import (mailer,
                             storage)
from flask_login import (LoginManager,
                         login_required,
                         login_user,
                         logout_user,
                         current_user)


def post_admin(model, **kwargs):

    def wrapper(view):
        template_dir = kwargs["template_dir"] if "template_dir" \
                                                 in kwargs else "Pylot/PostAdmin"
        template_page = template_dir + "/%s.html"
        PostStruct = model.PostStruct

        Pylot.set_context__(COMPONENT_POST_ADMIN=True)

        @view.extends__
        class AdminPost(object):
            route_base = "post-admin"
            __session_edit_key = "admin_post_edit_post"

            @route("/", endpoint="PostAdmin:index")
            def index(self):
                """
                List all posts
                """
                self.set_meta__(title="All Posts")
                per_page = self.get_config__("PAGINATION_PER_PAGE", 25)
                page = request.args.get("page", 1)
                id = request.args.get("id", None)
                slug = request.args.get("slug", None)
                status = request.args.get("status", "all")
                user_id = request.args.get("user_id", None)
                type_id = request.args.get("type_id", None)
                category_id = request.args.get("category_id", None)

                posts = PostStruct.Post.all()

                if id:
                    posts = posts.filter(PostStruct.Post.id == id)
                if slug:
                    posts = posts.filter(PostStruct.Post.slug == slug)
                if user_id:
                    posts = posts.filter(PostStruct.Post.user_id == user_id)
                if type_id:
                    posts = posts.filter(PostStruct.Post.type_id == type_id)
                if category_id:
                    posts = posts.join(PostStruct.PostCategory)\
                        .join(PostStruct.Category)\
                        .filter(PostStruct.Category.id == category_id)
                if status == "publish":
                    posts = posts.filter(PostStruct.Post.is_published == True)
                elif status == "draft":
                    posts = posts.filter(PostStruct.Post.is_draft == True)
                elif status == "revision":
                    posts = posts.filter(PostStruct.Post.is_revision == True)

                posts = posts.order_by(PostStruct.Post.id.desc())
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
                post = PostStruct.Post.get(id)
                if not post:
                    abort(404, "Post doesn't exist")

                self.set_meta__(title="Read: %s " % post.title)

                return self.render(post=post,
                                   view_template=template_page % "read")

            @route("upload-image", methods=["POST"], endpoint="PostAdmin:upload_image")
            def upload_image(self):
                """
                Placeholder for markdown
                """

                url = ""
                if request.files.get("file"):
                    url = storage.put(request.files.get('file'))

                else:
                    return "Couldn't upload file. No file exist", 401

                return self.render(file_url=url)

                # For when there is an error
                error = False
                if error:
                    return "error message", 401

                return jsonify({
                    "id": "",
                    "url": "", # full image url
                })

            @route("new", defaults={"id": None}, endpoint="PostAdmin:new")
            @route("edit/<id>", endpoint="PostAdmin:edit")
            def edit(self, id):
                """
                Create / Edit Post
                """
                self.set_meta__(title="Edit Post")

                types = [(t.id, t.name) for t in PostStruct.Type.all().order_by(PostStruct.Type.name.asc())]
                categories = [(c.id, c.name) for c in PostStruct.Category.all().order_by(PostStruct.Category.name.asc())]
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
                    post = PostStruct.Post.get(id)
                    if not post or post.is_revision:
                        abort(404, "Post doesn't exist")
                    checked_cats = [c.id for c in post.categories]

                return self.render(post=post,
                                   types=types,
                                   categories=categories,
                                   checked_categories=checked_cats,
                                   view_template=template_page % "edit"
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

                if status in ["draft", "publish"] and (not title or not type_id):
                    if not title:
                        self.flash_error__("Post Title is missing ")
                    if not type_id:
                        self.flash_error__("Post type is missing")

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
                    post = PostStruct.Post.get(id)
                    if not post:
                        abort(404, "Post '%s' doesn't exist" % id)

                    if status == "delete":
                        post.delete()
                        self.flash_success__("Post deleted successfully!")
                        return redirect(url_for("%s:index" % view ))

                    elif status == "revision":
                        data.update({
                            "user_id": current_user.id,
                            "parent_id": id,
                            "is_revision": True,
                            "is_draft": False,
                            "is_published": False,
                            "is_public": False
                        })
                        post = PostStruct.Post.create(**data)
                        return jsonify({"revision_id": post.id})

                elif status in ["draft", "publish"]:
                    data.update({
                        "is_published": is_published,
                        "is_draft": is_draft,
                        "is_revision": False,
                        "is_public": is_public
                    })
                    if id:
                        post = PostStruct.Post.get(id)
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
                        post = PostStruct.Post.create(**data)

                    post.set_slug(slug or title)

                    post.update_categories(map(int, post_categories))

                    if post.is_published and not post.published_date:
                        post.update(published_date=published_date)

                    self.flash_success__("Post saved successfully!")

                    endpoint = "read" if post.is_published else "edit"
                    return redirect(url_for("%s:%s" % (view, endpoint), id=post.id))

                else:
                    abort(400, "Invalid post status")

            @route("categories", methods=["GET", "POST"], endpoint="PostAdmin:categories")
            def categories(self):
                self.set_meta__(title__prepend="Post Categories")
                if request.method == "POST":
                    id = request.form.get("id", None)
                    action = request.form.get("action")
                    name = request.form.get("name")
                    slug = request.form.get("slug", None)
                    ajax = request.form.get("ajax", False)
                    try:
                        if not id:
                            cat = PostStruct.Category.new(name=name, slug=slug)
                            if ajax:
                                return jsonify({
                                    "id": cat.id,
                                    "name": cat.name,
                                    "slug": cat.slug,
                                    "status": "OK"
                                })
                            self.flash_success__("New category '%s' added" % name)
                        else:
                            post_cat = PostStruct.Category.get(id)
                            if post_cat:
                                if action == "delete":
                                    post_cat.delete()
                                    self.flash_success__("Category '%s' deleted successfully!" % post_cat.name)
                                else:
                                    post_cat.update(name=name, slug=slug)
                                    self.flash_success__("Category '%s' updated successfully!" % post_cat.name)
                    except Exception as ex:
                        if ajax:
                            return jsonify({
                                "error": True,
                                "error_message": ex.message
                            })

                        self.flash_error__("Error: %s" % ex.message)
                    return redirect(url_for("%s:categories" % view))

                else:
                    cats = PostStruct.Category.all().order_by(PostStruct.Category.name.asc())
                    return self.render(categories=cats,
                                       view_template=template_page % "categories")

            @route("types", methods=["GET", "POST"], endpoint="PostAdmin:types")
            def types(self):
                self.set_meta__(title__prepend="Post Types")
                if request.method == "POST":
                    try:
                        id = request.form.get("id", None)
                        action = request.form.get("action")
                        name = request.form.get("name")
                        slug = request.form.get("slug", None)
                        if not id:
                            PostStruct.Type.new(name=name, slug=slug)
                            self.flash_success__("New type '%s' added" % name)
                        else:
                            post_type = PostStruct.Type.get(id)
                            if post_type:
                                if action == "delete":
                                    post_type.delete()
                                    self.flash_success__("Type '%s' deleted successfully!" % post_type.name)
                                else:
                                    post_type.update(name=name, slug=slug)
                                    self.flash_success__("Type '%s' updated successfully!" % post_type.name)
                    except Exception as ex:
                        self.flash_error__("Error: %s" % ex.message)
                    return redirect(url_for("%s:types" % view))
                else:
                    types = PostStruct.Type.all().order_by(PostStruct.Type.name.asc())
                    return self.render(types=types,
                                       view_template=template_page % "types")

        return view
    return wrapper