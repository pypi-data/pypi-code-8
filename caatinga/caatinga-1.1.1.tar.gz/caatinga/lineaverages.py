#!/usr/bin/env python

# List of file extensions of files to be aggregated
FILE_EXTENSIONS = [".py"]

# Path/Files beginning with items in this list will not be counted
IGNORE_STARTS_WITH = ["./tests"]

# Files ending with items in this list will not be counted
IGNORE_ENDS_WITH = [".pyc"]

# Lines that should not be counted
IGNORE_LINES = ['"""']

# String that represents a comment
COMMENT = "#"


import os
from os.path import join
from itertools import groupby


def main():
    allProjectFiles = list(fileList("."))
    endsWithFiltered = filterEndsWith(allProjectFiles, IGNORE_ENDS_WITH)
    startsWithFiltered = filterStartsWith(endsWithFiltered, IGNORE_STARTS_WITH)
    filesToTotal = getFilesWithExtensions(startsWithFiltered, FILE_EXTENSIONS)
    totals = list(map(_createFileTotal, filesToTotal))

    if len(FILE_EXTENSIONS) > 1:
        _showTotalsPerExtension(totals)

    print("Project Totals")
    print("========================")
    print("Files in project: {0}".format(len(allProjectFiles)))
    print("Files aggregated: {0}".format(len(totals)))
    _showAggregateTotals(totals)


def fileList(directory):
    for items in os.walk(directory):
        for file_ in items[2]:
            yield join(items[0], file_)


def filterEndsWith(items, ignoreList):
    comparefn = lambda item, ignore: item.endswith(ignore)
    return _ignoredItemsRemoved(items, ignoreList, comparefn)


def filterStartsWith(items, ignoreList):
    comparefn = lambda item, ignore: item.startswith(ignore)
    return _ignoredItemsRemoved(items, ignoreList, comparefn)


def getFilesWithExtensions(items, extensionList):
    comparefn = lambda item, extension: item.endswith(extension)
    return (item for item in items
            if _isItemFoundInList(item, extensionList, comparefn))


def _ignoredItemsRemoved(items, ignoreList, comparefn):
    return (item for item in items
            if not _isItemFoundInList(item, ignoreList, comparefn))


def _isItemFoundInList(item, itemList, comparefn):
    return any(comparefn(item, listItem) for listItem in itemList)


def _createFileTotal(file_):
    return FileTotals(file_, IGNORE_LINES, COMMENT)


class FileTotals:
    def __init__(self, fileName, ignoreLines, comment):
        self.fileName = fileName
        self._ignoreLines = ignoreLines
        self._comment = comment
        self.lineCount = 0
        self.maxColumnWidth = 0
        self.minColumnWidth = 0
        self.totalColumnWidth = 0
        self._updateTotals()

    def _updateTotals(self):
        with open(self.fileName, 'r') as f:
            for line in f:
                if self._isIgnoredLine(line):
                    self.lineCount += 1
                    self.totalColumnWidth += len(line.rstrip())
                    self._updateMaxColumnWidth(line)
                    self._updateMinColumnWidth(line)

    def _isIgnoredLine(self, line):
        strippedLine = line.strip()
        return (strippedLine not in self._ignoreLines and
                not strippedLine.startswith(self._comment))

    def _updateMaxColumnWidth(self, line):
        self.maxColumnWidth = max(self.maxColumnWidth, len(line))

    def _updateMinColumnWidth(self, line):
        self.minColumnWidth = (
            len(line) if self.minColumnWidth == 0
            else min(self.minColumnWidth, len(line)))


def _showTotalsPerExtension(totals):
    fileExtension = lambda f: f.fileName[f.fileName.rfind("."):]
    data = sorted(totals, key=fileExtension)
    groups = groupby(data, fileExtension)
    for key, groupTotals in groups:
        group = list(groupTotals)
        print("Totals by file extension")
        print("========================")
        print("Totals for {0} files".format(key))
        _showAggregateTotals(group)
        print()


def _showAggregateTotals(totals):
    totalLines = sum(total.lineCount for total in totals)
    totalColumnWidth = sum(total.totalColumnWidth for total in totals)
    largestLineCount = max(total.lineCount for total in totals)
    smallestLineCount = min(total.lineCount for total in totals)
    averageLineCount = int(totalLines / len(totals))
    largestColumn = max(total.maxColumnWidth for total in totals)
    smallestColumn = min(total.minColumnWidth for total in totals)
    averageColumn = int(totalColumnWidth / totalLines)

    print("Largest line count: {0}".format(largestLineCount))
    print("Smallest line count: {0}".format(smallestLineCount))
    print("Average line count: {0}".format(averageLineCount))
    print("Largest column: {0}".format(largestColumn))
    print("Smallest column: {0}".format(smallestColumn))
    print("Average column width: {0}".format(averageColumn))
    print("Total lines: {0}".format(totalLines))


if __name__ == "__main__":
    main()
