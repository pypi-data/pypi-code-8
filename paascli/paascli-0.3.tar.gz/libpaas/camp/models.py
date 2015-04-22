__author__ = 'hvishwanath'

class CAMPModel(object):
    def __init__(self):
        pass


class Artifact(CAMPModel):
    def __init__(self, atype, content, requirements):
        self.type = atype
        self.content = content
        self.requirements = requirements

    @classmethod
    def create_from_dict(cls, d):
        atype = d.get("artifact_type", None)
        if "content" in d:
            content = Content.create_from_dict(d.get("content"))
        else:
            content = None

        if "requirements" in d:
            requirements = []
            reqs = d.get("requirements")
            for r in reqs:
                requirements.append(Requirement.create_from_dict(r))
        else:
            requirements = None


        return Artifact(atype, content, requirements)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        msg = """

        Artifact. Type: %s.
        Requirements :
        --------------
        %s

        """
        rm = []
        for r in self.requirements:
            rm.append(str(r))

        return msg % (self.type, "\n\t".join(rm))


class Content(CAMPModel):
    def __init__(self, href):
        self.href = href

    @classmethod
    def create_from_dict(cls, d):
        href = d.get("href", None)
        return Content(href)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Content. href: %s>" % self.href


class Requirement(CAMPModel):
    def __init__(self, rtype, options, fulfillment):
        self.type = rtype
        self.options = options
        self.fulfillment = fulfillment

    @classmethod
    def create_from_dict(cls, d):
        rtype = d.get("requirement_type")
        d.pop("requirement_type")
        options = d
        return Requirement(rtype, options, None)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Requirement. \n\tType: %s, \n\toptions: %s\n" % (self.type, self.options)


class Fulfillment(CAMPModel):
    def __init__(self, options, fid, characteristics):
        self.options = options
        self.id = fid
        self.characteristics = characteristics

    @classmethod
    def create_from_dict(cls, d):
        pass


class Characteristic(CAMPModel):
    def __init__(self, ctype, options):
        self.type = ctype
        self.options = options

    @classmethod
    def create_from_dict(cls, d):
        pass


class Service(CAMPModel):
    def __init__(self, sid, characteristics):
        self.id = sid
        self.characteristics = characteristics

    @classmethod
    def create_from_dict(cls, d):
        pass


class CAMPPlan(CAMPModel):
    def __init__(self, version, name, description, tags, artifacts=[], services=[]):
        self.version = version
        self.name = name
        self.description = description
        self.tags = tags
        self.artifacts = artifacts
        self.services = services

    @classmethod
    def create_from_dict(cls, d):
        version = d.get("camp_version", "1.0")
        name = d.get("name")
        description = d.get("description")
        tags = d.get("tags")
        artifacts = []
        services = []

        if "artifacts" in d:
            for a in d.get("artifacts"):
                artifacts.append(Artifact.create_from_dict(a))

        return CAMPPlan(version, name, description, tags, artifacts, services)


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        msg = """
        Plan:
        -----
        Name: %s
        Description : %s

        Artifacts:
        ---------
        %s

        Services:
        ----------
        %s
        """

        am = []
        for a in self.artifacts:
            am.append(str(a))

        sm = []
        for s in self.services:
            sm.append(str(s))

        return msg % (self.name, self.description, "\n\t".join(am), "\n\t".join(sm))
