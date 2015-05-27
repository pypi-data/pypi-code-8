#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from xlrd import open_workbook
from xlrd.xldate import xldate_as_datetime
from xlrd.sheet import ctype_text
import codecs

def excel2sql(file_name=None, first_line_header=True, output_dir=None):
    output_dir = output_dir or './'
    try:
        wb = open_workbook(file_name)
        _sheet_all = []
        for i in range(len(wb.sheets())):
            _sheet = wb.sheet_by_index(i)
            _sv = {'_sheet_name': _sheet.name, '_sheet_list': []}
            for _r in xrange(_sheet.nrows):
                _rv = []
                for _c in xrange(_sheet.ncols):
                    _cell, _cell_type, _v, _vstr = _sheet.cell(_r, _c), _sheet.cell(_r, _c).ctype, _sheet.cell(_r, _c).value, repr(_sheet.cell(_r, _c).value)
                    _vunicode = None
                    if ('number' == ctype_text[_cell_type]) and (len(_vstr.split('.')) == 2) and (int(_vstr.split('.')[1]) == 0):
                        _vunicode = unicode(_vstr.split('.')[0])
                    elif ('xldate' == ctype_text[_cell_type]):
                        _date = xldate_as_datetime(_v, wb.datemode)  
                        _vunicode = unicode(str(_date))
                    else:
                        _vunicode = _v
                    _rv.append(_vunicode)

                _sv['_sheet_list'].append(_rv)
            _sheet_all.append(_sv)
        
        for s in _sheet_all:
            _sheet_name = s['_sheet_name']
            _sheet_list = s['_sheet_list']
            _cols = (first_line_header and _sheet_list[0]) or []
            _sql_file = output_dir+_sheet_name+'.sql'
            # ((_cols[j] and ' as ' + _cols[j]) or '')
            with codecs.open(filename=_sql_file, mode='w', encoding='utf-8', errors='strict', buffering=1024) as f:
                idx = (first_line_header and 1) or 0
                for k in range(len(_sheet_list)):
                    if k < idx: continue
                    r = _sheet_list[k]
                    write_str = ""
                    if k == idx and _cols and len(_cols) > 0:
                        write_str = 'select ' + ','.join([('\''+(r[j].replace('\'', '\"'))+'\'') + ' as ' + _cols[j] for j in range(len(r))]) + ' from dual '
                    else:
                        write_str = 'select ' + ','.join([('\''+(r[j].replace('\'', '\"'))+'\'') for j in range(len(r))]) + ' from dual '
                    f.write(write_str)
                    if (k == len(_sheet_list) - 1):
                        f.write(' \n')
                    else:
                        f.write(' union all \n')
                f.flush()
            
        pass
    except Exception as e:
        print u"读取文件错误: ", file_name
        print e
    finally:
        pass

if __name__ == "__main__":
    excel2sql(file_name=ur"C:/Users/XES/Desktop/缴费信息统计表-全国汇总.xls", first_line_header=True, output_dir=None)
    pass
