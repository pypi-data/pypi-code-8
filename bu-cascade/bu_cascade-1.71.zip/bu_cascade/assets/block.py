__author__ = 'ces55739'

from asset import Asset


class Block(Asset):

    def __init__(self, ws_connector, identifier):
        super(self.__class__, self).__init__(ws_connector)
        self.asset_type = "block"
        self.identifier = identifier

    def explore_asset(self):
        return self.get_asset_as_array()['asset']['xhtmlDataDefinitionBlock']

    def data_definition_path(self):
        return self.get_asset_as_array()['definitionPath']