"""
Pylot command line tool

manage.py

Command line tool to manage your application

"""

import argparse
from application import get_config
import application.model as model
from pylot import utils

config = get_config()
NAME = "Pylot Manager"
__version__ = config.APP_VERSION


def setup():

    # Create all db
    model.db.create_all()

    # :: USERS
    # SETUP USER ROLES
    roles = [
                {
                    "name": "SUPERADMIN",
                    "level": 99
                },
                {
                    "name": "ADMIN",
                    "level": 98
                },
                {
                    "name": "USER",
                    "level": 1
                },
             ]
    [model.UserModel.Role.new(name=role["name"], level=role["level"]) for role in roles]

    # ADD SUPER ADMIN
    email = config.ADMIN_EMAIL
    name = config.ADMIN_NAME
    if utils.is_valid_email(email):
        user = model.UserModel.User.get_by_email(email)
        if not user:
            model.UserModel.User.new(email=email, name=name, role="superadmin")
    else:
        raise AttributeError("Couldn't create new SUPERADMIN. 'email' is invalid")

    # :: POSTS
    # Set types
    post_types = ["Blog", "Article", "Page", "Other"]
    if not model.PostModel.Type.all().count():
        [model.PostModel.Type.new(t) for t in post_types]

    # Set categories
    post_categories = ["Blog"]
    if not model.PostModel.Category.all().count():
        [model.PostModel.Category.new(c) for c in post_categories]

    posts = [
        {
            "title": "About Us",
            "slug": "about",
            "type": "Page"
        },
        {
            "title": "Terms of Service",
            "slug": "tos",
            "type": "Page"
        }
    ]

def main():
    parser = argparse.ArgumentParser(description="%s  v.%s" % (NAME, __version__))
    parser.add_argument("--setup", help="Setup the system",  action="store_true")
    parser.add_argument("--upload-static-to-s3", help="Upload all static files to S3", action="store_true")
    arg = parser.parse_args()

    if arg.setup:
        # Default setup
        print("Setting up...")
        setup()

    if arg.upload_static_to_s3:
        # Upload static files to s3
        import flask_s3
        import run_www  # Or the main application run file
        print("Upload static files to S3")
        flask_s3.create_all(run_www.app)

if __name__ == "__main__":
    main()


