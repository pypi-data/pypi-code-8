"""
Contact Page
"""

from portfolio import (Portfolio, utils, route, abort, redirect, request, url_for)
from portfolio.component import (mailer, recaptcha)

def contact_page(**kwargs):

    template_dir = kwargs["template_dir"] if "template_dir" \
                                             in kwargs else "Portfolio/ContactPage"
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

                contact_email = self.get_config__("CONTACT_PAGE_EMAIL_RECIPIENT")
                if recaptcha.verify():
                    if not email or not subject or not message:
                        error_message = "All fields are required"
                    elif not utils.is_valid_email(email):
                        error_message = "Invalid email address"
                    if error_message:
                        self.flash_error__(error_message)
                    else:
                        mailer.send_template("contact-us.txt",
                                             to=contact_email,
                                             reply_to=email,
                                             mail_from=email,
                                             mail_subject=subject,
                                             mail_message=message,
                                             mail_name=name
                                            )
                        self.flash_success__("Message sent successfully! We'll get in touch with you soon.")
                else:
                    self.flash_error__("Invalid security code")
                return redirect(url_for("ContactPage"))
            else:
                self.set_meta__(title="Contact Us")
                return self.render(view_template=template_page % "contact")
        return view
    return wrapper