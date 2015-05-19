# Copyright 2015 Oliver Cope
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

from __future__ import absolute_import
from __future__ import unicode_literals

from .core import BaseTemplateEnvironment


class Chameleon(BaseTemplateEnvironment):

    def __init__(self, environment=None, app=None, **kwargs):
        if environment is None:
            from chameleon import PageTemplateLoader
            environment = PageTemplateLoader(**kwargs)
        super(Chameleon, self).__init__(environment, app, **kwargs)

    def _get_template(self, template):
        return self.environment[template]

    def _render(self, template, data, stream):
        if stream:
            raise Exception("stream option not supported for Chameleon")
        return self._get_template(template).render(**data)
