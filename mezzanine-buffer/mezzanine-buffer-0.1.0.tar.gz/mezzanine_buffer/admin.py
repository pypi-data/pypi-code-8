from __future__ import unicode_literals

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars

from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost


from buffpy import API
from django.utils import timezone
from mezzanine_buffer.utils import get_auth_settings, get_profiles


class BufferableAdminMixin(object):
    """
    Admin mixin that adds a "Send to Buffer" checkbox to the add/change
    views, which when checked, will send a Buffer update with the title and link
    to the object being saved, scheduled when the blog post is to publish
    """

    def make_formfield_html(self, settings):
        profiles = get_profiles(settings)

        def make_html_for_profile(profile):
            text = '{0} - {1}'.format(profile.service, profile.service_username)

            return '<option value="{0}">{1}</option>'.format(profile._id, text)


        option_fields = '\n'.join(map(make_html_for_profile, profiles))

        return """
            <div class='send_to_buffer_container'>
                <label class='vCheckboxLabel' for='id_send_to_buffer'>%s</label>
                <select id='id_send_to_buffer' name='buffer_profiles' multiple=multiple>
                    {0}
                </select>
            </div>
        """.format(option_fields)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        This is more or less heavily borrowed from the built in mezzanine.twitter implementation.

        Adds the "Send to Buffer" checkbox after the "status" field,
        provided by any ``Displayable`` models. The approach here is
        quite a hack, however the sane approach of using a custom
        form with a boolean field defined, and then adding it to the
        formssets attribute of the admin class fell apart quite
        horrifically.
        """
        formfield = super(BufferableAdminMixin,
            self).formfield_for_dbfield(db_field, **kwargs)

        auth_settings = get_auth_settings()

        if API and db_field.name == "status" and auth_settings:
            def wrapper(render):
                def wrapped(*args, **kwargs):
                    rendered = render(*args, **kwargs)
                    label = _("Send to Buffer Profiles")
                    return mark_safe(rendered + self.make_formfield_html(auth_settings) % label)
                return wrapped
            formfield.widget.render = wrapper(formfield.widget.render)
        return formfield

    def save_model(self, request, obj, form, change):
        """
        Sends a Buffer update with the title/short_url if applicable.
        """
        super(BufferableAdminMixin, self).save_model(request, obj, form, change)

        profile_ids = request.POST.getlist("buffer_profiles")
        if len(profile_ids) > 0:

            auth_settings = get_auth_settings()
            parts = (obj.site.domain, obj.get_absolute_url())
            # TODO look into https-forced case
            url = "http://%s%s" % parts

            message = truncatechars(obj, 140 - len(url) - 1)

            when = None

            # if something is scheduled for the future, don't post until then
            if obj.publish_date > timezone.now():
                when = obj.publish_date

            # TODO rewrite this when buffpy has multi profile support
            # we can save the extra profiles call + multiple POSTs
            profiles = filter(lambda p: p._id in profile_ids, get_profiles(auth_settings))
            for profile in profiles:
                profile.updates.new("%s %s" % (message, url), shorten=True, when=when)



class BufferableBlogPostAdmin(BufferableAdminMixin, BlogPostAdmin):
    pass

admin.site.unregister(BlogPost)
admin.site.register(BlogPost, BufferableBlogPostAdmin)