__author__ = 'mjhunick'

import cgi
import os
import re
import types
from behave.model import Feature, Tag
from behave.parser import parse_feature, parse_file
from tabulate import tabulate
from yarara.reports.test_report_utils import gather_errors


class V1NumberMatcher(object):
    def __init__(self, exp):
        self.matcher = re.compile(exp)

    def __call__(self, s):
        m = self.matcher.match(s)
        return m is not None and m.end() == len(s)


is_reg_test_number = V1NumberMatcher('RT-[0-9]+')
is_reg_suite_number = V1NumberMatcher('RS-[0-9]+')
is_test_set_number = V1NumberMatcher('TS-[0-9]+')


def table_to_string(table):
    return tabulate([table.headings] + [row.cells for row in table.rows], tablefmt='orgtbl')


def example_to_string(example, tab='    '):
    result = 'Examples:'
    if example.name:
        result += ' ' + example.name
    if example.table:
        result += ('\n' + table_to_string(example.table)).replace('\n', '\n' + tab)
    return result


def step_to_string(step, tab='    '):
    result = step.keyword + ' ' + step.name
    if step.table:
        result += ':' + ('\n' + table_to_string(step.table)).replace('\n', '\n' + tab)
    return result


def steps_to_string(steps, tab='    '):
    return '\n'.join(step_to_string(step, tab) for step in steps)


def background_to_string(background, tab='    '):
    result = ''
    result += 'Background:'
    if background.name:
        result += ' ' + background.name
    result += ('\n' + steps_to_string(background.steps, tab)).replace('\n', '\n' + tab)
    return result


def scenario_to_string(scenario, tab='    '):
    result = ''
    if scenario.tags:
        result += ' '.join(['@' + tag for tag in scenario.tags]) + '\n'
    if scenario.type == 'scenario':
        result += 'Scenario:'
    elif scenario.type == 'scenario_outline':
        result += 'Scenario Outline:'
    else:
        raise NotImplemented
    if scenario.name:
        result += ' ' + scenario.name
    result += ('\n' + steps_to_string(scenario.steps, tab)).replace('\n', '\n' + tab)
    if scenario.type == 'scenario_outline' and scenario.examples:
        result += ('\n' + '\n'.join((example_to_string(ex, tab)) for ex in scenario.examples)).replace('\n', '\n' + tab)
    return result


def feature_to_string(feature, tab='    '):
    result = ''
    if feature.tags:
        result += ' '.join(['@' + tag for tag in feature.tags]) + '\n'
    result += 'Feature:'
    if feature.name:
        result += ' ' + feature.name
    result += '\n' + ('\n' + background_to_string(feature.background, tab)).replace('\n', '\n' + tab)

    if feature.scenarios:
        result += '\n' + '\n'.join(('\n' + scenario_to_string(sc, tab)).replace('\n', '\n' + tab) for sc in feature.scenarios)

    return result


def get_features_paths(base_dir='.'):
    feature_paths = []
    for (dir_path, _, filenames) in os.walk(base_dir):
        feature_paths += [os.path.join(dir_path, name) for name in filenames if name.endswith('.feature')]
    return feature_paths


def escape_html(s):
    return cgi.escape(s).replace('\n', '<br/>')


def get_html_results(scenario):
    result = ''
    log_name = scenario['name'].replace(' ', '_')
    log_path = os.path.join(os.environ['OUTPUT'], 'reports/logs/' + log_name + '/' + log_name + '.log')
    try:
        with open(log_path) as f:
            result += '<h3>Log</h3>' + escape_html(f.read())
    except IOError:
        print 'asdasd'
        pass
    error_msg, error_lines, error_step = gather_errors(scenario, True)
    html_test_log = ''
    if error_msg:
        html_test_log = '<strong>' + escape_html(error_msg) + '</strong>' + '<br/>'.join(escape_html(s) for s in error_lines)
    if html_test_log:
        result += '<br/><br/><h3>Error</h3>' + html_test_log
    return result


