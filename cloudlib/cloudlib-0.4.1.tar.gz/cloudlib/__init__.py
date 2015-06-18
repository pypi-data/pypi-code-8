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

__author__ = 'Kevin Carter'
__contact__ = 'Kevin Carter'
__email__ = 'kevin@cloudnull.com'
__copyright__ = '2014 All Rights Reserved'
__license__ = 'Apache2'
__date__ = '2014-04-20'
__version__ = '0.4.1'
__status__ = 'Production'
__appname__ = 'cloudlib'
__description__ = 'general purpose library for in application use'
__url__ = 'https://github.com/cloudnull/cloudlib'


class MissingConfig(Exception):
    """Raise this exception when the config variable is required."""
    pass


class MissingConfigValue(Exception):
    """Raise this exception when the config a value is required."""
    pass


class MessageFailure(Exception):
    """Raise this exception when an application fails processing a message."""
    pass


class MD5CheckMismatch(Exception):
    """Exception class when the md5 sum of a file is not what is expected."""
    pass
