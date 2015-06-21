"""Views for service pages.

Special pages with service functions. List of pages:
 * page, which shows on the first run of application --
implemented by first_run() function.
 * update page - implements by update_application().
"""

from jinja2 import TemplateNotFound
from flask import render_template, abort, request, \
    redirect, url_for, current_app
from sqlalchemy.exc import OperationalError

from pagapp.support_functions import flash_form_errors, is_first_run, \
    remove_danger_symbols
from pagapp.database_functions import create_database
from pagapp.service_pages import service_pages
from pagapp.service_pages.forms import FirstRunForm
from pagapp.models import db
from pagapp.models.users import Users
from pagapp.models.configuration import Configuration


@service_pages.route('/first_run', methods=['GET', 'POST'])
def first_run():
    """Renders service page on the first run."""
    if is_first_run() is False:
        current_app.logger.info(
            "Seems, there is not a first run of the application.")
        return redirect(url_for('public_pages.index'))
    else:
        create_database()

    form = FirstRunForm()

    # Add data from existing tables to form.
    try:
        form.gallery_title.data = Configuration.query.first().gallery_title
    except (OperationalError, AttributeError):
        pass
    try:
        form.username.data = Users.query.first().nickname
    except (OperationalError, AttributeError):
        pass

    if request.method == 'POST' and form.validate():
        current_app.logger.debug(
            "Form within {} function validated!".format(
                first_run.__name__))
        gallery_title = remove_danger_symbols(form.gallery_title.data)
        username = remove_danger_symbols(form.username.data)
        password = remove_danger_symbols(form.password.data)
        try:
            current_app.logger.debug("Trying to edit current configuration.")
            Configuration.query.first().gallery_title = gallery_title
        except AttributeError:
            current_app.logger.debug("Trying do add new configuration.")
            new_configuration = Configuration(gallery_title)
            db.session.add(new_configuration)

        try:
            current_app.logger.debug("Trying to edit current user.")
            Users.query.first().nickname = username
            Users.query.first().set_new_password(password)
        except AttributeError:
            current_app.logger.debug("Trying to add new user.")
            new_administrator = Users(username, password, True)
            db.session.add(new_administrator)

        db.session.commit()
        return redirect(url_for('public_pages.index'))
    else:
        current_app.logger.debug(
            "Form within {} function didn't validated!".format(
                first_run.__name__))
        flash_form_errors(form)

    try:
        return render_template('first_run.html', form=form)
    except TemplateNotFound:
        current_app.logger.error("Couldn't find HTML template: first_run.html")
        abort(404)
