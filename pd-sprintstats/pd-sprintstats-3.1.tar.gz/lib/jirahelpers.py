# Copyright:: Copyright (c) 2015 PagerDuty, Inc.
# License:: Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and


def find_custom_field(field_name, jira):
    fields = jira.fields()
    for f in fields:
        if field_name in f['clauseNames']:
            return f


def find_board(board_name, greenhopper):
    boards = [b for b in greenhopper.boards() if b.name == board_name]
    if len(boards):
        return boards[0]
    return None


def find_sprint(sprint_name, board, greenhopper):
    sprints = [s for s in greenhopper.sprints(
        board.id) if s.name == sprint_name]
    if len(sprints):
        return sprints[0]
    return None


def find_project(project_name_or_key, jira):
    projects = [p for p in jira.projects()
                if p.name == project_name_or_key
                or p.key == project_name_or_key]
    if len(projects):
        return projects[0]
    return None


def fetch_subtasks(issues, jira):
    subtasks = jira.search_issues('parent in ({0})'.format(
        ','.join([i.key for i in issues])), expand='changelog', maxResults=-1)
    return subtasks
