from threads import CollectorThread
import psutil

class MemoryCollector(CollectorThread):
    identifier = 'memory'

    def run(self):
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

class CPUCollector(CollectorThread):
    identifier = 'cpu'

    def run(self):
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


class DiskCollector(CollectorThread):
    identifier = 'disk'

    def run(self):
        partitions = psutil.disk_partitions()

        data = []

        for part in partitions:
            usage = psutil.disk_usage(part.mountpoint)

            data.append({
                "name": "system.disk." + part.device,

                "columns": ["total", "used", "free"],
                "points": [[usage.total, usage.used, usage.free]]
            })

        return data
