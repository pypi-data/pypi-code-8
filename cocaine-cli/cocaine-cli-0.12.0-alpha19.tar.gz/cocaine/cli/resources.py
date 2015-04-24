from .resource import Resource, ROResource

class Task(ROResource):

    url = "/task/%(_id)s/"

    def __init__(self, task_id, **kwargs):
        super(Task, self).__init__(**kwargs)
        self._data["_id"] = task_id

    def view_short(self):
        return "task %(_id)s\t status %(status)s"%self
        
    def view_simple(self):
        fields = ("_id", "status", "state")
        d = dict(((key, self[key]) for key in fields))
        return json.dumps(d, indent=2)
        


class Project(Resource):
    url = "/project/%(name)s/"

    def __init__(self, name, **kwargs):
        super(Project, self).__init__(**kwargs)
        self._data["name"] = name

    def view_versions(self):

        for k,v in self.versions.iteritems():

            if k in self.state["versions"]:
                state = self.state["versions"][k]
                if state["build"]:
                    sb = state["build"]

                    push(sb.status)
                    push7(sb.task)

                    if sb.status == "built":
                        push(sb.config)
                        push(sb.task)

                if state["deploy"]:

                    sd = state["deploy"]
                    for c in sd:
                        push(sd.status)
                        push(sd.task)
                        push(sd.config)
        

class Version(ROResource):
    url = "/project/%(name)s/version/%(version)s/"

    def __init__(self, project_id, version_tag, **kwargs):
        super(Version,self).__init__()
        self._data["name"] = project_id
        self._data["version"] = version_tag

class User(Resource):
    url = "/user/%(_id)s/"

    def __init__(self, login, **kwargs):
        super(User, self).__init__(*kwargs)
        self._data["_id"] = login

class Cluster(Resource):
    url = "/cluster/%(_id)s/"

    def __init__(self, cluster_id, **kwargs):
        super(Cluster, self).__init__(**kwargs)

        self._data["_id"] = cluster_id

