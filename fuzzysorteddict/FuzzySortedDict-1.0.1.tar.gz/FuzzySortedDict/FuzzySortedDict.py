import bisect

import blist

class FuzzySortedDict(blist.sorteddict):
    """
    Sorted dictionary that returns the nearest matching key's value

    Subclasses the :class:`blist.sorteddict`, adding the functionality of
    getting the value of the key closest to the requested key, instead of
    requiring an exact match.  Optionally, a rounding mode can be specified,
    to return the nearest key less than or equal to or greater than or equal
    to the provided key.

    To find the nearest match, the keys will be compared and subtracted, so all
    types used as keys shall support comparison and subtraction will all other
    types used as keys.

    Note:
        The standard :class:`blist.sorteddict` arguments are supported in
        addition to the ones below.

    Arguments:
        rounding (optional): Round keys toward nearest (0, default),
            -infinity (<0), or infinity (>0).  When searching for the nearest
            key, the two closest keys will be resolved with this rounding mode.
    """

    def __init__(self, *args, **kwargs):
        self.rounding = kwargs.pop('rounding', 0)

        super(FuzzySortedDict, self).__init__(*args, **kwargs)

    def nearest_key(self, request):
        """
        Find the closest key to the given key, taking rounding mode into
        account.

        Arguments:
            request: key being looked for

        Returns:
            The key in the dictionary closest to request

        Raises:
            KeyError: An appropriate key could not be found, either because
                the dictionary is empty, or there is not a valid key based
                on the rounding mode.
        """
        key_list = self.keys()

        index = bisect.bisect_left(key_list, request)

        if len(key_list) <= 0:  # Empty dictionary!
            raise KeyError(request)
        elif index >= len(key_list):
            # Requested key is greater than any key in the list.
            if self.rounding > 0:
                raise KeyError("No key towards infinity found")
            return key_list[index-1]
        elif key_list[index] == request:
            # Exact match
            return key_list[index]
        elif index == 0 and self.rounding < 0:
            # Requested key is smaller than any key in the list.
            raise KeyError("No key towards -infinity found")
        elif self.rounding > 0: # Towards inf
            return key_list[index]
        elif self.rounding < 0: # Towards -inf
            return key_list[index-1]
        else:
            if abs(key_list[index] - request) < \
                abs(key_list[index-1] - request):
                # key at index is closer than previous key
                return key_list[index]
            else:
                return key_list[index-1]

    def __getitem__(self, key):
        """
        Gets the value corresponding to the key closest to the given key.

        Arguments:
            key: the key to look for

        Returns:
            the value corresponding to the closest key

        Raises:
            KeyError: The dictionary is empty
        """
        best_key = self.nearest_key(key)

        return super(FuzzySortedDict, self).__getitem__(best_key)
