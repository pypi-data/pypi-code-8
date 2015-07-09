from django_image.backend import Backend


class DummyBackend(Backend):

    def get_url(self, django_file, options):
        sorted_options = sorted(options.items())
        params = ['{}={}'.format(k, v) for k, v in sorted_options]
        url = 'http://imgservice.com/api/{}'.format(django_file.url)
        if params:
            url += '?' + '&'.join(params)
        return url

    def get_html(self, django_file, options, attributes):
        """ Render the HTML appropriate for displaying the image
        """
        html = '<img src="{url}"{attributes}>'
        attributes = self.make_html_attributes(attributes)
        if attributes:
            attributes = ' ' + attributes
        return html.format(
                url=self.get_url(django_file, options),
                attributes=attributes,
            )
