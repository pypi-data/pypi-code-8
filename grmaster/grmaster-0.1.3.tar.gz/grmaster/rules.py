# -*- coding: utf-8 -*-

"""Rules, which must be executing."""

#   grmaster - tool for dividing students into groups
#   Copyright (C) 2015  Lutov V. S. <vslutov@yandex.ru>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random, sys
from grmaster.manager import set_item, get_item

def divide(elem_count, group_count):
    """Random divide elems into groups."""
    sizes = [elem_count // group_count] * group_count
    prefix = elem_count % group_count
    sizes[:prefix] = [elem_count // group_count + 1] * prefix
    return sizes

def init_meta_english_groups(manager):
    """Init meta for english rule."""
    header = manager.config['english_header'][0]
    index = manager.students.header.index(header)
    manager.meta['_english_index'] = index
    per_group = int(manager.config['english_per_group'][0])

    levels = manager.students.split_by_header(header)
    levels.sort(key=len)

    manager.meta['_english_groups'] = [[[''] * per_group
                                        for i in range(stream_size)]
                                       for stream_size in manager.stream_sizes]
    meta_english_groups = manager.meta['_english_groups']

    groups = [[group[0], group[1], i]
              for group in manager.group_ids
              for i in range(per_group)]
    random.shuffle(groups)

    group_count = len(groups)
    group_size = len(manager.students) // group_count

    for i in range(len(levels)):
        level_group_count = len(levels[i]) // group_size
        if level_group_count == 0:
            level_group_count = 1
        if i == len(levels) - 1:
            level_group_count = group_count
        else:
            group_count -= level_group_count

        for group, students in zip(groups,
                                   divide(len(levels[i]), level_group_count)):
            set_item(meta_english_groups, group, [levels[i][0][index], students])

        groups = groups[level_group_count:]

def init_meta_wishes(manager):
    """Meta wishes usefull with assignement."""
    if 'stream_tables' in manager.config:
        header = manager.config['stream_tables']
        manager.meta['_wishes'] = [None for i in range(len(manager.students))]
        for i in range(len(header)):
            if header[i] == '':
                break
            else:
                student_names = manager.meta[header[i]]
                for student_name in student_names:
                    student = manager.students.get_by_column(0, student_name[0])
                    student_index = manager.students.body.index(student)
                    manager.meta['_wishes'][student_index] = i

def english_rule(manager, student, group):
    """Test if student can study in group."""
    index = manager.meta['_english_index']
    for en_type, count in get_item(manager.meta['_english_groups'], group):
        if en_type == student[index] and count > 0:
            return True
    return False

def english_assign(manager, student, group):
    """Try to add student to group."""
    index = manager.meta['_english_index']
    for en_box in get_item(manager.meta['_english_groups'], group):
        if en_box[0] == student[index] and en_box[1] > 0:
            en_box[1] -= 1
            return True

def add_english(manager):
    """Add english rule and add for futher using."""
    init_meta_english_groups(manager)
    manager.rule_chain.append(english_rule)
    manager.assign_chain.append(english_assign)

def get_wishes_count(manager):
    """Return count of filled wishes."""
    all_wishes = filled_wishes = 0
    if '_wishes' in manager.meta:
        meta_wishes = manager.meta['_wishes']
        for i in range(len(manager.students)):
            if meta_wishes[i] is not None:
                all_wishes += 1
                if manager.result_groups[i][0] == meta_wishes[i]:
                    filled_wishes += 1
    if 'friends_table' in manager.config:
        friends_table = manager.meta[manager.config['friends_table'][0]]
        for row in friends_table:
            all_wishes += 1
            student_one = manager.students.get_by_column(0, row[0])
            student_one = manager.students.body.index(student_one)
            student_two = manager.students.get_by_column(0, row[1])
            student_two = manager.students.body.index(student_two)
            if manager.result_groups[student_one] == manager.result_groups[student_two]:
                filled_wishes += 1
    return [filled_wishes, all_wishes]

def assign_friends(manager):
    """First, assign friends."""

def assign_wishes(manager):
    """Just try to assign, who wish to be assigned."""
    if '_wishes' in manager.meta:
        meta_wishes = manager.meta['_wishes']
        wishes = []
        has_score = 'score_header' in manager.config
        if has_score:
            score_index = manager.students.header.index(manager.config['score_header'][0])
        for i in range(len(manager.students)):
            if meta_wishes[i] is not None:
                stream = meta_wishes[i]
                student = manager.students[i]
                score = int(student[score_index]) if has_score else 0
                wishes.append([score, student, stream])

        wishes.sort(reverse=True)

        for score, student, stream in wishes:
            for group in range(manager.stream_sizes[stream]):
                if manager.assign_student(student, [stream, group]):
                    break

def apply_all(manager):
    """Apply all rules in right sequence"""
    add_english(manager)
    init_meta_wishes(manager)
    assign_friends(manager)
    assign_wishes(manager)
    manager.assign_all()
    print(get_wishes_count(manager), file=sys.stderr)
