from __future__ import print_function
from jinja2 import Template, Environment, PackageLoader
from sas7bdat import SAS7BDAT
from collections import OrderedDict
import os
import math
import tempfile
import webbrowser
import imp

class PROCcontents:
    def __init__(self, directory):
        env = Environment(loader = PackageLoader('saslib', 'ext'))
        self.template = env.get_template('sastemplate.html')
        self.sas_files = sorted([x for x in os.listdir(directory) \
            if x.endswith('sas7bdat')])
        if not self.sas_files:
            raise IOError('no sas7bdat files are available')
        if len(set(self.sas_files)) != len(self.sas_files):
            raise IOError('the sas7bdat files may have the same names')
        self.directory = directory
        self.data = self.read_data()
        self.temp_dir = tempfile.mkdtemp()
        self.path = imp.find_module('saslib')[1]
        
    def convert_size(self, size):
        size /= 1024
        size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size, 1024)))
        p = math.pow(1024,i)
        s = round(size / p, 2)
        if (s > 0):
           return '%s %s' % (s, size_name[i])
        return '0B'

    def to_unicode(self, s):
        if isinstance(s, str):
            try:
                return s.decode('utf-8')
            except UnicodeDecodeError:
                return unicode(s, errors = 'ignore')
        return s

    def read_data(self):
        """Use the package sas7bdata to read the meta information from every
        sas file under the specified directory
        """
        data = OrderedDict()
        for x in self.sas_files:
            current_sas_name = x.replace('.sas7bdat', '')
            current_file = os.path.join(self.directory, x)
            current = SAS7BDAT(current_file)
            statinfo = os.stat(current_file)
            meta = [['Position', 'Name', 'Type', 'Length', 'Format', 'Label']]
            for i, col in enumerate(current.header.parent.columns, 1):
                _metaline = [i] + map(self.to_unicode, [col.name, col.type, \
                    col.length, col.format, col.label])
                meta.append(_metaline)
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
            detail['FILE_SIZE'] = self.convert_size(statinfo.st_size)
            data[current_sas_name] = {'meta': meta, 'detail': detail}
            current.close()
        return data

    def write_html(self):
        """Use the jinja2 template to write the report"""
        
        outfile = os.path.join(self.temp_dir, 'contents.html')
        f = open(outfile, 'w')
        print(self.template.render(data = self.data, directory = \
            self.directory, path = os.path.join(self.path, 'ext'))\
                .encode('utf-8'), file = f)
        return outfile

    def show(self):
        webbrowser.open_new(self.write_html())


