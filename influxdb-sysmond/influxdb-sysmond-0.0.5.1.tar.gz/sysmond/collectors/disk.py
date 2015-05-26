from .. import CollectorThread

import psutil

class DiskCollector(CollectorThread):
    identifier = 'disk'

    def collect(self, cache):
        partitions = psutil.disk_partitions()

        data = []
        part_data = {}

        total_available = 0
        total_used = 0
        total_free = 0

        for part in partitions:
            usage = psutil.disk_usage(part.mountpoint)

            total_available += usage.total
            total_used += usage.used
            total_free += usage.free

            data.append({
                "name": "system.disk." + part.device,

                "columns": ["total", "used", "free"],
                "points": [[usage.total, usage.used, usage.free]]
            })

        data.append({
            "name": "system.disk.total",

            "columns": ["total", "used", "free"],
            "points": [[total_available, total_used, total_free]]
        })

        return data
