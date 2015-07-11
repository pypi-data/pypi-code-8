"""Main Recommender module."""

from exceptions import RecommendationDataUnavailableError
from exceptions import DataError


class Recommender(object):
    """Performs recommendations based on supplied data and a comparison
    algorithm.

    Attributes:
        data_provider         DataProvider instance
        similarity_algorithm  SimilarityMetric instance"""
    def __init__(self, data_provider, similarity_metric):
        self.__provider = data_provider
        self.__similarity = similarity_metric

    def item_based_recommendations(self, subject):
        """Build a list of recommendations relevant to the items's
        properties. Returns a list of tuples where the first item is
        the anticipated score the subject might give the recommended item
        the second is the recommended item.

        arguments:
            item The item for which recommendations are being built"""
        data = {}
        top_similarities = {}

        try:
            data = self.__provider.get_content()
            top_similarities = self.__provider.get_top_matching_items(subject)
        except DataError:
            raise RecommendationDataUnavailableError

        total_scores = {}
        score_sums = {}

        if top_similarities == {}:
            top_similarities = self.calculate_similarities(data, subject, 10)

        for similarity, other in top_similarities:
            if similarity <= 0:
                continue

            for item in data[other].keys():
                if item not in data[subject] or data[subject][item] == 0:
                    total_scores.setdefault(item, 0)
                    score_sums.setdefault(item, 0)

                    total_scores[item] += data[other][item] * similarity
                    score_sums[item] += similarity

        rankings = [(total / score_sums[item], item)
                    for item, total in total_scores.items()]
        return sorted(rankings, key=lambda x: x[0], reverse=True)

    def content_based_recommendations(self, subject):
        """Build a list of recommendations for a given subject based on
        the most similar content to the subject's properties. Returns a
        list of tuples where the first item is the anticipated score the
        subject might give the recommended item the second is the
        recommended item.

        arguments:
            item The item for which recommendations are being built"""

        data = {}
        content_similarities = {}
        try:
            data = self.__provider.get_content()
            content_similarities = self.__provider.get_top_matching_items()
        except DataError:
            raise RecommendationDataUnavailableError

        transposed = self.__provider.transposed_content()

        if content_similarities == {}:
            content_similarities = self.calculate_similarities(transposed,
                                                               limit=10)
        total_scores = {}
        score_sums = {}

        for item, rating in data[subject].items():
            for similarity, item2 in content_similarities[item]:
                if item2 in data[subject]:
                    continue

                total_scores.setdefault(item2, 0)
                score_sums.setdefault(item2, 0)

                total_scores[item2] += similarity * rating
                score_sums[item2] += similarity

        rankings = [(score / score_sums[item], item)
                    for item, score in total_scores.items()]
        return sorted(rankings, key=lambda x: x[0], reverse=True)

    def calculate_similarities(self, data, subject="", limit=3):
        """Generate a dictionary in which each key is an item and the
        value is a list of its top matches, e.g.:
        {"<item>": [(<similarity_score>, <similar_item>)]}

        arguments:
            data The poll from which to calculate the most similar items
            subject The subject we want to return results for. If left blank
                    all results are returned.
            limit The max number of top matching items returnedi. If 0 all
                  reslts are returned."""
        result = {}
        for item in data.keys():
            result[item] = self.__top_matches(item, data, limit)
        if subject == "":
            return result
        return result[subject]

    def __top_matches(self, item, data, limit=3):
        """Generate a list of top matching items to another item. The list
        consists of tuples: (<similarity_score>, <item>)

        arguments:
            item The item for which the top matches are calculated
            data The dataset from which scores are pulled
            limit The max number of top matching items returned, if 0 all
                  results are returned"""
        scores = [(self.__similarity(data[item], data[other]), other)
                  for other in data.keys() if other != item]
        if limit == 0:
            return sorted(scores, key=lambda x: x[0], reverse=True)
        return sorted(scores, key=lambda x: x[0], reverse=True)[:limit]
