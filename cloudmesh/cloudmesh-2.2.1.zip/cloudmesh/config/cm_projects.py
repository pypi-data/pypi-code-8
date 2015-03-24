from cloudmesh.config.cm_config import cm_config
from string import Template
import os
import json


class cm_projects:

    """A class to manage the project ids for the various clouds."""

    def __init__(self, filename=None):
        """initializes based on cm_config and returns pointer to
           the projects dict."""
        # Check if the file exists
        self.config = cm_config(filename)

    @property
    def get_default(self):
        """returns the default project"""
        return self.config.get('cloudmesh.projects.default')

    # @default.setter
    def default(self, name):
        """sets the default project"""
        # check if name is in active projects
        # if it is, set the new default project.
        # if it is not through an exception and spit out a nice msg
        # explaining that the default project needs to be set
        self.add(name)
        self.config['cloudmesh']['projects']['default'] = name

    def add(self, name, status="active"):
        """adds a project with given status"""
        # add the name to the following array (make sure it is an array ;-)
        if status != 'default':
            if name not in self.names(status):
                self.config['cloudmesh']['projects'][status].append(name)

    def delete(self, name, status='active'):
        """adds a project with given status"""
        # add the name to the following array (make sure it is an array ;-)
        try:
            self.config['cloudmesh']['projects'][status].remove(name)
        except AttributeError, e:
            original = self.config['cloudmesh']['projects'][status]
            if name == original:
                # If it is a single value instead of a list, puts a empty string
                # as an action of deleting the value
                self.config['cloudmesh']['projects'][status] = ''

    def names(self, status="active"):
        """returns all projects in an array with a specified status"""
        return self.config.get('cloudmesh.projects')[status]

    def __str__(self):
        """returns the string representing the project"""
        # untested
        text = self.config.get('cloudmesh.projects')
        return str(text)

    def dump(self):
        """returns the dict in a string representing the project"""
        # untested
        return json.dumps(self.config.get('cloudmesh.projects'), indent=4)

    def write(self):
        """writes the updated dict to the config"""
        self.config.write(self.config.filename, 'yaml')
