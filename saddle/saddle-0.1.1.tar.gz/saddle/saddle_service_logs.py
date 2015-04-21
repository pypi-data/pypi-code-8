import re, json, pyuv, os, signal, sys


# TODO: Grep
# TODO: Wait until (lambda line)         *starts from beginning* (timeout)
# TODO: Wait until json (lambda json)    *starts from beginning* (timeout)

class SubLog(object):
    def __init__(self, name, titles):
        self.titles = titles
        self.name = name
        self._end_of_file = 0
        self.max_length_of_titles = max([len(title) for title in titles])

    def _match_service(self, line_with_color):
        """Return line if line matches this service's name, return None otherwise."""
        line = re.compile("(\x1b\[\d+m)+").sub("", line_with_color)        # Strip color codes
        
        regexp = re.compile(r"^\[(.*?)\]\s(.*?)$")
        if regexp.match(line):
            title = regexp.match(line).group(1).strip()
            if title in self.titles:
                return (title, regexp.match(line).group(2))
        return None

    def tailf(self, lines=10):
        # TODO: Grep
        # TODO: Object that is callable // Grep
        # TODO: Stop printing everything twice
        # TODO: Color for tailed / printed logs
        
        # TODO: Number of lines to print before tailing
        
        loop = pyuv.Loop.default_loop()
        self.end_of_file = os.stat(self._logfilename).st_size
        
        def read_handle(handle, filename, events, error):
            """Callback every time data is appended to the file."""
            with open(self._logfilename, "r") as filehandle:
                filehandle.seek(self._end_of_file)
                tailportion = filehandle.read()
            for line in tailportion.split('\n'):
                matching_line = self._match_service(line)
                if matching_line is not None:
                    if len(self.titles) == 1:
                        sys.stdout.write(matching_line)
                    else:
                        sys.stdout.write("[{}] {}".format(matching_line[0].rjust(self.max_length_of_titles), matching_line[1]))
                    sys.stdout.write('\n')
                    sys.stdout.flush()
            self._end_of_file = os.stat(self._logfilename).st_size

        def signal_cb(handle, signum):
            """Handle ctrl-C if not in ipython shell"""
            event_handle.close()
            signal_h.close()

        event_handle = pyuv.fs.FSEvent(loop)
        event_handle.start(self._logfilename, 0, read_handle)
        
        signal_h = pyuv.Signal(loop)
        signal_h.start(signal_cb, signal.SIGINT)
        
        loop.run()

    def lines(self):
        """Return a list of lines output by this service."""
        lines = []
        with open(self._logfilename, "r") as log_handle:
            for line in log_handle:
                matching_line = self._match_service(line)
                if matching_line is not None:
                    if len(self.titles) == 1:
                        lines.append(matching_line[1])
                    else:
                        lines.append(matching_line)
        return lines

    def __repr__(self):
        if len(self.titles) == 1:
            return "\n".join(self.lines())
        else:
            return "\n".join(["[{}] {}".format(title.rjust(self.max_length_of_titles), line) for title, line in self.lines()])
    
    def __str__(self):
        return self.__repr__()
    
    def json(self):
        """Return a list of JSON objects output by this service."""
        lines = []
        for line in self.lines():
            try:
                if len(line) == 1:
                    lines.append(json.loads(line, strict=False))
                else:
                    lines.append(json.loads(line[1], strict=False))
            except ValueError:
                pass
        return lines
    
class ServiceLogs(SubLog):
    """Service log handling - tailing, matching lines, extracting JSON."""
    
    def __init__(self, name):
        self._name = name
        sout = name
        serr = "Err " + name
        setupout = "Setup " + name
        setuperr = "Err Setup " + name
        postout = "Post " + name
        posterr = "Post Err " + name
        
        self.out = SubLog(name, [sout ])
        self.err = SubLog(name, [serr ])
        self.setup = SubLog(name, [setupout, setuperr, ])
        self.setup.out = SubLog(name, [setupout, ])
        self.setup.err = SubLog(name, [setuperr, ])
        self.poststart = SubLog(name, [postout, posterr,])
        self.poststart.out = SubLog(name, [postout, ])
        self.poststart.err = SubLog(name, [posterr, ])
        super(ServiceLogs, self).__init__(name, titles=[sout, serr, setupout, setuperr, postout, posterr, ])
    
    def set_logfilename(self, logfilename):
        self._logfilename = logfilename
        self.out._logfilename = logfilename
        self.err._logfilename = logfilename
        self.setup._logfilename = logfilename
        self.setup.out._logfilename = logfilename
        self.setup.err._logfilename = logfilename
        self.poststart._logfilename = logfilename
        self.poststart.out._logfilename = logfilename
        self.poststart.err._logfilename = logfilename