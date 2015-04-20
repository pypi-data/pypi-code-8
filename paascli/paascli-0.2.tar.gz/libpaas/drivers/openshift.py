__author__ = 'hvishwanath'

import requests
import base64
import os
import sh
from .base import BasePaaSProvider, ArtifactHandler


class OpenshiftPythonArtifactHandler(ArtifactHandler):
    supported_types = ["org.python:src"]
    cartridge = "python-2.7"


    def __init__(self, pdpobj, artifact):
        ArtifactHandler.__init__(self, pdpobj, artifact)


    def handle_artifact(self):
        if self.artifact.type not in self.supported_types:
            raise NotImplementedError("No support for type : %s" % self.artifact.type)

        if self.artifact.type == "org.python:src":
            return self.handle_python_src()
        else:
            raise NotImplementedError("No support for type : %s" % self.artifact.type)

    def handle_python_src(self):
        print "Detected artifact of type python source"
        print "Analyzing requirements..."
        renv = {}
        for r in self.artifact.requirements:
            if r.type == "com.python:wsgi":

                print "Detected wsgi application"

                if "com.python.wsgi.application" in r.options:
                    print "WSGI application is found in : %s" % r.options.get("com.python.wsgi.application")

                if "com.python.wsgi.servername" in r.options:
                    print "Requested server is : %s" % r.options.get("com.python.wsgi.servername")

                if r.options.get("com.python.wsgi.servername") == "platform":
                    module, app = r.options.get("com.python.wsgi.application").split("/")
                    renv["OPENSHIFT_PYTHON_WSGI_APPLICATION"] = module + ".py"

            elif r.type == "org.libpaas:env":
                print "Detected environment variables to be set for the application"
                o = dict(r.options)
                print "Setting env variables : \n\t%s" % str(o)
        return renv

class OpenshiftJavaArtifactHandler(ArtifactHandler):
    pass


