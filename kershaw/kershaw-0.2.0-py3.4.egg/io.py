import os
from kershaw.lang import filter_empty


def file_lines(file_path, start=1, end=None, length=None, include_empty=True):
    """
    Retrieve all or a slice of a file's contents, returned as a list of lines with newlines removed.

    :param file_path: The path to the file to be read from.
    :type file_path: str
    :param start: The number of lines into the file to start slicing from.
    :type start: int
    :param end: The number of lines into the file to stop slicing. Mutually exclusive with 'length'.
    :type end: int
    :param length: The number of lines to slice from the file. Mutually exclusive with 'end'.
    :type length: int
    :param include_empty: A flag indicating that empty lines from the file should be included in
        the returned list. Setting false is useful for reading things like config files or logs.
    :type include_empty: bool
    :return: The slice of the file defined by the given parameters.
    :rtype: list
    """
    assert start > 0, "start_line must be greater than 0"
    assert None in (end, length), "can't specify both end_line and length"
    assert end is None or end > start,\
        "end_line must be greater than start_line (value is one-indexed)"
    lines = [line.strip() for line in open(file_path, 'r').readlines()]
    start -= 1
    if length is not None:
        end = start + length + 1
    if end is not None and end < len(lines):
        end -= 1
        lines = lines[:end]
    if start > 0:
        lines = lines[start:]
    return lines if include_empty else filter_empty(lines)


def head(file_path, length=1, short_circuit_singles=True, include_empty=True):
    """
    Retrieve the number of lines specified by `length` (defaults to a single line) from the
    beginning of the given file.

    :param file_path: The path to the file to be read from.
    :type file_path: str
    :param length: The number of lines to read from the file.
    :type length: int
    :param short_circuit_singles: A flag indicating that the method should the requested line as a
        string instead of list when 'length' is 1.
    :type short_circuit_singles: bool
    :return: If 'length' is 1 and 'short_circuit_singles' (which are both the default values) the
        contents of the first line as a string. Otherwise, a list containing the number of
        lines requested.
    :rtype: list|str
    """
    lines = file_lines(file_path, length=length, include_empty=include_empty)
    return lines[0] if (short_circuit_singles and length == 1) else lines


def tail(file_path, length=1, short_circuit_singles=True, include_empty=True):
    """
    Retrieve the number of lines specified by `length` (defaults to a single line) from the end of
    the given file.

    :param file_path: The path to the file to be read from.
    :type file_path: str
    :param length: The number of lines to read from the file.
    :type length: int
    :param short_circuit_singles: A flag indicating that the method should the requested line as a
        string instead of list when 'length' is 1.
    :type short_circuit_singles: bool
    :return: If 'length' is 1 and 'short_circuit_singles' (which are both the default values) the
        contents of the final line as a string. Otherwise, a list containing the number of
        lines requested.
    :rtype: list|str
    """
    lines = file_lines(file_path, include_empty=include_empty)[-length:]
    return lines[0] if (short_circuit_singles and length == 1) else lines


def touch(file_path, cwd=os.getcwd(), retain_fp=False):
    """
    Create a file at the specified path if it does not exist. Update the modification timestamp
    if it does exit.

    :param file_path: The path to the file to be touched.
    :type file_path: str
    :param retain_fp: A flag indicating that the file pointer for the new file should be
        returned, instead of void/None.
    :type retain_fp: bool
    :return: The file's pointer if retain_fp is True, else None/void.
    :rtype: file|None
    """
    if cwd is not None and file_path[0] != '/':
        file_path = os.path.join(cwd, file_path)
    destination_dir = os.path.dirname(file_path)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    file_fp = open(file_path, 'a')
    try:
        os.utime(file_path, None)
        return file_fp
    except:
        retain_fp = False
        raise
    finally:
        if not retain_fp:
            file_fp.close()