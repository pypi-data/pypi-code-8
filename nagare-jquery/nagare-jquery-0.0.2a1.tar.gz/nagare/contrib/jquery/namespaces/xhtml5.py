import json
import peak.rules
from nagare import ajax, namespaces, partial, presentation, serializer
from nagare.namespaces import xhtml5, xhtml, xhtml_base
from nagare.ajax import javascript_dependencies


JQUERY_INTERNAL_PREFIX = '/static/jquery-nagare/'
JQUERY_EXTERNAL_PREFIX = '//code.jquery.com/'

JQUERY_PREFIX = JQUERY_EXTERNAL_PREFIX


def serialize_body(view_to_js, content_type, doctype):
    """Wrap a view body into a javascript code

    In:
      - ``view_to_js`` -- the view
      - ``content_type`` -- the rendered content type
      - ``doctype`` -- the (optional) doctype
      - ``declaration`` -- is the XML declaration to be outputed?

    Return:
      - Javascript to evaluate on the client
    """
    # Get the HTML or XHTML of the view
    body = serializer.serialize(
        view_to_js.output, content_type, doctype, False)[1]

    # Wrap it into a javascript code
    return json.dumps([view_to_js.js, view_to_js.id.encode('utf-8'), body])


class ViewToJs(object):

    def __init__(self, js, id, renderer, output):
        """Wrap a view into a javascript code

        In:
          - ``js`` -- name of the function to call, on the client, to change the
            DOM element
          - ``id`` -- id of the DOM element to replace on the client
          - ``renderer`` -- the current renderer
          - ``output`` -- the view (or ``None``)
        """
        # print js, id, renderer, output
        # print 'ViewToJs'
        self.js = js
        self.id = id
        self.renderer = renderer
        self.output = output


@peak.rules.when(serializer.serialize, (ViewToJs,))
def serialize(self, content_type, doctype, declaration):
    """Wrap a view into a javascript code

    In:
      - ``content_type`` -- the rendered content type
      - ``doctype`` -- the (optional) doctype
      - ``declaration`` -- is the XML declaration to be outputed?

    Return:
      - a tuple ('text/plain', Javascript to evaluate on the client)
    """
    if self.output is None:
        return ('application/json', '')

    # Get the javascript for the header
    head = presentation.render(self.renderer.head, self.renderer, None, None)

    # Wrap the body and the header into a javascript code
    return ('application/json', serialize_body(self, content_type, doctype))


class Update(ajax.Update):
    PRIORITIES = {1: 1,
                  2: 2,
                  4: 4,
                  5: 5,
                  41: 4}

    @classmethod
    def _generate_response(cls, render, args, js, component_to_update, r):
        """Wrap the rendering of a component into a JS statement

        In:
          - ``render`` -- rendering function to call
          - ``args`` -- ``render`` parameters
          - ``js`` -- JS function to wrap the rendering into
          - ``component_to_update`` -- id of the DOM element to update on the client
          - ``r`` -- renderer

        Return:
          - the JS statement
        """
        # print "_generate_response ",js, component_to_update
        return ViewToJs(js, component_to_update, r, render(r, *args))

    def _generate_render(self, renderer):
        """Generate the rendering function

        In:
          - ``renderer`` -- the current renderer

        Return:
          - the rendering function
        """
        request = renderer.request

        if request and not request.is_xhr and ('_a' not in request.params):
            javascript_dependencies(renderer)
            renderer.head.javascript_url('/static/jquery-nagare/ajax.js')

        js = 'nagare_updateNode'
        component_to_update = self.component_to_update
        if component_to_update is None:
            async_root = renderer.get_async_root()

            # Remember to wrap the root view into a ``<div>``
            component_to_update = async_root.id
            async_root.wrapper_to_generate = True
            js = 'nagare_replaceNode'

        # Get the ``id`` attribute of the target element or, else, generate one
        if isinstance(component_to_update, namespaces.xml._Tag):
            id_ = component_to_update.get('id')
            if id_ is None:
                id_ = renderer.generate_id('id')
                component_to_update.set('id', id_)
            component_to_update = id_

        render = self.render
        model = ()
        if not callable(render):
            model = (render if render != '' else async_root.model,)
            render = renderer.get_async_root().component.render
        # print "_generate_render ", js, self._generate_response
        return partial.Partial(self._generate_response, render, model, js, component_to_update)

    def generate_action(self, priority, renderer):
        """Generate the javascript action

        In:
          - ``priority`` -- type of the action (see ``callbacks.py``)
          - ``renderer`` -- the current renderer

        Return:
          - the javascript code
        """
        action = {'action': self._generate_replace(self.PRIORITIES[priority], renderer),
                  'priority': priority}

        if priority in [1, 41, 2]:
            action['session'] = renderer.get_session_id()

        return json.dumps(action)

