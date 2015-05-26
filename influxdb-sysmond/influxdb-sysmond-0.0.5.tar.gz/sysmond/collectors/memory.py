from .. import CollectorThread

import psutil

class MemoryCollector(CollectorThread):
    identifier = 'memory'

    def collect(self, cache):
        mem = psutil.virtual_memory()

        return [{
            "name": "system.memory",
            "columns": [
                "total",
                "available",
                "used",
                "active",
                "inactive",
#                "wired",
                "free"
            ],
            "points": [[
                mem.total,
                mem.available,
                mem.used,
                mem.active,
                mem.inactive,
#                mem.wired,
                mem.free
            ]]
        }]
