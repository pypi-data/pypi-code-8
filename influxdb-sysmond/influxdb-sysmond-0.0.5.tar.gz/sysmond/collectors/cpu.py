from .. import CollectorThread

import psutil

class CPUCollector(CollectorThread):
    identifier = 'cpu'

    def collect(self, cache):
        cpu = psutil.cpu_times_percent()

        return [{
            "name": "system.cpu",
            "columns": [
                "user",
                "nice",
                "system",
                "idle"
            ],
            "points": [[
                cpu.user,
                cpu.nice,
                cpu.system,
                cpu.idle
            ]]
        }]