# Overload base nagare Inputs


class _HTMLActionTag(object):

    def sync_action(self, renderer, action, with_request):
        """Register a synchronous action

        In:
          - ``renderer`` -- the current renderer
          - ``action`` -- action
          - ``with_request`` -- will the request and response objects be passed to the action?
        """
        self.set(self._actions[1], renderer.register_callback(
            self._actions[0], action, with_request))

    def async_action(self, renderer, action, with_request):
        """Register an asynchronous action

        In:
          - ``renderer`` -- the current renderer
          - ``action`` -- action
          - ``with_request`` -- will the request and response objects be passed to the action?
        """
        if not isinstance(action, Update):
            action = Update(action=action, with_request=with_request)

        self.set(self._actions[2], action.generate_action(
            self._actions[0], renderer))

    _async_action = async_action


class TextInput(_HTMLActionTag, xhtml.TextInput):
    _actions = (1, 'name', 'data-nagare-action')
    async_action = _HTMLActionTag.sync_action


class TextArea(_HTMLActionTag, xhtml.TextArea):
    _actions = (1, 'name', 'data-nagare-action')
    async_action = _HTMLActionTag.sync_action


class PasswordInput(_HTMLActionTag, xhtml.PasswordInput):
    _actions = (1, 'name', 'data-nagare-action')
    async_action = _HTMLActionTag.sync_action


class RadioInput(_HTMLActionTag, xhtml.RadioInput):
    _actions = (2, 'value', 'data-nagare-action')
    async_action = _HTMLActionTag.sync_action


class CheckboxInput(_HTMLActionTag, xhtml.CheckboxInput):
    _actions = (1, 'name', 'data-nagare-action')
    async_action = _HTMLActionTag.sync_action


class SubmitInput(_HTMLActionTag, xhtml.SubmitInput):
    _actions = (4, 'name', 'data-nagare-action')


class HiddenInput(_HTMLActionTag, xhtml.HiddenInput):
    _actions = (1, 'name', 'data-nagare-action')
    async_action = _HTMLActionTag.sync_action


class FileInput(_HTMLActionTag, xhtml.FileInput):
    _actions = (1, 'name', 'data-nagare-action')
    async_action = _HTMLActionTag.sync_action


class ImageInput(_HTMLActionTag, xhtml.ImageInput):
    _actions = (5, 'name', 'data-nagare-action')


class Select(_HTMLActionTag, xhtml.Select):
    _actions = (1, 'name', 'data-nagare-action')
    async_action = _HTMLActionTag.sync_action


class A(_HTMLActionTag, xhtml.A):
    _actions = (41, None, 'data-nagare-action')

    def async_action(self, renderer, action, with_request):
        """Register an asynchronous action

        In:
          - ``renderer`` -- the current renderer
          - ``action`` -- action
          - ``with_request`` -- will the request and response objects be passed to the action?
        """
        _HTMLActionTag.async_action(self, renderer, action, with_request)
        if not self.get('href'):
            self.set('href', '#')

    _async_action = async_action
    sync_action = xhtml.A.sync_action


