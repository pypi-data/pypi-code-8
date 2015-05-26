from .. import CollectorThread

import os

class LoadCollector(CollectorThread):
    identifier = 'load'

    def collect(self, cache):
        load = os.getloadavg()

        return [{
            "name":"system.load",

            "columns": ["1m", "5m", "15m"],
            "points": [[
                round(load[0], 2),
                round(load[1], 2),
                round(load[2], 2)
            ]]
        }]
