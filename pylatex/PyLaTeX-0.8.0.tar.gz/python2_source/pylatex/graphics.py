# -*- coding: utf-8 -*-
u"""
    pylatex.graphics
    ~~~~~~~~~~~~~~~~

    This module implements the class that deals with graphics.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from __future__ import absolute_import
import os.path

from .utils import fix_filename, make_temp_dir
from .base_classes import BaseLaTeXNamedContainer
from .package import Package
from .command import Command
import uuid


class Figure(BaseLaTeXNamedContainer):

    u"""A class that represents a Graphic."""

    def __init__(self, data=None, position=None, seperate_paragraph=True):
        u"""
        :param data:
        :param position:

        :type data: list
        :type position: str
        :param data:
        :param position:
        :param seperate_paragraph:

        :type data: list
        :type position: str
        :type seperate_paragraph: bool
        """

        packages = [Package(u'graphicx')]
        super(Figure, self).__init__(data=data, packages=packages,
                         options=position,
                         seperate_paragraph=seperate_paragraph)

    def add_image(self, filename, width=ur'0.8\textwidth',
                  placement=ur'\centering'):
        u"""Adds an image.

        :param filename:
        :param width:
        :param placement:

        :type filename: str
        :type width: str
        :type placement: str
        """

        if placement is not None:
            self.append(placement)

        if width is not None:
            width = u'width=' + unicode(width)

        self.append(Command(u'includegraphics', options=width,
                            arguments=fix_filename(filename)))

    def add_caption(self, caption):
        u"""Adds a caption to the figure.

        :param caption:
        :type caption: str
        """

        self.append(Command(u'caption', caption))


class SubFigure(BaseLaTeXNamedContainer):

    u"""A Class that represents a subfigure from the subcaption package"""

    def __init__(self, data=None, position=None,
                 width=ur'0.45\linewidth', seperate_paragraph=False):
        u"""
        :param data:
        :param position:

        :type data: list
        :type position: str
        :param data:
        :param position:
        :param seperate_paragraph:

        :type data: list
        :type position: str
        :type seperate_paragraph: bool
        """

        packages = [Package(u'subcaption')]

        super(SubFigure, self).__init__(data=data, packages=packages,
                         options=position,
                         argument=width,
                         seperate_paragraph=seperate_paragraph)

    def add_image(self, filename, width=ur'\linewidth',
                  placement=None):
        u"""Adds an image.

        :param filename:
        :param width:
        :param placement:

        :type filename: str
        :type width: str
        :type placement: str
        """

        if placement is not None:
            self.append(placement)
        if width is not None:
            width = u'width=' + unicode(width)

        self.append(Command(u'includegraphics', options=width,
                            arguments=fix_filename(filename)))

    def add_caption(self, caption):
        u"""Adds a caption to the figure

        :param caption:
        :type caption: str
        """

        self.append(Command(u'caption', caption))


class Plt(Figure):
    u"""A class that represents a plot created with matplotlib."""

    container_name = u'figure'

    def __init__(self, **kwargs):
        super(Plt, self).__init__(**kwargs)

    def _save_plot(self, plt, *args, **kwargs):
        u"""Saves the plot.

        :param plt: matplotlib.pyplot
        :type plt: module

        :return: The basename with which the plot has been saved.
        :rtype: str
        """

        tmp_path = make_temp_dir()

        filename = os.path.join(tmp_path, unicode(uuid.uuid4()) + u'.pdf')

        plt.savefig(filename, *args, **kwargs)

        return filename

    def add_plot(self, plt, width=ur'0.8\textwidth',
                 placement=ur'\centering', *args, **kwargs):
        u"""Adds a plot.

        :param plt: matplotlib.pyplot
        :param width: The width of the plot.
        :param placement: The placement of the plot.

        :type plt: module
        :type width: str
        :type placement: str
        """

        filename = self._save_plot(plt, *args, **kwargs)

        self.add_image(filename, width, placement)
