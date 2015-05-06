__author__ = 'ejc84332'

from asset import Asset


class Page(Asset):

    def __init__(self, ws_connector, identifier=None):
        super(self.__class__, self).__init__(ws_connector)
        self.asset_type = "page"
        self.identifier = identifier
        # self.asset = None       ## stored as string. Do we want this to constantly set a new asset as traversals occur?

    def explore_asset(self):
        new_asset = self.get_asset_as_array()['asset']['page']
        self.set_asset(new_asset)
        return new_asset

    def nodes(self):
        new_asset = self.get_asset_as_array()['structuredDataNodes']['structuredDataNode']
        self.set_asset(new_asset)
        return new_asset
