import re
import io
import html
import logging
import collections
from piecrust import APP_VERSION, PIECRUST_URL
from piecrust.page import FLAG_RAW_CACHE_VALID


logger = logging.getLogger(__name__)


css_id_re = re.compile(r'[^\w\d\-]+')


# CSS for the debug window.
CSS_DEBUGWINDOW = """
text-align: left;
font-family: serif;
font-style: normal;
font-weight: normal;
position: fixed;
width: 50%;
bottom: 0;
right: 0;
overflow: auto;
max-height: 50%;
box-shadow: 0 0 10px #633;
"""

CSS_PIPELINESTATUS = """
background: #fff;
color: #a22;
"""

CSS_DEBUGINFO = """
padding: 1em;
background: #a42;
color: #fff;
"""

# HTML elements.
CSS_P = 'margin: 0; padding: 0;'
CSS_A = 'color: #fff; text-decoration: none;'

# Headers.
CSS_BIGHEADER = 'margin: 0.5em 0; font-weight: bold;'
CSS_HEADER = 'margin: 0.5em 0; font-weight: bold;'

# Data block elements.
CSS_DATA = 'font-family: Courier, sans-serif; font-size: 0.9em;'
CSS_DATABLOCK = 'margin-left: 2em;'
CSS_VALUE = 'color: #fca;'
CSS_DOC = 'color: #fa8; font-size: 0.9em;'

# 'Baked with PieCrust' text
BRANDING_TEXT = 'Baked with <em><a href="%s">PieCrust</a> %s</em>.' % (
        PIECRUST_URL, APP_VERSION)


def build_debug_info(page, data):
    """ Generates HTML debug info for the given page's data.
    """
    output = io.StringIO()
    try:
        _do_build_debug_info(page, data, output)
        return output.getvalue()
    finally:
        output.close()


def _do_build_debug_info(page, data, output):
    app = page.app

    print('<div id="piecrust-debug-info" style="%s">' % CSS_DEBUGWINDOW,
          file=output)

    print('<div id="piecrust-debug-info-pipeline-status" style="%s">' %
          CSS_PIPELINESTATUS, file=output)
    print('</div>', file=output)

    print('<div style="%s">' % CSS_DEBUGINFO, file=output)
    print('<p style="%s"><strong>PieCrust %s</strong> &mdash; ' %
          (CSS_P, APP_VERSION), file=output)

    # If we have some execution info in the environment,
    # add more information.
    if page.flags & FLAG_RAW_CACHE_VALID:
        output.write('baked this morning')
    else:
        output.write('baked just now')

    if app.cache.enabled:
        if app.env.was_cache_cleaned:
            output.write(', from a brand new cache')
        else:
            output.write(', from a valid cache')
    else:
        output.write(', with no cache')

    output.write(', ')
    if app.env.start_time != 0:
        output.write('in __PIECRUST_TIMING_INFORMATION__')
    else:
        output.write('no timing information available')

    print('</p>', file=output)
    print('</div>', file=output)

    if data:
        print('<div style="%s padding-top: 0;">' % CSS_DEBUGINFO, file=output)
        print(('<p style="%s cursor: pointer;" onclick="var l = '
                         'document.getElementById(\'piecrust-debug-details\'); '
                         'if (l.style.display == \'none\') l.style.display = '
                         '\'block\'; else l.style.display = \'none\';">' % CSS_P), file=output)
        print(('<span style="%s">Template engine data</span> '
                         '&mdash; click to toggle</a>.</p>' % CSS_BIGHEADER), file=output)

        print('<div id="piecrust-debug-details" style="display: none;">', file=output)
        print(('<p style="%s">The following key/value pairs are '
                         'available in the layout\'s markup, and most are '
                         'available in the page\'s markup.</p>' % CSS_DOC), file=output)

        filtered_data = dict(data)
        for k in list(filtered_data.keys()):
            if k.startswith('__'):
                del filtered_data[k]

        renderer = DebugDataRenderer(output)
        renderer.external_docs['data-site'] = (
                "This section comes from the site configuration file.")
        renderer.external_docs['data-page'] = (
                "This section comes from the page's configuration header.")
        renderer.renderData(filtered_data)

        print('</div>', file=output)
        print('</div>', file=output)

    print('</div>', file=output)

    print('<script src="/__piecrust_static/piecrust-debug-info.js"></script>',
            file=output)