def feature_dir(yarara_dir):
    return os.path.join(yarara_dir, 'project/features/')


def results_dir(yarara_dir):
    return os.path.join(yarara_dir, 'output/results/')


def valid_tag(tag):
    return True  # FIXME


class FeatureWrapper(object):
    def __init__(self, filename):
        self.filename = filename
        self.reload()

    def __getattr__(self, name):
        return self.feature.__getattribute__(name)

    def reload(self):
        with open(self.filename) as f:
            data = f.read().decode('utf-8')
        self.feature = parse_feature(data, filename=self.filename)
        self.lines = data.split('\n')
        for scenario in self.feature.scenarios:
            scenario.feature = self
            scenario.add_tag = types.MethodType(add_scenario_tag, scenario)
            scenario.remove_tag = types.MethodType(remove_scenario_tag, scenario)

    def to_string(self):
        return '\n'.join(self.lines).encode('utf-8')

    def dump_to_file(self):
        with open(self.filename, 'w') as f:
            f.write(self.to_string())

    def add_scenario(self, scenario, tab='    ', reload=True):
        self.lines += [''] + [tab + line for line in scenario_to_string(scenario, tab).split('\n')]
        if reload:
            self.dump_to_file()
            self.reload()

    def add_scenarios(self, scenarios, reload=True):
        for sc in scenarios:
            self.add_scenario(sc, reload=False)
        if reload:
            self.dump_to_file()
            self.reload()

    def remove_scenarios_with_tags(self, tags, reload=True):
        keep_line = [True for _ in xrange(len(self.lines))]
        for i, sc in enumerate(self.scenarios):
            if set(tags) & set(sc.tags):
                # remove
                first_line = min([sc.line] + [t.line for t in sc.tags]) - 1
                last_line = max([sc.line] + [s.line for s in sc.steps]) - 1
                # try to remove one more line (empty) for formatting
                if last_line < len(self.lines) - 1 and self.lines[last_line + 1].strip() == '':
                    last_line += 1
                elif self.lines[first_line - 1].strip() == '':
                    first_line -= 1
                for i in xrange(first_line, last_line + 1):
                    keep_line[i] = False
                self.feature.scenarios = self.scenarios[:i] + self.scenarios[i + 1:]  # remove from scenarios list

        self.lines = [l for i, l in enumerate(self.lines) if keep_line[i]]

        if reload:
            self.dump_to_file()
            self.reload()


def add_scenario_tag(scenario, tag):
    feature = scenario.feature
    assert valid_tag(tag)
    if tag in scenario.tags:
        return
    if not scenario.tags:
        tag_line = scenario.line
        tag = Tag(tag, tag_line)
        # Append new line with tag before scenario
        feature.lines.insert(tag_line - 1, '@' + tag)
        scenario.location.line += 1
        for sc in feature.scenarios:
            if sc is not scenario and sc.line >= scenario.line:
                sc.location.line += 1
                for t in sc.tags:
                    t.line += 1
    else:
        line_number = scenario.tags[0].line
        line = feature.lines[line_number - 1]
        tag = Tag(tag, line_number)
        # Add tag before first tag
        tag_index = line.index('@')
        feature.lines[line_number - 1] = line[:tag_index] +  '@' + tag + ' ' + line[tag_index:]

    scenario.tags.insert(0, tag)


def remove_scenario_tag(scenario, tag):
    feature = scenario.feature
    assert valid_tag(tag)
    assert tag in scenario.tags
    tag_line = scenario.tags[scenario.tags.index(tag)].line
    i = feature.lines[tag_line - 1].find('@' + tag)
    if i > 0 and feature.lines[tag_line - 1][i-1] == ' ':
        feature.lines[tag_line - 1] = feature.lines[tag_line - 1].replace(' @' + tag, '', 1)
    else:
        feature.lines[tag_line - 1] = feature.lines[tag_line - 1].replace('@' + tag, '', 1)
    scenario.tags.remove(tag)

