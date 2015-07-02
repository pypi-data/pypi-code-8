"""
Some tools for docker events
"""

import docker_events


@docker_events.start.subscribe
def log_start(event_data, config=None):
    print "START", event_data, config


@docker_events.stop.subscribe
def log_stop(event_data, config=None):
    print "STOP", event_data, config
