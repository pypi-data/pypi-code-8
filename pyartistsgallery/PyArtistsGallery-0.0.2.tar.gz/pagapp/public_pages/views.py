"""Views for public part of application.

Anonymous user should be able to view next pages:
 * main page of application - implemented by index();
 * page with contents of selected album - implemented by album();
 * login page - implemented by login().
"""

from jinja2 import TemplateNotFound
from flask import render_template, abort, current_app
from flask import redirect, url_for, request, flash
from flask_login import login_user, current_user

from pagapp.models.albums import Albums
from pagapp.models.pictures import Pictures
from pagapp.models.users import Users
from pagapp.models.configuration import Configuration
from pagapp.public_pages import public_pages
from pagapp.public_pages.forms import LoginForm
from pagapp.support_functions import flash_form_errors, is_first_run, \
    remove_danger_symbols
from pagapp.database_functions import is_upgrade_ready, upgrade_database


@public_pages.route('/')
@public_pages.route('/index')
def index():
    """Renders main page of art gallery."""
    try:
        if is_first_run() is True:
            current_app.logger.info(
                "Seems, there is first run of the application.")
            return redirect(url_for('service_pages.first_run'))
        elif is_upgrade_ready():
            upgrade_database()
            flash('Database updated successfully!', category='success')
        return render_template(
            'index.html',
            title=Configuration.query.first().gallery_title,
            albums=Albums.get_albums_list())
    except TemplateNotFound:
        current_app.logger.error("Couldn't find HTML template: index.html")
        abort(404)


@public_pages.route('/album/<album_url>')
def album(album_url):
    """Renders page for album with given album's URL.

    Argument:
    album_url -- unique string, by which album can be accessed via web
    interface.
    """
    album_url = remove_danger_symbols(album_url)
    try:
        matched_album = Albums.query.filter_by(
            url_part=album_url).first()
        matched_pictures = Pictures.query.filter_by(
            album_id=matched_album.id)
    except AttributeError:
        current_app.logger.error(
            "Album with URL does not found in the database.".format(album_url))
        flash('Album does not exists!', category='danger')
        return redirect(url_for('.index'))

    try:
        return render_template(
            'album.html',
            title=Configuration.query.first().gallery_title,
            current_album=matched_album,
            albums=Albums.get_albums_list(),
            pictures=matched_pictures)
    except TemplateNotFound:
        current_app.logger.error("Couldn't find template: album.html")
        abort(404)


@public_pages.route('/login', methods=['GET', 'POST'])
def login():
    """Renders login page.

    Function renders login page and raise messages for user if (s)he
    successfully logged in or not.
    """
    if current_user.is_authenticated() is True:
        return redirect(url_for('admin_panel.panel') + '#upload')

    login_form = LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        current_app.logger.debug(
            "Form within {} function validated".format(login.__name__))
        username = remove_danger_symbols(login_form.login.data)
        user = Users.query.filter_by(nickname=username).first()
        login_user(user)
        return redirect(url_for('admin_panel.panel') + '#upload')
    else:
        flash_form_errors(login_form)

    try:
        return render_template(
            "login.html",
            title=Configuration.query.first().gallery_title,
            form=login_form)
    except TemplateNotFound:
        current_app.logger.error("Couldn't find template: login.html")
        abort(404)
