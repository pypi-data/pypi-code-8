__author__ = 'ces55739'

class List():

    def __init__(self, asset):
        self.asset = asset

    def get_asset(self):
        return self.asset

    def find(self, key, asset_structure=None):
        if asset_structure is None:
            asset_structure = self.get_asset()

        match = False
        if 'identifier' in asset_structure and asset_structure['identifier'] == key:
            match = List(asset_structure).asset
        else:
            for node in asset_structure:
                if isinstance(asset_structure, list):
                    match = self.find(key, node)
                else:
                    match = self.find(key, asset_structure[node])
                if match is not False:
                    return match

        return match


    ## once find works, update this.
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
        if 'text' in self.asset:
            self.asset['text'] = value
            return True
        else:
            return False