class Openshift(BasePaaSProvider):
    __singleton = None # the one, true Singleton
    server = "https://openshift.redhat.com/broker/rest"
    handler_map = {
        "org.python:src" : (OpenshiftPythonArtifactHandler, "python-2.7")
    }
    headers = {'Accept': 'application/json; version=1.7'}
    data = {"nolinks": "true"}

    def __new__(cls, *args, **kwargs):
        # Check to see if a __singleton exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __singleton objects
        if cls != type(cls.__singleton):
        #if not cls.__singleton:
            cls.__singleton = super(Openshift, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    @classmethod
    def getInstance(cls, *args):
        '''
        Returns a singleton instance of the class
        '''
        if not cls.__singleton:
            cls.__singleton = Openshift(*args)
        return cls.__singleton


    def _verify_or_create_domain(self):
        """
        Verify that a domain with the name self.domain exists. Else create it.
        :return:
        """

        # Get all domains registered with the user
        r = requests.get(
            url=self.server + "/domains",
            auth=(self.username, self.password),
            headers=self.headers,
            json=self.data
        )
        if r.ok:
            names = []
            d = r.json()
            rdata = d["data"]
            if rdata:
                for d in rdata:
                    names.append(d["name"])
            if self.domain in names:
                return
        else:
            print "Error querying for domains for the configured user"
            print r.status_code, r.text
            return

        print "Domain %s is not created on rhcloud. Creating.."

        d = {"id": self.domain}
        d.update(self.data)

        r = requests.post(
            url= self.server + "/domains",
            auth= (self.username, self.password),
            headers = self.headers,
            json=d
        )
        if r.ok:
            print "Domain %s successfully created.." % self.domain

        else:
            print "Error creating domain for the configured user"
            print r.status_code, r.text
            return

        return r


    def __init__(self, username, password, domain="libpaas"):
        self.username = username
        self.domain = domain
        self.password = base64.b64decode(password)
        self.auth = self._get_auth()


    def _get_auth(self):
        a = "%s:%s" % (self.username, self.password)
        return base64.b64encode(a)


    def _create_app(self, appid, crid):
        d = {"name": appid, "cartridge": crid}
        d.update(self.data)

        print "Sending data : %s" % str(d)
        r = requests.post(
            url= self.server + "/domains/" + self.domain + "/applications",
            auth= (self.username, self.password),
            headers = self.headers,
            json = d
        )
        return r


    def _delete_app(self, appid):
        r = requests.delete(
            url= self.server + "/domains/" + self.domain + "/applications/" + appid,
            auth= (self.username, self.password),
            headers = self.headers,
            json=self.data
        )
        return r


    def install_app(self, appid, pdpobject):
        print "Analyzing artifacts.."
        plan = pdpobject.plan

        for a in plan.artifacts:
            h, c = self.handler_map.get(a.type)
            if h is None:
                raise NotImplementedError("No handler for artifact type : %s" % a.type)
            print "Detected app type : %s, Matching cartridge : %s" % (a.type, c)
            ho = h(pdpobject, a)
            renv = ho.handle_artifact()

            print "Creating application.."
            r = self._create_app(appid, h.cartridge)
            if r.ok:
                print "Application %s created" % appid
            else:
                print "Error creating application %s" % appid
                print r.status_code, r.text
                return

            # Set env variables on the app using rhc for now
            from sh import rhc
            for k, v in renv.items():
                rhc.env.set("%s=%s" % (k, v), "-a", appid)
                print "Set environment %s=%s on the app" % (k, v)

            resp = r.json()
            print "Received response : %s" % resp
            data = resp["data"]
            # Start staging it.
            git_url = data["git_url"]
            web_url = data["app_url"]

            print "Staging PDP archive.."
            print "PDP archive is at : %s" % pdpobject.pdpdir
            print "Configuring git.."

            # Empty out any samples given by the cartridge
            from sh import git
            import sh
            import tempfile
            import shutil
            import subprocess
            tmpdir = tempfile.mkdtemp()
            subprocess.check_call(["git", "clone", git_url, tmpdir])
            print "Cloned cartridge sample to %s" % tmpdir
            cwd = os.getcwd()
            os.chdir(tmpdir)
            git.rm("-r", "*")
            print "Removed all contents from cartridge repo"

            # Copy pdpdir contents
            subprocess.check_call("cp -rp %s/* ." % pdpobject.pdpdir, shell=True)
            print "Copied app contents to %s" % tmpdir
            sh.ls("-la", tmpdir)
            print "Adding and committing app code"
            git.add("*")
            git.commit("-m", "Adding app contents")

            print "Configuring git remote.."
            git.remote.add("rhc", git_url)

            print "Pushing to openshift"
            git.push("-u", "-f", "rhc", "master")

            print "Uploaded app successfully.."
            print "App is available at : %s" % web_url

            return appid, git_url, web_url


    def start_app(self, appid):

        d = {"event": "start"}
        d.update(self.data)
        r = requests.post(
            url= self.server + "/domains/" + self.domain + "/applications/" + appid + "/events",
            auth= (self.username, self.password),
            headers = self.headers,
            json = d
        )
        if r.ok:
            print "Application %s started" % appid
            return r
        else:
            print "Error starting application %s" % appid
            print r.status_code, r.text
            return


    def stop_app(self, appid):
        d = {"event": "stop"}
        d.update(self.data)

        r = requests.post(
            url= self.server + "/domains/" + self.domain + "/applications/" + appid + "/events",
            auth= (self.username, self.password),
            headers = self.headers,
            json = d
        )
        if r.ok:
            print "Application %s stopped" % appid
            return r
        else:
            print "Error stopping application %s" % appid
            print r.status_code, r.text
            return

    def uninstall_app(self, appid):
        print "Uninstalling app : %s from openshift" % appid

        r = requests.delete(
            url= self.server + "/domains/" + self.domain + "/applications/" + appid,
            auth= (self.username, self.password),
            headers = self.headers,
            json =self.data
        )

        if r.ok:
            print "Successfully uninstalled"
            return r
        else:
            print "Error uninstalling application"
            print r.status_code, r.text
            return


    def list_apps(self):
        r = requests.get(
            url= self.server + "/domains/" + self.domain + "/applications",
            auth= (self.username, self.password),
            headers = self.headers,
            json =self.data
        )

        if r.ok:
            rval = []
            print "Retrieved applications on openshift"
            resp = r.json()
            rj = resp["data"]
            for a in rj:
                d = dict()
                d["appid"] = a["name"]
                d["giturl"] = a["git_url"]
                d["weburl"] = a["app_url"]
                rval.append(d)
            return rval
        else:
            print "Error fetching application info on openshift"
            print r.status_code, r.text
            return


    def get_app_info(self, appid):
        r = requests.get(
            url= self.server + "/domains/" + self.domain + "/applications/" + appid,
            auth= (self.username, self.password),
            headers = self.headers,
            json=self.data
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


