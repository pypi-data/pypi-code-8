
# Copyright (c) 2015
#  Adam Tauno Williams <awilliam@whitemice.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from pprint import pformat

from coils.core import \
    NoSuchPathException, \
    SQLConnectionFactory, \
    fill_project7000_template, \
    CoilsException

from coils.core.omphalos import Render as Omphalos_Render

from coils.net import PathObject

from coils.logic.task.services.utility import \
    do_task_notification_preamble, \
    get_name_dictionary_matching_events, \
    send_task_notification_message, \
    EndTemplateException, \
    end_template


class TaskRuleDemo(PathObject):
    """
    For testing of task rulesets

    URI paramters:
        objectId
        taskId - presense inidcates that an e-mail should be sent
        floorSeconds - age of events to be included, default is ~1 year
        floorObjectId  - what the object id floor is for included events
    """

    def __init__(self, parent, name, **params):
        self.name = name
        PathObject.__init__(self, parent, **params)

    def is_public(self):
        return False

    def do_GET(self):

        """Parse URL parameters"""

        stream = BLOBManager.ScratchFile()



        object_id = None
        try:
            object_id = int(self.parameters['objectId'][0])
        except:
            raise CoilsException(
                'objectId parameter required in paramter string'
            )

        """Marshall task and perform notification preamble"""

        task = self.context.run_command('task::get', id=object_id, )

        prior_txt = pformat(
            Omphalos_Render(task, 65535 - 32768 - 8192, self.context)
        )
        stream.write(pformat(task))


        if not task:
            raise NoSuchPathException(
                'Unable to marshall task OGo#{0}'.format(object_id, )
            )

        if not template:
            raise NoSuchPathException(
                'Unable to marshall task notification template'
            )


        self.request.simple_response(
            200,
            mimetype='text/html',
            data=content,
        )
