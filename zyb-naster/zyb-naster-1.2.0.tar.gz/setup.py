from distutils.core import setup#导入setup函数
setup(
    #setup函数的参数
    name='zyb-naster',               #发布的名字
    version='1.2.0',                 #版本
    py_modules=['print_list'],       #模块的元数据(模块的名字)
    author='zyb',                    #作者
    author_email='yabeizhao@126.com',#作者邮箱
    url='www.baidu.com',             #网站
    description='输出列表',       #介绍
      )