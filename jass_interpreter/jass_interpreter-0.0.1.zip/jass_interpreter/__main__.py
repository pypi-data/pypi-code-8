# * coding:utf-8 *
import sys
import re

from parsimonious import Grammar
from docopt import docopt

from jass_interpreter.jass_parser import JassParser
from jass_interpreter.python_generator import JassToPyTransformer

VERSION = "0.0.2"

__author__ = 'Joonas'

def remove_excess_empty_lines(src):
    # return src
    # remove empty lines
    src = re.sub(pattern="\s+\n", repl="\n", string=src)

    # insert newlines after larger blocks (function definitions, loop atm)
    src = re.sub(pattern="pass\n", repl="pass\n\n", string=src)

    return src

def main(options):
    files = options["<files>"]
    parser = JassParser()
    transformer = JassToPyTransformer()
    for fn in files:
        with open(fn) as jassfile:
            data = jassfile.read()
            ast = parser.parse(data)
        with open(fn + ".py", "w") as pyfile:
            src = transformer.visit(ast)
            # print(src)
            pyfile.write(remove_excess_empty_lines(src))





if __name__ == "__main__":
    docs = '''
        Usage:
            jass_interpreter [--debug] <files>...

        Options:
            -d, --debug    Emit debug statements


    '''
    options = docopt(docs, sys.argv[1:], version=VERSION)
    main(options)
