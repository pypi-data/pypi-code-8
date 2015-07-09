
class Backend(object):
    option_mapping = {}

    def normalise_options(self, user_options):
        #TODO: apply option mapping
        return user_options

    def make_html_attributes(self, attributes):
        attributes = ['{}="{}"'.format(k, v) for k, v in attributes.items()]
        return ' '.join(attributes)
