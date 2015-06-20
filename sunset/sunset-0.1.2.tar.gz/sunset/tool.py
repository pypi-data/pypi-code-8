import re
import os
import logging
import datetime
from collections import defaultdict

from sunset.scanners.api import Scanner
from sunset.parser import Parser


log = logging.getLogger(__name__)


class ScanLog(object):
    all_levels = frozenset(['ALERT', 'WARNING'])
    all_outmodes = frozenset(['CSV'])

    def __init__(self):
        self.output_mode = None
        self.levels = self.all_levels
        self.within = 7
        self.counts = defaultdict(int)

    def set_levels(self, levels):
        for level in levels:
            if level not in self.all_levels:
                raise ValueError('"{0}" is not a valid level'.format(level))

        self.levels = frozenset(levels)

    def delta_as_str(self, delta, friendly=True):
        if friendly:
            if delta < 0:
                return 'expired yesterday' if delta == -1 else 'expired {0} days ago'.format(abs(delta))
            elif delta > 0:
                return 'expires tomorrow' if delta == 1 else 'expires in {0} days'.format(delta)
            else:
                return 'expired today'
        else:
            return str(delta)

    def emit(self, level, filename, lines, delta):
        if level not in self.levels:
            return

        if delta > self.within:
            return

        self.counts[level] += 1

        fileinfo = '{0}:{1}'.format(
            os.path.basename(filename),
            lines[0] if lines[0] == lines[1] else '{0}-{1}'.format(*lines))

        if self.output_mode == 'CSV':
            print ','.join(map(str, [level, fileinfo, self.delta_as_str(delta, friendly=False)]))
        else:
            print '%-16s %-32s %s' % (level, fileinfo, self.delta_as_str(delta))

    def get_message_count(self, level=None):
        if level is None:
            return sum(self.counts.values())
        else:
            return self.counts[level]

    def alert(self, filename, lines, delta):
        self.emit('ALERT', filename, lines, delta)

    def warn(self, filename, lines, delta):
        self.emit('WARNING', filename, lines, delta)


class ScanTool(object):
    re_date_range = re.compile(r'(-?\d+)d')
    re_file_ext = re.compile(r'\.([A-Za-z0-9]+)$')

    def __init__(self, scanlog):
        self.today = datetime.date.today()
        self.targets = ['.']
        self.recursive = None
        self.scanlog = scanlog

    def scan_files(self):
        items = list(self.targets)

        while items:
            item = items.pop()
            if os.path.isfile(item):
                yield os.path.abspath(item)
            elif os.path.isdir(item):
                for entry in os.listdir(item):
                    entry = os.path.abspath(os.path.join(item, entry))
                    if os.path.isfile(entry):
                        yield entry
                    elif os.path.isdir(entry) and self.recursive:
                        items.append(entry)

    def check_markers(self, filename, markers):
        for marker in markers:
            delta = (marker.expires - self.today).days
            if delta <= 0:
                self.scanlog.alert(filename, (marker.line_start, marker.line_end), delta)
            else:
                self.scanlog.warn(filename, (marker.line_start, marker.line_end), delta)

    def start_scan(self):
        for filename in self.scan_files():
            match = self.re_file_ext.search(os.path.basename(filename))
            if match:
                for scanner in Scanner.find_by_filetype(match.groups()[0]):
                    log.debug('Processing file %s with scanner %s', filename, scanner.__class__.__name__)
                    parser = Parser()

                    with open(filename, 'r') as scanfile:
                        scanner.scan(scanfile.readline, parser)

                    if parser.markers:
                        log.debug('...found %d markers', len(parser.markers))

                    self.check_markers(filename, parser.markers)

    @classmethod
    def config_from_args(cls, args):
        tool = cls(ScanLog())

        if args.levels:
            tool.scanlog.set_levels(args.levels.split(','))

        if args.within:
            match = cls.re_date_range.match(args.within.lower())
            if match:
                tool.scanlog.within = int(match.group(1))

        if args.recursive:
            tool.recursive = True

        if args.files:
            tool.targets = list(args.files)

        if args.output:
            tool.scanlog.output_mode = args.output

        return tool
