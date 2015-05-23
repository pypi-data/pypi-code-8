# -*- coding: utf-8 -*-
u"""
    pylatex.document
    ~~~~~~~

    This module implements the class that deals with the full document.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from __future__ import absolute_import
import os
import subprocess
import errno
from .package import Package
from .command import Command
from .utils import dumps_list, rm_temp_dir
from .base_classes import BaseLaTeXContainer


class Document(BaseLaTeXContainer):

    u"""
    A class that contains a full LaTeX document. If needed, you can append
    stuff to the preamble or the packages.
    """

    def __init__(self, default_filepath=u'default_filepath',
                 documentclass=u'article', fontenc=u'T1', inputenc=u'utf8',
                 author=u'', title=u'', date=u'', data=None, maketitle=False):
        u"""
            :param default_filepath: the default path to save files
            :param documentclass: the LaTeX class of the document
            :param fontenc: the option for the fontenc package
            :param inputenc: the option for the inputenc package
            :param author: the author of the document
            :param title: the title of the document
            :param date: the date of the document
            :param data:
            :param maketitle: whether `\maketitle` command is activated or not.

            :type default_filepath: str
            :type documentclass: str or :class:`command.Command` instance
            :type fontenc: str
            :type inputenc: str
            :type author: str
            :type title: str
            :type date: str
            :type data: list
            :type maketitle: bool
        """

        self.default_filepath = default_filepath
        self.maketitle = maketitle

        if isinstance(documentclass, Command):
            self.documentclass = documentclass
        else:
            self.documentclass = Command(u'documentclass',
                                         arguments=documentclass)

        fontenc = Package(u'fontenc', options=fontenc)
        inputenc = Package(u'inputenc', options=inputenc)
        lmodern = Package(u'lmodern')
        packages = [fontenc, inputenc, lmodern]

        self.preamble = []

        self.preamble.append(Command(u'title', title))
        self.preamble.append(Command(u'author', author))
        self.preamble.append(Command(u'date', date))

        super(Document, self).__init__(data, packages=packages)

    def dumps(self):
        u"""Represents the document as a string in LaTeX syntax.

            :return:
            :rtype: str
        """

        document = ur'\begin{document}' + os.linesep

        if self.maketitle:
            document += ur'\maketitle' + os.linesep

        document += super(Document, self).dumps() + os.linesep

        document += ur'\end{document}' + os.linesep

        head = self.documentclass.dumps() + os.linesep
        head += self.dumps_packages() + os.linesep
        head += dumps_list(self.preamble) + os.linesep

        return head + os.linesep + document

    def generate_tex(self, filepath=u''):
        super(Document, self).generate_tex(self.select_filepath(filepath))

    def generate_pdf(self, filepath=u'', clean=True, compiler=u'pdflatex'):
        u"""Generates a .pdf file.

            :param filepath: the name of the file
            :param clean: whether non-pdf files created by `pdflatex` must be
            removed or not

            :type filepath: str
            :type clean: bool
        """

        filepath = self.select_filepath(filepath)
        filepath = os.path.join(u'.', filepath)

        cur_dir = os.getcwdu()
        dest_dir = os.path.dirname(filepath)
        basename = os.path.basename(filepath)
        os.chdir(dest_dir)

        self.generate_tex(basename)

        command = compiler + u' --jobname="' + basename + u'" "' + \
            basename + u'.tex"'

        subprocess.check_call(command, shell=True)

        if clean:
            for ext in [u'aux', u'log', u'out', u'tex']:
                try:
                    os.remove(basename + u'.' + ext)
                except (OSError, IOError), e:
                    # Use FileNotFoundError when python 2 is dropped
                    if e.errno != errno.ENOENT:
                        raise

            rm_temp_dir()
        os.chdir(cur_dir)

    def select_filepath(self, filepath):
        u"""Makes a choice between `filepath` and `self.default_filepath`.

            :param filepath: the filepath to be compared with
            `self.default_filepath`

            :type filepath: str

            :return: The selected filepath
            :rtype: str
        """

        if filepath == u'':
            return self.default_filepath
        else:
            return filepath
