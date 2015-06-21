from hitchserve import Service
import sys


class CronService(Service):
    def __init__(self, run, every=1, **kwargs):
        kwargs['log_line_ready_checker'] = lambda line: "READY" in line
        kwargs['command'] = [sys.executable, "-u", "-m", "hitchcron.cron", str(every),] + run
        super(CronService, self).__init__(**kwargs)
