"""
Portfolio
"""

from portfolio import (Portfolio,
                   route,
                   abort,
                   request,
                   redirect,
                   url_for,
                   jsonify,
                   session)
from portfolio.component import (storage,
                             mailer,
                             cache,
                             recaptcha)
from portfolio.component import views
from application import model
import datetime

Portfolio.bind(model.db.init_app)

@views.user_account(model=model)
class Login(Portfolio):
    route_base = "/"

@views.user_admin(model=model)
class UserAdmin(Portfolio):
    pass

@views.post_admin(model=model)
class PostManager(Portfolio):
    pass


@views.post_reader(model=model, types=["page"])
@views.contact_page()
class Index(Portfolio):
    route_base = "/"

    def index(self):
        self.set_meta__(title="Hello Portfolio!")
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


@views.post_reader(model=model, types=["blog", "article", "page"])
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
        self.set_meta__(title="Example Page")
        self.flash_error__("This is an error message set by error_ and called with show_flashed_message()")
        self.flash_success__("This is a success message set by error_ and called with show_flashed_message()")
        return self.render()


class AdminZone(Portfolio):

    def index(self):
        return "Admin Zone"
