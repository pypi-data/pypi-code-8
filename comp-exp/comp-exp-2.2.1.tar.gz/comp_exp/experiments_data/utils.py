from functools import wraps
from IPython.core.display import _display_mimetype


# taken from IPython 3.0
def display_markdown(*objs, **kwargs):
    _display_mimetype('text/markdown', objs, **kwargs)


def summary_dec(summary):

    @wraps(summary)
    def wrapped(self, recursive=False, ipy_md=False):
        lines = []
        for line in summary(self):
            rec_obj = None
            indent = 0
            if isinstance(line, tuple):
                if len(line) == 2:
                    indent, line = line
                elif len(line) == 3:
                    indent, line, rec_obj = line

            if recursive and rec_obj is not None:
                inner_lines = rec_obj.summary(recursive=True)
                inner_lines = [' ' * (indent + 1) * 2 + line for line in inner_lines.split('\n')]
                inner_lines[0] = inner_lines[0][2:]
                lines.extend(inner_lines)
            else:
                lines.append(' ' * indent * 2 + '* ' + line)

        if ipy_md:
            display_markdown('\n'.join(lines), raw=True)
        return '\n'.join(lines)

    return wrapped
