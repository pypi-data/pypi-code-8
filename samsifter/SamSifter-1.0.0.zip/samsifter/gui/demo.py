#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Demo of custom widgets for filter items and parameters.

.. moduleauthor:: Florian Aldehoff <samsifter@biohazardous.de>
"""
import sys

from PyQt4.QtGui import QMainWindow, QApplication

from samsifter.models.filter import FilterItem
from samsifter.models.parameter import (
    FilterParameter, FilterFilepath, FilterSwitch, FilterThreshold)


def main():
    """Demo of parameter widgets for SamSifter GUI."""
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    fil = FilterItem(
        text="Filter",
        desc="Description of a filter."
    )
    fil.add_parameter(FilterParameter(
        text="Parameter",
        desc="Description of a parameter.",
        cli_name="-p",
        default=True
    ))
    fil.add_parameter(FilterThreshold(
        text="Threshold",
        desc="Description of a threshold.",
        cli_name="-t"
    ))
    fil.add_parameter(FilterSwitch(
        text="Switch",
        desc="Description of a switch.",
        cli_name="-s",
        default=2,
        options=("True", "False", "Whatever")
    ))
    fil.add_parameter(FilterFilepath(
        text="Filepath",
        desc="Description of a filepath.",
        cli_name="-f",
        default="example.csv"
    ))

    main_window.setCentralWidget(fil.make_widget())
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
