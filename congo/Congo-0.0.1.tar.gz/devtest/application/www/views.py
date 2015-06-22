"""
Portfolio
"""

import datetime

from flask import url_for, request, redirect, abort, session, jsonify
from portfolio import Portfolio, utils, route
from portfolio.ext import mailer, recaptcha
from portfolio.component import ViewError


from flask import redirect, request, url_for, session, jsonify
from portfolio import Portfolio, route
from portfolio.ext import storage, mailer, cache, recaptcha
from portfolio.component.views import (post_admin, post_reader)

from portfolio.component import contact_page, user_account, cms_post

from application import model

Portfolio.bind(model.db.init_app)

@user_account.view(model=model)
class Login(Portfolio):
    route_base = "/"


@user_account.admin_view(model=model)
class UserAdmin(Portfolio): pass


@cms_post.admin_view(model=model)
class PostAdmin(Portfolio): pass


@cms_post.view(model=model, types=["page"])
@contact_page.view()
class Index(Portfolio):
    route_base = "/"

    def index(self):
        self.meta_data(title="Hello Portfolio!")
        return self.render()

    @route("upload", methods=["GET", "POST"])
    def upload(self):
        url = ""
        if request.method == "POST":
            _file = request.files.get('file')
            resp = storage.upload(_file, prefix="my-pictures/pat2", acl="public-read")
            return jsonify({"cdn_url": resp.get_url(),
                           "name": resp.name,
                            "size": resp.size})
        return self.render(file_url=url)


@cms_post.view(model=model, types=["blog", "article", "page"])
class Blog(Portfolio):
    pass

# Example
class Example(Portfolio):

    @cache.cached(10)
    def time(self):
        return str(datetime.datetime.now())

    def sendmail(self):
        mailer.send(to="mcx2082@gmail.com", subject="Portfolio is looking good",
                    body="Di yo sa\n Nou sonn'on lot jan!")
        return "email sent"

    def index(self):
        self.meta_data(title="Example Page")
        self.flash_error("This is an error message set by error_ and called with show_flashed_message()")
        self.flash_success("This is a success message set by error_ and called with show_flashed_message()")
        return self.render()


class AdminZone(Portfolio):

    def index(self):
        return "Admin Zone"
