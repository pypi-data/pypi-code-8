"""
Post Reader
"""

from portfolio import (Portfolio, utils, route, abort, redirect, request, url_for,
                   jsonify, session, AppError)



def post_reader(model, **kwargs):
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
    template_dir = kwargs["template_dir"] if "template_dir" in kwargs else "Portfolio/PostReader"
    types = kwargs["types"] if "types" in kwargs else []

    Post = model.PostModel.Post
    Type = model.PostModel.Type

    def wrapper(view):
        view_name = view.__name__

        @view.extends__
        class PostView(object):

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