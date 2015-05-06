__author__ = 'ejc84332'
import json

class Asset(object):

    def __init__(self, ws_connector, identifier=None):
        self.ws = ws_connector
        self.identifier = identifier
        self.asset_type = None
        self.asset = None       ## stored as string. Do we want this to constantly set a new asset as traversals occur?

    def set_identifier(self, identifier):
        self.identifier = identifier

    def read_asset(self, identifier=None):
        # can either set identifier on creation or when you call read_asset
        if self.identifier is not None:
            self.set_identifier(self.identifier)
        else:
            self.set_identifier(identifier)

        read_asset = self.ws.read(self.identifier, self.asset_type)

        # set the asset value to the writable asset structure
        asset_structure = self.get_asset_structure(read_asset)

        self.set_asset(asset_structure)

        return asset_structure

    def create_asset(self, asset):
        return self.ws.create(asset)

    def edit_asset(self, asset):
        return self.ws.edit(asset)

    def delete_asset(self, identifier=None):
        if identifier:
            self.set_identifier(identifier)
        return self.ws.delete(self.identifier, self.asset_type)

    def get_asset_structure(self, asset=None):
        if asset is None:
            asset = self.asset
        return self.ws.build_asset_structure(asset)

    def publish_asset(self, identifier=None):
        if identifier:
            self.set_identifier(identifier)
        return self.ws.publish(self.identifier, self.asset_type)

    def unpublish_asset(self, identifier=None):
        if identifier:
            self.set_identifier(identifier)
        return self.ws.unpublish(self.identifier, self.asset_type)

    def move_asset(self, new_identifier=None, identifier=None):
        if identifier:
            old_identifier = identifier
        else:
            old_identifier = self.identifier

        if new_identifier:
            self.set_identifier((new_identifier))
        return self.ws.move(self.identifier, old_identifier, self.asset_type)

    def rename_asset(self, identifier, new_name):
        if identifier:
            self.set_identifier((identifier))

        return self.ws.rename(self.identifier, new_name, self.asset_type)

    def is_in_workflow_asset(self, identifier=None):
        if identifier:
            self.set_identifier(identifier)
        return self.ws.is_in_workflow(self.identifier, self.asset_type)

    ## Test functions

    def get_identifier(self):
        return self.identifier

    def set_asset(self, asset):
        self.asset = asset

    def get_asset_as_array(self, asset=None):
        if asset is None:
            asset = self.asset
        return json.loads(asset)

    def get_asset(self):
        return self.asset

    ## Need to find a way to put this on the right node level.
    ## OR -- Recurse through
    ## OR -- specify node level?
    def find(self, key):
        for item in self.get_asset():
            if item['identifier'] == key:
                return item.text

    ## Need to find a way to put this on the right node level.
    ## OR -- Recurse through
    ## OR -- specify node level?
    def find_all(self, key):
        matches = []
        for item in self.get_asset():
            if item['identifier'] == key:
                matches.append(item)

        return matches

    def text(self):
        return self.get_asset()['text']