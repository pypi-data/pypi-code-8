from setuptools import setup

version = '0.0.1'
name = 'myopenopt'
short_description = '`myopenopt` is a package for myopenopt.'
long_description = """\
`myopenopt` is a package for myopenopt.
::

    from myopenopt import *
    model = Model("sample", mtype='NLP')
    x1 = model.addVar(vtype="C", name="x1")
    x2 = model.addVar(vtype="C", name="x2")
    x3 = model.addVar(vtype="C", ub=10, name="x3")
    model.update()
    c1 = model.addConstr(x1**2 + 2*x2**2 <= x3**2, name="C1")
    c2 = model.addConstr(x3 <= 30, name="C2")
    c3 = model.addConstr(quicksum([x1, x2, x3]) <= 20, name="C3" )    
    model.setObjective(15*x1 + 18*x2 + 30*x3, GRB.MAXIMIZE)
    print(model)
    model.optimize(solver="ralg")
    print("Result =", model.Status)
    for v in model.getVars():
        print(v.VarName, v.X)

Requirements
------------
* Python 2 or Python 3 and openopt, FuncDesigner

Features
--------
* nothing

Setup
-----
::

   Add compiler path(ex. C:\Anaconda3\MinGW\bin)
   $ pip install openopt
   $ pip install FuncDesigner
   $ pip install myopenopt

History
-------
0.0.1 (2015-5-4)
~~~~~~~~~~~~~~~~~~
* first release

"""

classifiers = [
   "Development Status :: 1 - Planning",
   "License :: OSI Approved :: Python Software Foundation License",
   "Programming Language :: Python",
   "Topic :: Software Development",
]

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    py_modules=['myopenopt'],
    keywords=['myopenopt',],
    author='Mikio Kubo',
    author_email='kubomikio@gmail.com',
    url='https://pypi.python.org/pypi/myopenopt',
    install_requires=[
          'openopt',
          'FuncDesigner',
    ],
    license='PSFL',
)