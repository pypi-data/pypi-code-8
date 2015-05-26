from .. import CollectorThread

import psutil

class NetworkCollector(CollectorThread):
    identifier = 'net'

    def collect(self, cache):
        stats = psutil.net_io_counters(pernic=True)

        collected = []

        if 'prev' in cache:
            prev = cache['prev']

            for prev_if, data in cache['prev'].iteritems():
                collected.append({
                    "name": "system.net." + prev_if,

                    "columns": [
                        "bytes_tx",
                        "bytes_rx",
                        "packets_tx",
                        "packets_rx",
                        "errors_in",
                        "errors_out",
                        "dropped_in",
                        "dropped_out"
                    ],

                    "points": [[
                        (stats[prev_if].bytes_sent - prev[prev_if].bytes_sent),
                        (stats[prev_if].bytes_recv - prev[prev_if].bytes_recv),
                        (stats[prev_if].packets_sent - prev[prev_if].packets_sent),
                        (stats[prev_if].packets_recv - prev[prev_if].packets_recv),
                        (stats[prev_if].errin - prev[prev_if].errin),
                        (stats[prev_if].errout - prev[prev_if].errout),
                        (stats[prev_if].dropin - prev[prev_if].dropin),
                        (stats[prev_if].dropout - prev[prev_if].dropout)
                    ]]
                })

        # Update 'prev' data
        cache['prev'] = stats

        return collected
