# Copyright 2015, Kevin Carter.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys


def is_int(value):
    """Return value as int if the value can be an int.

    :param value: ``str``
    :return: ``int`` || ``str``
    """
    try:
        return int(value)
    except ValueError:
        return value


def ensure_string(obj):
    """Return String and if Unicode convert to string.

    :param obj: ``str`` || ``unicode``
    :return: ``str``
    """

    if sys.version_info < (3, 2, 0) and isinstance(obj, unicode):
        return str(obj.encode('utf8'))
    else:
        return obj


def dict_update(base_dict, update_dict):
    """Return an updated dictionary.

    If ``update_dict`` is a dictionary it will be used to update the `
    `base_dict`` which is then returned.

    :param request_kwargs: ``dict``
    :param kwargs: ``dict``
    :return: ``dict``
    """
    if isinstance(update_dict, dict):
        base_dict.update(update_dict)

    return base_dict
