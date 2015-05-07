__author__ = 'ces55739'


class List():

    def __init__(self, asset):
        self.asset = asset

    def __call__(self, *args, **kwargs):
        return self.asset

    def find(self, key, asset_structure=None):
        if asset_structure is None:
            asset_structure = self.asset

        matches = False
        if 'identifier' in asset_structure.keys() and asset_structure['identifier'] == key:
            matches = List(asset_structure)
        elif 'structuredDataNodes' in asset_structure.keys():
            for node in asset_structure['structuredDataNodes']['structuredDataNode']:
                matches = self.find(key, node)
                if matches is not False:
                    return matches

        return matches

    def find_all(self, key, asset_structure=None):
        if asset_structure is None:
            asset_structure = self.asset

        matches = []
        if 'identifier' in asset_structure.keys() and asset_structure['identifier'] == key:
            matches.append(List(asset_structure))
        elif 'structuredDataNodes' in asset_structure.keys():
            for node in asset_structure['structuredDataNodes']['structuredDataNode']:
                result = self.find_all(key, node)

                if len(result) > 0:
                    for item in result:
                        matches.append(item)

        return matches

    def set(self, value):
        self.asset['text'] = value
        return True

