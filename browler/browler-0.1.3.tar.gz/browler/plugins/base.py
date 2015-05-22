"""
Interface for all Plugins
"""

class Plugin(object):

    def match(self, page):
        pass

    def run(self, page):
        pass

    def startup(self, context):
        pass

    def shutdown(self, crawler):
        pass

    def before_threads(self, context):
        """
        Global Startup hook
        :param context:
        :return:
        """
        pass

    def after_threads(self, context):
        """
        Global Shutdown hook
        :param context:
        :return:
        """
        pass
