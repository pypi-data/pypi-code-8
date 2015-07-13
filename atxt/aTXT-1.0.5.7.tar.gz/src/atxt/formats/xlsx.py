#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-13 02:41:06
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-13 02:50:51
import xlrd
import os

from _utils import save_raw_data


def xlsx(from_file, to_txt, opts):
    filename = from_file.path
    workbook = xlrd.open_workbook(filename)
    sheets_name = workbook.sheet_names()
    output = os.linesep
    for names in sheets_name:
        worksheet = workbook.sheet_by_name(names)
        num_rows = worksheet.nrows
        num_cells = worksheet.ncols

        for curr_row in range(num_rows):
            row = worksheet.row(curr_row)
            new_output = []
            for index_col in xrange(num_cells):
                value = worksheet.cell_value(curr_row, index_col)
                if value:
                    if isinstance(value, (int, float)):
                        value = unicode(value)
                    new_output.append(value)
            if new_output:
                output += u' '.join(new_output) + unicode(os.linesep)

    return save_raw_data(to_txt.path, output)
