"""Contains data handling functionality. The DataHandler class is resposible
for serving all data necessary for the recommender"""


class DataHandler(object):
    """Represents the interface each data provider class should implement."""

    def get_content(self):
        """Returns a dictionary containing the data on which recommendations
        are based."""
        raise NotImplementedError

    def get_top_matching_items(self, item, limit):
        """Returns a dictionary containing the top matching items to
        a given item.

        parameters:
            item The item for which the top matches are returned
            limit The max number of results returned, if 0 should
                  return all results found"""
        raise NotImplementedError

    def update_top_matching_items(self, top_matches):
        """Save updated data for item similarities

        parameters:
            top_mathces A dictionary containing items that should be updated"""
        raise NotImplementedError

    def transposed_content(self):
        """Transpose the content so that properties become keys
        and keys become properties."""
        result = {}
        for key, value in self.get_content().items():
            for property, score in value.items():
                result.setdefault(property, {})
                result[property][key] = score
        return result
