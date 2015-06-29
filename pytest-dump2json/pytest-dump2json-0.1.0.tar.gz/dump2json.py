import json

report = {
        'passed':[],
        'skipped':[],
        'failed':[],
        'duration':0.0,
        'total_passed':0,
        'total_skipped':0,
        'total_failed':0,
        }

def pytest_addoption(parser):
    group = parser.getgroup("dump_to_json")
    group.addoption("--json-filename", action="store", default="test_report.json", help='The json filename to which to dump test results.')


def pytest_runtest_makereport(item, call, __multicall__):
    rep = __multicall__.execute()
    report['duration'] += rep.duration

    if rep.when == "call":
        if rep.passed:
            report['passed'].append(rep.nodeid)
            report['total_passed'] += 1
        if rep.failed:
            report['failed'].append(rep.nodeid)
            report['total_failed'] += 1
    else:
        if rep.skipped:
            report['skipped'].append(rep.nodeid)
            report['total_skipped'] += 1

    return rep


def pytest_sessionfinish(session, exitstatus):
    if report['passed'] or report['failed'] or report['skipped']:
        filename = session.config.getoption('--json-filename')
        with open(filename, 'w') as f:
            json.dump(report, f, sort_keys=True, indent=4, separators=(',', ': '))
