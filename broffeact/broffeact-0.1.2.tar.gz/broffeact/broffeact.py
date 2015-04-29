#!/usr/bin/python3
import datetime as dt
import os
import re
import argparse
from jinja2 import Template


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Status:
    NOT_STARTED, PARSING, DONE = range(3)


def printWarning(msg):
    print(bcolors.WARNING + "WARNING:" + bcolors.ENDC, msg)


def printFAIL(msg):
    print(bcolors.FAIL + "FAIL:" + bcolors.ENDC, msg)


def printOK(word, msg):
    print(bcolors.OKBLUE + word + bcolors.ENDC, msg)

# --------------------------------


class AgDoc:
    """Documentation generator for agflow."""
    defaults = {
        'template_filename': 'default',
        'prefix_module': 'M',
        'prefix_comment': '#',
        'prefix_export': 'exp',
        'file_output': 'doc.html',
        'extensions': ['coffee'],
        'directories': ['.'],
        'component_terms': ['createFactory'],
        'proptypes_term': 'React.PropTypes',
    }
    STATS = {
        "nbr_exported": 0,
        "nbr_commented": 0,
        "nbr_modules_unused": 0,
    }

    def __init__(self, defaults):
        self.defaults.update(defaults)
        self.init_output_dir()

    def init_output_dir(self):
        dir = os.path.dirname(self.defaults["file_output"])
        if not os.path.exists(dir) and dir != "":
            os.makedirs(dir)

    def genDoc(self):
        self.writeHTMLDoc(self.walk())

    def isValidExtension(self, name):
        """Check if a file has a valid extension to parse"""
        file_ext = os.path.splitext(name)[1]
        return file_ext and file_ext[1:] in self.defaults["extensions"]

    def walk(self):
        """A little promenade into the application returning
        the comments into a list of dict"""
        print("SCANNING IN:", self.defaults["directories"])
        a, d, j = os.path.abspath, os.path.dirname, os.path.join
        main_root_len = len(a((d(d(d(os.path.realpath(__file__)))))))

        values = []
        for dirname in self.defaults["directories"]:
            for root, dirs, files in os.walk(dirname, topdown=True):
                files = sorted(f for f in files if self.isValidExtension(f))
                for name in files:
                    parsed = self.parse(a(j(root, name)), main_root_len)
                    if len(parsed[1])+len(parsed[2])+len(parsed[3]) > 0:
                        values.append(parsed)
        return values

    def parse(self, file_name, strip_len):
        """Parse the file"""
        printOK("PARSING:", file_name)
        p_module = self.defaults['prefix_module']
        with open(file_name, 'r') as f:
            comments_dic = {}
            prev_lines, modules, used_modules = [], set(), set()
            status = Status.NOT_STARTED
            for line in f:
                line = line.strip()

                if status == Status.NOT_STARTED:
                    if line.lstrip().startswith(p_module):
                        status = Status.PARSING
                elif status == Status.PARSING:
                    module, sep, rest = line.partition(':')
                    if sep == ':':
                        modules.add(module)
                    else:
                        status = Status.DONE
                else:
                    used_modules |= set(
                        re.findall(
                            r'\b{}\.([\w\d_]+)\b'.format(p_module),
                            line
                        )
                    )

                    # Export part
                    if self.isExportedLine(line):
                        exported_name = self.getExportedName(line)
                        printOK("FOUND EXPORTED: ", exported_name)
                        self.STATS["nbr_exported"] += 1
                        comment = self.getComment(line, prev_lines)
                        comments_dic[exported_name] = comment
                        if comment[2]:
                            self.STATS["nbr_commented"] += 1
                        else:
                            printWarning("'{}' not commented in {}".format(
                                exported_name, file_name
                            ))
                prev_lines.append(line)

        # Check for unused module
        unused_modules = modules - used_modules
        for unused in unused_modules:
            self.STATS["nbr_modules_unused"] += 1
            printWarning("Unused module: '" + unused + "'")

        return (
            file_name[strip_len:].lstrip('/'), modules,
            unused_modules, comments_dic
        )

    def getComment(self, line, prev_lines):
        """Get the comment(s) from prevLines of a component"""

        isComponent = any(
            term in line
            for term in self.defaults['component_terms']
        )

        if isComponent:
            com, isCommented = self.getCompComments(line, prev_lines)
            comment = ("c", com, isCommented)
        else:
            com, isCommented = self.getFuncComments(line, prev_lines)
            comment = ("f", com, isCommented)
        return comment

    def getCompComments(self, line, prev_lines):
        comments, ignore_lines, propTypes = '', True, []
        for prev_line in reversed(prev_lines):
            comment = prev_line
            if ignore_lines:
                if self.defaults["proptypes_term"] in comment:
                    propTypes.append(
                        comment.replace(
                            self.defaults["proptypes_term"] + ".", ""
                        ).replace(".isRequired", " (required)")
                    )
                ignore_lines = 'createClass' not in comment
                continue

            if not comment.startswith(self.defaults["prefix_comment"]):
                break
            comments = comment + '\n' + comments

        if propTypes and comments:
            comments = (
                "PropTypes:\n-" +
                "\n-".join(propTypes) +
                "\n" + comments
            )
        return comments, comments != ""

    def getFuncComments(self, line, prev_lines):
        comments = ''
        for prev_line in reversed(prev_lines):
            if not prev_line.startswith(self.defaults["prefix_comment"]):
                break
            comments = prev_line + '\n' + comments

        # Adding args if there is a comment
        if comments:
            m = re.search(r'\((.*)\)', line)
            if m:
                comments = "ARGS: {}\n".format(m.group(1)) + comments

        return comments, comments != ""

    def isExportedLine(self, line):
        """Check if the line contains the exportPrefix"""
        return line.startswith(self.defaults["prefix_export"] + ".")

    def getExportedName(self, line):
        export, sep, rest = line.partition('=')
        assert sep == '=', 'Should be "=" found "{}"'.format(sep)
        prefix_export, sep, export = export.partition('.')
        assert sep == '.', 'Should be "." found "{}"'.format(sep)
        assert prefix_export.strip() == self.defaults['prefix_export'],\
            'Should be {} found {}'.format(
                self.defaults['prefix_export'], prefix_export
            )
        return export

    def writeHTMLDoc(self, values):
        """ values=(file_name, modules, modules_unused, comments_dic)"""
        tpl_filename = os.path.dirname(os.path.realpath(__file__)) + \
            "/templates/"+self.defaults["template_filename"]+".html"
        try:
            t = Template(open(tpl_filename, 'r').read())
        except:
            printFAIL("Couldn't open template: " +
                      self.defaults["template_filename"])
            return
        params = {
            'values': values,
            'exported_cnt': self.STATS['nbr_exported'],
            'commented_cnt': self.STATS['nbr_commented'],
            'unused_cnt': self.STATS['nbr_modules_unused'],
            'commented_percentage': (
                0 if self.STATS['nbr_exported'] == 0 else
                self.STATS['nbr_commented'] * 100 / self.STATS['nbr_exported']
            ),
            'last_modification': dt.datetime.strftime(
                dt.datetime.utcnow(), '%A, %d %B %Y %H:%M:%S'
            )
        }
        f = open(self.defaults['file_output'], 'w')
        f.write(t.render(**params))
        f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity")
    parser.add_argument("-o", "--output",
                        help="output filename", default="doc/index.html")
    parser.add_argument("-i", "--input", default="app/",
                        help="input directories (eg: app/,extra/")
    parser.add_argument("-t", "--template", default="default",
                        help="HTML template file (eg: default)")
    args = parser.parse_args()

    options = {}

    options["file_output"] = args.output
    options["directories"] = args.input.split(",")
    options["template_filename"] = args.template
    AgDoc(options).genDoc()