class Img(_HTMLActionTag, xhtml.Img):

    sync_action = xhtml.Img.sync_action
    async_action = sync_action


class Input(_HTMLActionTag, xhtml5.Input):
    _actions = (1, 'name', 'data-nagare-action')


class Renderer(xhtml5.Renderer):

    a = xhtml.TagProp('a', set(xhtml_base.allattrs + xhtml_base.focusattrs + ('charset', 'type',
                                                                              'name', 'href', 'hreflang', 'rel', 'rev', 'shape', 'coords', 'target', 'oncontextmenu')), A)
    area = xhtml.TagProp('area', set(xhtml_base.allattrs + xhtml_base.focusattrs + (
        'shape', 'coords', 'href', 'nohref', 'alt', 'target')), A)
    button = xhtml.TagProp('button', set(
        xhtml_base.allattrs + xhtml_base.focusattrs + ('name', 'value', 'type', 'disabled')), SubmitInput)

    form = xhtml.TagProp('form', set(xhtml_base.allattrs + ('action', 'method', 'name',
                                                            'enctype', 'onsubmit', 'onreset', 'accept_charset', 'target')), xhtml.Form)

    img = xhtml.TagProp('img', set(xhtml_base.allattrs + ('src', 'alt', 'name', 'longdesc', 'width', 'height', 'usemap', 'ismap'
                                                          'align', 'border', 'hspace', 'vspace', 'lowsrc')), Img)
    input = xhtml.TagProp('input', set(xhtml_base.allattrs + xhtml_base.focusattrs + ('type', 'name', 'value', 'checked', 'disabled', 'readonly', 'size', 'maxlength', 'src'
                                                                                      'alt', 'usemap', 'onselect', 'onchange', 'accept', 'align', 'border')), TextInput)
    select = xhtml.TagProp('select', set(xhtml_base.allattrs + ('name', 'size',
                                                                'multiple', 'disabled', 'tabindex', 'onfocus', 'onblur', 'onchange', 'rows')), Select)
    textarea = xhtml.TagProp('textarea', set(xhtml_base.allattrs + xhtml_base.focusattrs + (
        'name', 'rows', 'cols', 'disabled', 'readonly', 'onselect', 'onchange', 'wrap')), TextArea)

    _specialTags = dict([(input_type + '_input', Input) for input_type in (
        'tel', 'search', 'url', 'email',
        'datetime', 'date', 'datetime-local_input',
                    'month', 'week', 'time', 'number', 'range', 'color'
    )])

    _specialTags.update(
        text_input=TextInput,
        radio_input=RadioInput,
        checkbox_input=CheckboxInput,
        submit_input=SubmitInput,
        hidden_input=HiddenInput,
        file_input=FileInput,
        password_input=PasswordInput,
        image_input=ImageInput
    )

    def AsyncRenderer(self, *args, **kw):
        """Create an associated asynchronous HTML renderer

        Return:
          - a new asynchronous renderer
        """
        # If no arguments are given, this renderer becomes the parent of the
        # newly created renderer
        if not args and not kw:
            args = (self,)

        return AsyncRenderer(*args, **kw)

    def get_session_id(self):
        return '_s=%d;_c=%05d' % (self.session.session_id, self.session.state_id)


class AsyncRenderer(xhtml5.AsyncRenderer, Renderer):

    def SyncRenderer(self, *args, **kw):
        """Create an associated synchronous HTML renderer

        Return:
          - a new synchronous renderer
        """
        # If no arguments are given, this renderer becomes the parent of the
        # newly created renderer
        if not args and not kw:
            args = (self,)

        return Renderer(*args, **kw)


@peak.rules.around(javascript_dependencies, (Renderer,))
def javascript_dependencies(next_method, renderer):
    head = renderer.head

    head.javascript_url(JQUERY_PREFIX + '/jquery-2.1.3.min.js')
