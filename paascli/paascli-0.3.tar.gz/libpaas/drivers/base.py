__author__ = 'hvishwanath'


class BasePaaSProvider(object):
    def __init__(self, name):
        pass


    def install_app(self, appid, path_to_pdp):
        pass

    def start_app(self, appid):
        pass

    def stop_app(self, appid):
        pass

    def uninstall_app(self, appid):
        pass

    def list_apps(self):
        pass

    def get_app_info(self, appid):
        pass

    def list_services(self):
        pass

    def list_env_vars(self):
        pass

    def getenv(self, key):
        pass

    def setenv(self, key, value):
        pass


class ArtifactHandler(object):
    def __init__(self, pdpobj, artifact):
        self.pdpobj = pdpobj
        self.artifact = artifact