class DebugDataRenderer(object):
    MAX_VALUE_LENGTH = 150

    def __init__(self, output):
        self.indent = 0
        self.output = output
        self.external_docs = {}

    def renderData(self, data):
        if not isinstance(data, dict):
            raise Exception("Expected top level data to be a dict.")
        self._writeLine('<div style="%s">' % CSS_DATA)
        self._renderDict(data, 'data')
        self._writeLine('</div>')

    def _renderValue(self, data, path):
        if data is None:
            self._write('&lt;null&gt;')
            return

        if isinstance(data, dict):
            self._renderCollapsableValueStart(path)
            with IndentScope(self):
                self._renderDict(data, path)
            self._renderCollapsableValueEnd()
            return

        if isinstance(data, list):
            self._renderCollapsableValueStart(path)
            with IndentScope(self):
                self._renderList(data, path)
            self._renderCollapsableValueEnd()
            return

        data_type = type(data)
        if data_type is bool:
            self._write('<span style="%s">%s</span>' % (CSS_VALUE,
                'true' if bool(data) else 'false'))
            return

        if data_type is int:
            self._write('<span style="%s">%d</span>' % (CSS_VALUE, data))
            return

        if data_type is float:
            self._write('<span style="%s">%4.2f</span>' % (CSS_VALUE, data))
            return

        if data_type is str:
            if len(data) > DebugDataRenderer.MAX_VALUE_LENGTH:
                data = data[:DebugDataRenderer.MAX_VALUE_LENGTH - 5]
                data += '[...]'
            data = html.escape(data)
            self._write('<span style="%s">%s</span>' % (CSS_VALUE, data))
            return

        self._renderCollapsableValueStart(path)
        with IndentScope(self):
            self._renderObject(data, path)
        self._renderCollapsableValueEnd()

    def _renderList(self, data, path):
        self._writeLine('<div style="%s">' % CSS_DATABLOCK)
        self._renderDoc(data, path)
        self._renderAttributes(data, path)
        rendered_count = self._renderIterable(data, path, lambda d: enumerate(d))
        if rendered_count == 0:
            self._writeLine('<p style="%s %s">(empty array)</p>' % (CSS_P, CSS_DOC))
        self._writeLine('</div>')

    def _renderDict(self, data, path):
        self._writeLine('<div style="%s">' % CSS_DATABLOCK)
        self._renderDoc(data, path)
        self._renderAttributes(data, path)
        rendered_count = self._renderIterable(data, path,
                lambda d: sorted(iter(d.items()), key=lambda i: i[0]))
        if rendered_count == 0:
            self._writeLine('<p style="%s %s">(empty dictionary)</p>' % (CSS_P, CSS_DOC))
        self._writeLine('</div>')

    def _renderObject(self, data, path):
        if hasattr(data.__class__, 'debug_render_func'):
            # This object wants to be rendered as a simple string...
            render_func_name = data.__class__.debug_render_func
            render_func = getattr(data, render_func_name)
            value = render_func()
            self._renderValue(value, path)
            return

        self._writeLine('<div style="%s">' % CSS_DATABLOCK)
        self._renderDoc(data, path)
        rendered_attrs = self._renderAttributes(data, path)

        if (hasattr(data, '__iter__') and
                hasattr(data.__class__, 'debug_render_items') and
                data.__class__.debug_render_items):
            rendered_count = self._renderIterable(data, path,
                    lambda d: enumerate(d))
            if rendered_count == 0:
                self._writeLine('<p style="%s %s">(empty)</p>' % (CSS_P, CSS_DOC))

        elif rendered_attrs == 0:
            self._writeLine('<p style="%s %s">(empty)</p>' % (CSS_P, CSS_DOC))

        self._writeLine('</div>')

    def _renderIterable(self, data, path, iter_func):
        rendered_count = 0
        with IndentScope(self):
            for i, item in iter_func(data):
                self._writeStart('<div>%s' % i)
                if item is not None:
                    self._write(' : ')
                    self._renderValue(item, self._makePath(path, i))
                self._writeEnd('</div>')
                rendered_count += 1
        return rendered_count

    def _renderDoc(self, data, path):
        if hasattr(data.__class__, 'debug_render_doc'):
            self._writeLine('<span style="%s">&ndash; %s</span>' %
                    (CSS_DOC, data.__class__.debug_render_doc))

        doc = self.external_docs.get(path)
        if doc is not None:
            self._writeLine('<span style="%s">&ndash; %s</span>' %
                    (CSS_DOC, doc))

    def _renderAttributes(self, data, path):
        if not hasattr(data.__class__, 'debug_render'):
            return 0

        attr_names = list(data.__class__.debug_render)
        if hasattr(data.__class__, 'debug_render_dynamic'):
            drd = data.__class__.debug_render_dynamic
            for ng in drd:
                name_gen = getattr(data, ng)
                attr_names += name_gen()

        invoke_attrs = []
        if hasattr(data.__class__, 'debug_render_invoke'):
            invoke_attrs = list(data.__class__.debug_render_invoke)
        if hasattr(data.__class__, 'debug_render_invoke_dynamic'):
            drid = data.__class__.debug_render_invoke_dynamic
            for ng in drid:
                name_gen = getattr(data, ng)
                invoke_attrs += name_gen()

        redirects = {}
        if hasattr(data.__class__, 'debug_render_redirect'):
            redirects = data.__class__.debug_render_redirect

        rendered_count = 0
        for name in attr_names:
            value = None
            render_name = name
            should_call = name in invoke_attrs

            if name in redirects:
                name = redirects[name]

            query_instance = False
            try:
                attr = getattr(data.__class__, name)
            except AttributeError:
                # This could be an attribute on the instance itself, or some
                # dynamic attribute.
                query_instance = True

            if query_instance:
                attr = getattr(data, name)

            if isinstance(attr, collections.Callable):
                attr_func = getattr(data, name)
                argcount = attr_func.__code__.co_argcount
                var_names = attr_func.__code__.co_varnames
                if argcount == 1 and should_call:
                    render_name += '()'
                    value = attr_func()
                else:
                    if should_call:
                        logger.warning("Method '%s' should be invoked for "
                                       "rendering, but it has %s arguments." %
                                       (name, argcount))
                        should_call = False
                    render_name += '(%s)' % ','.join(var_names[1:])
            elif should_call:
                value = getattr(data, name)

            self._writeLine('<div>%s' % render_name)
            with IndentScope(self):
                if should_call:
                    self._write(' : ')
                    self._renderValue(value, self._makePath(path, name))
            self._writeLine('</div>')
            rendered_count += 1

        return rendered_count

    def _renderCollapsableValueStart(self, path):
        self._writeLine('<span style="cursor: pointer;" onclick="var l = '
                    'document.getElementById(\'piecrust-debug-data-%s\'); '
                    'if (l.style.display == \'none\') {'
                    '  l.style.display = \'block\';'
                    '  this.innerHTML = \'[-]\';'
                    '} else {'
                    '  l.style.display = \'none\';'
                    '  this.innerHTML = \'[+]\';'
                    '}">'
                    '[+]'
                    '</span>' %
                    path)
        self._writeLine('<div style="display: none"'
                         'id="piecrust-debug-data-%s">' % path)

    def _renderCollapsableValueEnd(self):
        self._writeLine('</div>')

    def _makePath(self, parent_path, key):
        return '%s-%s' % (parent_path, css_id_re.sub('-', str(key)))

    def _writeLine(self, msg):
        self.output.write(self.indent * '  ')
        self.output.write(msg)
        self.output.write('\n')

    def _writeStart(self, msg=None):
        self.output.write(self.indent * '  ')
        if msg is not None:
            self.output.write(msg)

    def _write(self, msg):
        self.output.write(msg)

    def _writeEnd(self, msg=None):
        if msg is not None:
            self.output.write(msg)
        self.output.write('\n')


class IndentScope(object):
    def __init__(self, target):
        self.target = target

    def __enter__(self):
        self.target.indent += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.target.indent -= 1

