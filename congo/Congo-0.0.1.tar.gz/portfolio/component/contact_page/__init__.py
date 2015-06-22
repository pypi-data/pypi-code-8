
"""
Contact Page
"""

from flask import request, redirect, url_for
from portfolio import Portfolio, utils, route
from portfolio.ext import mailer, recaptcha

Portfolio.register_component_template_static(__name__)

def view(**kwargs):
    template_dir = kwargs["template_dir"] if "template_dir" \
                                             in kwargs else "ContactPage"
    template_page = template_dir + "/%s.html"

    def wrapper(view):
        @view.extends__
        @route("contact", methods=["GET", "POST"], endpoint="ContactPage")
        def contact(self):
            if request.method == "POST":
                error_message = None
                email = request.form.get("email")
                subject = request.form.get("subject")
                message = request.form.get("message")
                name = request.form.get("name")

                contact_email = self.get_config("CONTACT_PAGE_EMAIL_RECIPIENT")
                if recaptcha.verify():
                    if not email or not subject or not message:
                        error_message = "All fields are required"
                    elif not utils.is_valid_email(email):
                        error_message = "Invalid email address"
                    if error_message:
                        self.flash_error(error_message)
                    else:
                        mailer.send_template("contact-us.txt",
                                             to=contact_email,
                                             reply_to=email,
                                             mail_from=email,
                                             mail_subject=subject,
                                             mail_message=message,
                                             mail_name=name
                                            )
                        self.flash_success("Message sent successfully! We'll get in touch with you soon.")
                else:
                    self.flash_error("Invalid security code")
                return redirect(url_for("ContactPage"))
            else:
                self.meta_data(title="Contact Us")
                return self.render(view_template=template_page % "contact")
        return view
    return wrapper