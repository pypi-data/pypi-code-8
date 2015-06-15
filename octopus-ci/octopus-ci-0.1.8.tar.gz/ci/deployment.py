__author__ = 'soroosh'

import boto
import calendar


def check_deleted(stack, region):
    rows = []
    cf = boto.cloudformation.connect_to_region(region)
    events = cf.describe_stack_events(stack.stack_name)

    for event in events:
        d = event.__dict__
        d['stack_name'] = stack.name
        d['version'] = stack.version
        d['resource_type'] = d['resource_type']
        d['event_time'] = calendar.timegm(event.timestamp.timetuple())
        rows.append(d)

    rows.sort(key=lambda x: x['event_time'])
    if rows[-1]["resource_status"] == "DELETE_COMPLETE" and len(
            list(filter(lambda r: r["resource_status"] == "DELETE_IN_PROGRESS", rows))) == len(
            list(filter(lambda r: r["resource_status"] == "DELETE_COMPLETE", rows))):
        return True

    print(rows[-1]["resource_status"])
    return False


