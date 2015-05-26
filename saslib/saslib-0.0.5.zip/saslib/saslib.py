from __future__ import print_function
from jinja2 import Template
from sas7bdat import SAS7BDAT
from collections import OrderedDict
import os
import math
import tempfile
import webbrowser
from ext import template_string, convertSize

class PROCcontents:
    def __init__(self, directory):
        self.sas_files = sorted([x for x in os.listdir(directory) \
            if x.endswith('sas7bdat')])
        if not self.sas_files:
            raise IOError('no sas7bdat files are available')
        if len(set(self.sas_files)) != len(self.sas_files):
            raise IOError('the sas7bdat files may have the same names')
        self.template = Template(template_string)
        self.directory = directory
        self.data = self.read_data()
        self.temp_dir = tempfile.mkdtemp()

    def read_data(self):
        """Use the package sas7bdata to read the meta information from every
        sas file under the specified directory
        """
        data = OrderedDict()
        for x in self.sas_files:
            current_sas_name = x.replace('.sas7bdat', '')
            current_file = self.directory + '/' + x
            current = SAS7BDAT(current_file)
            statinfo = os.stat(current_file)
            meta = [['Position', 'Name', 'Type', 'Length', 'Format', 'Label']]
            for i, col in enumerate(current.header.parent.columns, 1):
                meta.append([i, col.name, col.type, col.length, col.format, col.label])
            _detail = current.header.properties.__dict__
            blacklist = ['col_count_p1', 'col_count_p2', 'lcp', 'lcs', \
                'filename', 'endianess', 'u64']
            detail = OrderedDict()
            for k in sorted(_detail):
                if k in blacklist:
                    continue
                v = _detail[k]
                if isinstance(v, str):
                    v = v.lower()
                detail[k.upper()] = v
            detail['FILE_SIZE'] = convertSize(statinfo.st_size)
            data[current_sas_name] = {'meta': meta, 'detail': detail}
            current.close()
        return data

    def write_html(self):
        """Use the jinja2 template to write the report"""
        outfile = os.path.join(self.temp_dir, 'contents.html')
        f = open(outfile, 'w')
        print(self.template.render(data = self.data, directory = \
            self.directory), file = f)
        return outfile

    def show(self):
        webbrowser.open_new(self.write_html())


