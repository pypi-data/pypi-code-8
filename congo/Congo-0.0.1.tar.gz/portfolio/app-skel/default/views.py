"""
Your views
"""

from portfolio import (Portfolio,
                   mailer,
                   storage,
                   route,
                   abort,
                   request,
                   redirect,
                   url_for,
                   jsonify,
                   session,
                   AppError)
from portfolio.views import (login_view,
                         contact_view)

from application import model

LoginView = login_view(model.User)
ContactView = contact_view()

# Login
class Login(LoginView, Portfolio):
    pass

# Index
class Index(ContactView, Portfolio):
    route_base = "/"

    def index(self):
        self.meta_(title="Hello Portfolio!")
        return self.render()

# Example
class Example(Portfolio):
    def index(self):
        self.meta_(title="Example Page")
        self.self.flash_error_("This is an error message set by self.flash_error_ and called with show_flashed_message()")
        self.self.flash_success_("This is a success message set by self.flash_error_ and called with show_flashed_message()")
        return self.render()

