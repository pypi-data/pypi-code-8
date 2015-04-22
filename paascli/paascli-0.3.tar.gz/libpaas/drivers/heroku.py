__author__ = 'hvishwanath'

import requests
import base64
import os
import sh
from .base import BasePaaSProvider, ArtifactHandler


class HerokuPythonArtifactHandler(ArtifactHandler):
    supported_types = ["org.python:src"]


    def __init__(self, pdpobj, artifact):
        ArtifactHandler.__init__(self, pdpobj, artifact)


    def handle_artifact(self):
        if self.artifact.type not in self.supported_types:
            raise NotImplementedError("No support for type : %s" % self.artifact.type)

        if self.artifact.type == "org.python:src":
            self.handle_python_src()
        else:
            raise NotImplementedError("No support for type : %s" % self.artifact.type)

    def handle_python_src(self):
        print "Detected artifact of type python source"
        print "Analyzing requirements..."
        for r in self.artifact.requirements:
            if r.type == "com.python:wsgi":

                pfile = os.path.join(self.pdpobj.pdpdir, "Procfile")
                pfilecontent = ""

                print "Detected wsgi application"

                if "com.python.wsgi.application" in r.options:
                    print "WSGI application is found in : %s" % r.options.get("com.python.wsgi.application")

                if "com.python.wsgi.servername" in r.options:
                    print "Requested server is : %s" % r.options.get("com.python.wsgi.servername")

                if r.options.get("com.python.wsgi.servername") == "platform":
                    module, app = r.options.get("com.python.wsgi.application").split("/")
                    pfilecontent = "web: python %s" % (module + ".py")

                print "Creating Procfile with content: \n%s" % pfilecontent
                file(pfile, "w").write(pfilecontent)
                print "Generated Procfile at : %s" % pfile
            elif r.type == "org.libpaas:env":
                print "Detected environment variables to be set for the application"
                o = dict(r.options)
                print "Setting env variables : \n\t%s" % str(o)

class HerokuJavaArtifactHandler(ArtifactHandler):
    pass


class Heroku(BasePaaSProvider):
    __singleton = None # the one, true Singleton
    server = "https://api.heroku.com"
    handler_map = {
        "org.python:src" : HerokuPythonArtifactHandler
    }
    headers = {'Accept': 'application/vnd.heroku+json; version=3'}

    def __new__(cls, *args, **kwargs):
        # Check to see if a __singleton exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __singleton objects
        if cls != type(cls.__singleton):
        #if not cls.__singleton:
            cls.__singleton = super(Heroku, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    @classmethod
    def getInstance(cls, *args):
        '''
        Returns a singleton instance of the class
        '''
        if not cls.__singleton:
            cls.__singleton = Heroku(*args)
        return cls.__singleton

    def __init__(self, username, password):
        self.username = username
        self.password = base64.b64decode(password)
        self.auth = self._get_auth()


    def _get_auth(self):
        a = "%s:%s" % (self.username, self.password)
        return base64.b64encode(a)


    def _create_app(self, appid):
        r = requests.post(
            url= self.server + "/apps",
            auth= (self.username, self.password),
            headers = self.headers,
            json = {"name": appid}
        )
        return r

    def _delete_app(self, appid):
        r = requests.delete(
            url= self.server + "/apps/" + appid,
            auth= (self.username, self.password),
            headers = self.headers,
        )
        return r


    def install_app(self, appid, pdpobject):
        print "Creating app : %s on heroku" % appid
        r = self._create_app(appid)
        if r.ok:
            print "Successfully created"
        else:
            print "Error creating application"
            print r.status_code, r.text
            return

        resp = r.json()

        git_url = resp["git_url"]
        web_url = resp["web_url"]
        print "Staging PDP archive.."
        print "PDP archive is at : %s" % pdpobject.pdpdir
        print "Configuring git.."
        cwd = os.getcwd()
        os.chdir(pdpobject.pdpdir)
        from sh import git
        git.init()

        print "Invoking the right artifact handler"
        plan = pdpobject.plan
        for a in plan.artifacts:
            h = self.handler_map.get(a.type)
            if h is None:
                raise NotImplementedError("No handler for artifact type : %s" % a.type)
            ho = h(pdpobject, a)
            ho.handle_artifact()

        print "Configuring git remote.."
        git.remote.add("heroku", git_url)


        def process_output(line):
            print(line)

        print "Adding files to repo"
        git.add(".")
        print "Committing to local repo"
        git.commit("-m", "Initial commit")
        print "Pushing to heroku"
        git.push("-u", "heroku", "master", _out=process_output, _tty_out=True)

        print "Uploaded app successfully.."
        print "App is available at : %s" % web_url

        return appid, git_url, web_url


    def start_app(self, appid):
        r = requests.patch(
            url= self.server + "/apps/" + appid + "/formation",
            auth= (self.username, self.password),
            headers = self.headers,
            json = {
                "updates": [
                    {
                        "process": "web",
                        "quantity": 1,
                        "size": "1X"
                    }
                ]

                }
        )
        if r.ok:
            print "Application %s started" % appid
            return r
        else:
            print "Error starting application %s" % appid
            print r.status_code, r.text
            return


    def stop_app(self, appid):
        r = requests.patch(
            url= self.server + "/apps/" + appid + "/formation",
            auth= (self.username, self.password),
            headers = self.headers,
            json = {
                "updates": [
                    {
                        "process": "web",
                        "quantity": 0,
                        "size": "1X"
                    }
                ]

                }
        )
        if r.ok:
            print "Application %s stopped" % appid
            return r
        else:
            print "Error stopping application %s" % appid
            print r.status_code, r.text
            return

    def uninstall_app(self, appid):
        print "Uninstalling app : %s from heroku" % appid

        r = self._delete_app(appid)
        if r.ok:
            print "Successfully uninstalled"
            return r
        else:
            print "Error uninstalling application"
            print r.status_code, r.text
            return


    def list_apps(self):
        r = requests.get(
            url= self.server + "/apps/",
            auth= (self.username, self.password),
            headers = self.headers,
        )
        if r.ok:
            rval = []
            print "Retrieved applications on heroku"
            rj = r.json()
            for a in rj:
                d = dict()
                d["appid"] = a["name"]
                d["giturl"] = a["git_url"]
                d["weburl"] = a["web_url"]
                rval.append(d)
            return rval
        else:
            print "Error fetching application info on heroku"
            print r.status_code, r.text
            return


    def get_app_info(self, appid):
        r = requests.get(
            url= self.server + "/apps/" + appid,
            auth= (self.username, self.password),
            headers = self.headers,
        )
        if r.ok:
            print "Successfully queried for app info"
            return r
        else:
            print "Error querying for app information : %s" % appid
            print r.status_code, r.text
            return


    def list_services(self):
        pass

    def list_env_vars(self):
        pass

    def getenv(self, key):
        pass

    def setenv(self, key, value):
        pass


