#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import webob

from oslo import messaging

from cinder.api import extensions
from cinder.api.openstack import wsgi
from cinder.api import xmlutil
from cinder import exception
from cinder.openstack.common import log as logging
from cinder.openstack.common import strutils
from cinder import utils
from cinder import volume
from cinder.openstack.common.gettextutils import _

LOG = logging.getLogger(__name__)

class BackportedVolumeActionsController(wsgi.Controller):
    def __init__(self, *args, **kwargs):
        super(BackportedVolumeActionsController, self).__init__(*args, **kwargs)
        self.volume_api = volume.API()

    @wsgi.action('os-set_bootable')
    def _set_bootable(self, req, id, body):
        """Update bootable status of a volume."""
        context = req.environ['cinder.context']
        try:
            volume = self.volume_api.get(context, id)
        except exception.VolumeNotFound as error:
            raise webob.exc.HTTPNotFound(explanation=error.msg)

        try:
            bootable = body['os-set_bootable']['bootable']
        except KeyError:
            msg = _("Must specify bootable in request.")
            raise webob.exc.HTTPBadRequest(explanation=msg)

        if isinstance(bootable, basestring):
            try:
                bootable = strutils.bool_from_string(bootable,
                                                     strict=True)
            except ValueError:
                msg = _("Bad value for 'bootable'")
                raise webob.exc.HTTPBadRequest(explanation=msg)

        elif not isinstance(bootable, bool):
            msg = _("'bootable' not string or bool")
            raise webob.exc.HTTPBadRequest(explanation=msg)

        update_dict = {'bootable': bootable}

        self.volume_api.update(context, volume, update_dict)
        return webob.Response(status_int=200)

class Volume_actions_backport(extensions.ExtensionDescriptor):
    """Enable volume actions
    """

    name = "BackportedVolumeActions"
    alias = "os-volume-actions-backport"
    namespace = "http://docs.openstack.org/volume/ext/backported-volume-actions/api/v2"
    updated = "2015-14-31T00:00:00+00:00"

    def get_controller_extensions(self):
        controller = BackportedVolumeActionsController()
        extension = extensions.ControllerExtension(self, 'volumes', controller)
        return [extension]

