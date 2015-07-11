"""Contains similarity algorithms used to determine how similar two items are.
Euclidean distance and Pearson corellation"""


def euclidean_distance(item1, item2):
    """Calculates a similarity rating between two data items. Returns
    a float value between 0 and 1. A value of 1 represents a high
    similarity rating, a value of 0 represents the lowest
    similarity rating.

    arguments:
    item1 & item2 - the itmes being compared
    """
    common_properties = __get_common_properties(item1, item2)
    sum_of_squares = 0
    if common_properties:
        for property in common_properties:
            sum_of_squares += (item2[property] - item1[property])**2
        return 1 / (1 + sum_of_squares**0.5)
    else:
        return 0


def pearson_corellation(item1, item2):
    """Calculate the pearson corellation coefficient between two items.
    Return a float representing the corellation coefficient. More info can
    be found here:
    https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
    """
    common_properties = __get_common_properties(item1, item2)
    item_count = len(common_properties)
    if item_count > 0:
        item1 = {k: item1[k] for k in common_properties}
        item2 = {k: item2[k] for k in common_properties}

        item1_sum = sum(item1.values())
        item2_sum = sum(item2.values())
    if item_count > 0:
        numerator = 0

        item1_squared_sum = 0
        item2_squared_sum = 0
        for key in item1.keys():
            factor_item1 = __factor(item1[key], item1_sum, item_count)
            factor_item2 = __factor(item2[key], item2_sum, item_count)

            numerator += factor_item1 * factor_item2
            item1_squared_sum += factor_item1**2
            item2_squared_sum += factor_item2**2

        return numerator / (item1_squared_sum**0.5 * item2_squared_sum**0.5)

    else:
        return 0


def tanimoto_coefficient(item1, item2):
    """Applicable in cases when similarity is calculated based on the
    presense or absense of a given characteristic. It's required that
    item1 and item2 have bitmaps of the characteristics. E.g. 1 corresponds
    to the presense of a characteristic - 0 to the absence."""

    common_properties = __get_common_properties(item1, item2)
    item_count = len(common_properties)
    if item_count == 0:
        return 0

    return float(item_count/(len(item1) + len(item2) - item_count))


def __factor(score, items_sum, item_count):
    """Helper method for the pearson correlation coefficient algorithm."""
    return score - items_sum/item_count


def __get_common_properties(item1, item2):
    """Return the common keys that two maps have"""
    return set(item1.keys()) & set(item2.keys())
