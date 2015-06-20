import sys
import re
import datetime


class Marker(object):
    __slots__ = ['line_start', 'line_end', 'expires']

    def __init__(self, lineno):
        self.line_start = lineno
        self.line_end = lineno
        self.expires = None

    def __str__(self):
        if self.line_start == self.line_end:
            line = str(self.line_start)
        else:
            line = '{0}-{1}'.format(self.line_start, self.line_end)

        return 'Marker(line={0}, expires={1})'.format(line, self.expires)

    def __repr__(self):
        return str(self)


class Parser(object):
    re_sunset_begin = re.compile(
        r'>>SUNSET'
        r'\s+(?P<date>([1-9][0-9]{3})-(1[1-2]|0?[1-9])-([1-2][0-9]|3[0-1]|0?[1-9]))\s*'
        r'(?P<end><<)?')

    re_sunset_end = re.compile(r'<<SUNSET')

    def __init__(self):
        self.markers = []
        self._open_marker = None

    def parse_begin(self, lineno, comment):
        match = self.re_sunset_begin.search(comment)
        if match:
            if self._open_marker:
                print >>sys.stderr, 'Unmatched marker start at line', self._open_marker.line_start
                self.markers.append(self._open_marker)

            groupdict = match.groupdict()

            self._open_marker = Marker(lineno)
            print groupdict['date'].split('-')
            self._open_marker.expires = datetime.date(*map(int, groupdict['date'].split('-')))
            if groupdict['end']:
                self.markers.append(self._open_marker)
                self._open_marker = None

            return True

        return False

    def parse_end(self, lineno, comment):
        match = self.re_sunset_end.search(comment)
        if match:
            if self._open_marker:
                self._open_marker.line_end = lineno
                self.markers.append(self._open_marker)
                self._open_marker = None
            else:
                print >>sys.stderr, 'Dangling marker end at line', lineno
                # TODO log syntax warning
                pass

    def parse(self, lineno, comment):
        if not self.parse_begin(lineno, comment):
            self.parse_end(lineno, comment)

