#coding=utf-8
#
__author__ = 'Maple'

import commands
import os

from {{ project_name }}.settings import *

def run():
    project_root = BASE_DIR #manage.py所在目录
    #检查数据库结构
    def check_db_schema():
        print u"**检查数据库结构**"
        base_cmd = 'python %s dbdiff ' % os.path.join(project_root, 'manage.py')
        apps = INSTALLED_APPS
        for app in apps:
            if app.startswith('django.'):
                continue
            print u'    /* App:%s */' % app
            cmd = base_cmd + app
            output = commands.getoutput(cmd)
            if 'no models founds' in output or \
               'missing a models.py' in output:
                app_model_check_rs = '/* -- No differences */'
            else:
                app_model_check_rs = output
            for line in app_model_check_rs.splitlines():
                print '        %s' % line
            if 'Table missing' in app_model_check_rs:
                print '\033[1;32;47m',
                print '    Please run: python manage.py syncdb',
                print  '\33[0m'
    check_db_schema()
    print
    # def check_cronds_install():
    #     print u"""**检查定时任务安装(检查根目录和app目录里的cronds目录)**"""
    # check_cronds_install()
