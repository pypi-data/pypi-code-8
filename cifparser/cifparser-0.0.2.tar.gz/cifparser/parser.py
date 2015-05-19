# Copyright 2015 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of cifparser.  cifparser is BSD-licensed software;
# for copyright information see the LICENSE file.

from cifparser.path import Path
from cifparser.valuetree import ValueTree, ROOT_PATH
from cifparser.grammar import *

class Frame(object):
    """
    Base class for all frame types.
    """
    def __init__(self, linenum, indent):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        """
        self.linenum = linenum
        self.indent = indent
    def __repr__(self):
        return str(self)

class ContainerFrame(Frame):
    """
    A Frame which represents a ValueTree container.
    """
    def __init__(self, linenum, indent, path, container):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        :param container:
        :type container: ValueTree
        """
        super().__init__(linenum, indent)
        self.path = path
        self.container = container
    def __str__(self):
        return "ContainerFrame(linenum={0}, indent={1}, path={2})".format(self.linenum,self.indent,self.path)

class ListItemFrame(ContainerFrame):
    """
    A Frame which represents a list item in a container.
    """
    def __init__(self, linenum, indent, path, container):
        """
        """
        super().__init__(linenum, indent, path, container)
    def __str__(self):
        return "ListItemFrame(linenum={0}, indent={1}, path={2})".format(self.linenum,self.indent,self.path)

class RootFrame(ContainerFrame):
    """
    A Frame which represents the root of the parsing stack.
    """
    def __init__(self, root):
        """
        :param root:
        :type root: ValueTree
        """
        super().__init__(None, None, Path([]), root)
    def __str__(self):
        return "RootFrame()"

class FieldFrame(Frame):
    """
    A Frame which represents a field, which is a name,value pair within a container.
    """
    def __init__(self, linenum, indent, path, container, field_name, field_value):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        :param container:
        :type container: ValueTree
        :param field_name:
        :type field_name: str
        :param field_value:
        :type field_value: str
        """
        super().__init__(linenum, indent)
        self.path = path
        self.container = container
        self.field_name = field_name
        self.field_value = field_value
    def __str__(self):
        return "FieldFrame(linenum={0}, indent={1}, path={2}, field_name={3})".format(
            self.linenum,self.indent,self.path,self.field_name)

class ValueContinuationFrame(Frame):
    """
    A Frame which represents the continuation of a field.
    """
    def __init__(self, linenum, indent, path, container, field_name, field_value):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        :param container:
        :type container: ValueTree
        :param field_name:
        :type field_name: str
        :param field_value:
        :type field_value: str
        """
        super().__init__(linenum, indent)
        self.path = path
        self.container = container
        self.field_name = field_name
        self.field_value = field_value
    def __str__(self):
        return "ValueContinuationFrame(linenum={0}, indent={1}, path={2}, field_name={3})".format(
            self.linenum,self.indent,self.path,self.field_name)

class ListContinuationFrame(Frame):
    """
    A Frame which represents the continuation of a field list.
    """
    def __init__(self, linenum, indent, path, container, field_name, list_value):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        :param container:
        :type container: ValueTree
        :param field_name:
        :type field_name: str
        :param list_value:
        :type list_value: str
        """
        super().__init__(linenum, indent)
        self.path = path
        self.container = container
        self.field_name = field_name
        self.list_value = list_value
    def __str__(self):
        return "ListContinuationFrame(linenum={0}, indent={1}, path={2}, field_name={3})".format(
            self.linenum,self.indent,self.path,self.field_name)

class ParserContext(object):
    """
    Manages the stack of frames during parsing.
    """
    def __init__(self, values):
        """
        :param values:
        :type values: ValueTree
        """
        self.values = values
        self.root_frame = RootFrame(values)
        self.frames = [self.root_frame]

    def current_frame(self):
        """
        :returns: The current top of the stack.
        :rtype: Frame
        """
        return self.frames[0]

    def current_indent(self):
        """
        :returns: The current indentation level.
        :rtype: int
        """
        return self.frames[0].indent

    def push_frame(self, frame):
        """
        Insert the specified frame at the top of the stack.

        :param frame:
        :type frame: Frame
        """
        self.frames.insert(0, frame)

    def pop_frame(self):
        """
        Remove and return the frame at the top of the stack.

        :returns: The top frame
        :rtype: Frame
        :raises Exception: If there are no frames on the stack
        """
        self.frames.pop(0)
        if len(self.frames) == 0:
            raise Exception("stack is exhausted")
        return self.frames[0]

    def append_child_object(self, linenum, indent, path):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        """
        frame = self.current_frame()
        assert isinstance(frame,RootFrame) or isinstance(frame,ContainerFrame) and frame.indent < indent
        assert len(path.segments) > 0
        container = frame.container
        if container.contains_container(path):
            raise KeyError("container exists at path {0}".format(path))
        container.put_container(path)
        container = container.get_container(path)
        path = frame.path + path
        frame = ContainerFrame(linenum, indent, path, container)
        self.push_frame(frame)

    def append_sibling_object(self, linenum, indent, path):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        """
        frame = self.current_frame()
        assert frame.indent is not None and frame.indent == indent
        self.pop_frame()
        self.append_child_object(linenum, indent, path)

    def append_parent_object(self, linenum, indent, path):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        """
        frame = self.current_frame()
        assert frame.indent is not None and frame.indent > indent
        while frame.indent != indent:
            frame = self.pop_frame()
        self.append_sibling_object(linenum, indent, path)

    def append_child_field(self, linenum, indent, field_name, field_value):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        :param field_name:
        :type field_name: str
        :param field_value:
        :type field_value: str
        """
        frame = self.current_frame()
        assert isinstance(frame,RootFrame) or isinstance(frame,ContainerFrame) and frame.indent < indent
        if frame.container.contains(ROOT_PATH, field_name):
            raise KeyError("field {0} exists in container at path {1}".format(field_name, frame.path))
        frame.container.put_field(ROOT_PATH, field_name, field_value)
        frame = FieldFrame(linenum, indent, frame.path, frame.container, field_name, field_value)
        self.push_frame(frame)

    def append_sibling_field(self, linenum, indent, field_name, field_value):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        :param field_name:
        :type field_name: str
        :param field_value:
        :type field_value: str
        """
        frame = self.current_frame()
        assert frame.indent is not None and frame.indent == indent
        self.pop_frame()
        self.append_child_field(linenum, indent, field_name, field_value)

    def append_parent_field(self, linenum, indent, field_name, field_value):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param path:
        :type path: Path
        :param field_name:
        :type field_name: str
        :param field_value:
        :type field_value: str
        """
        frame = self.current_frame()
        assert frame.indent is not None and frame.indent > indent
        while frame.indent != indent:
            frame = self.pop_frame()
        self.append_sibling_field(linenum, indent, field_name, field_value)

    def append_value_continuation(self, linenum, indent, continuation):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param continuation:
        :type continuation: str
        """
        frame = self.current_frame()
        assert isinstance(frame,FieldFrame) or isinstance(frame,ValueContinuationFrame)
        if isinstance(frame, FieldFrame):
            assert frame.indent < indent and frame.container.contains(ROOT_PATH, frame.field_name)
        if isinstance(frame, ValueContinuationFrame):
            assert frame.indent == indent and frame.container.contains(ROOT_PATH, frame.field_name)
            self.pop_frame()
        field_value = frame.field_value + '\n' + continuation
        frame.container.put_field(ROOT_PATH, frame.field_name, field_value)
        frame = ValueContinuationFrame(linenum, indent, frame.path, frame.container, frame.field_name, field_value)
        self.push_frame(frame)

    def append_list_continuation(self, linenum, indent, continuation):
        """
        :param linenum: The line number of the frame.
        :type linenum: int
        :param indent: The indentation level of the frame.
        :type indent: int
        :param continuation:
        :type continuation: str
        """
        frame = self.current_frame()
        assert isinstance(frame,FieldFrame) or isinstance(frame,ListContinuationFrame)
        if isinstance(frame, FieldFrame):
            assert frame.indent < indent and frame.container.contains(ROOT_PATH, frame.field_name)
        if isinstance(frame, ListContinuationFrame):
            assert frame.indent == indent and frame.container.contains(ROOT_PATH, frame.field_name)
            self.pop_frame()
        frame.container.append_field(ROOT_PATH, frame.field_name, continuation)
        frame = ListContinuationFrame(linenum, indent, frame.path, frame.container, frame.field_name, continuation)
        self.push_frame(frame)

def parse_file(f):
    """

    :param f:
    :type f: file
    :returns:
    :rtype: pesky.settings.valuetree.ValueTree
    """
    values = ValueTree()
    parser = ParserContext(values)

    for linenum,indent,value in iter_lines(f):

        # skip comment lines
        if isinstance(value, Comment):
            continue

        # track the current indentation to determine if we descent, ascend,
        # or stay at the same indentation level
        current_indent = parser.current_indent()

        # add a new container
        if isinstance(value, ObjectDef):
            # object is a child of the root
            if current_indent is None:
                parser.append_child_object(linenum, indent, value.path)
            # object is a child of the current object
            elif current_indent < indent:
                parser.append_child_object(linenum, indent, value.path)
            # object is a sibling of the current object
            elif current_indent == indent:
                parser.append_sibling_object(linenum, indent, value.path)
            # object is a parent of the current object
            else:
                parser.append_parent_object(linenum, indent, value.path)

        # add a list item under the current container
        if isinstance(value, ListItemDef):
            pass

        # add a new field
        if isinstance(value, FieldDef):
            if current_indent is None:
                parser.append_child_field(linenum, indent, value.field_name, value.field_value)
            elif current_indent < indent:
                parser.append_child_field(linenum, indent, value.field_name, value.field_value)
            elif current_indent == indent:
                parser.append_sibling_field(linenum, indent, value.field_name, value.field_value)
            else:
                parser.append_parent_field(linenum, indent, value.field_name, value.field_value)

        # concatenate the continuation to value of the current field
        if isinstance(value, ValueContinuation):
            parser.append_value_continuation(linenum, indent, value.value_continuation)

        # append the continuation to the current field
        if isinstance(value, ListContinuation):
            parser.append_list_continuation(linenum, indent, value.list_continuation)

    return values

def print_ast(f):
    """
    :param f:
    :type f: file
    :return:
    """
    for linenum,indent,value in iter_lines(f):
        print("{0}{1}|{2}".format(str(linenum).rjust(3), ' ' * indent, value))


__all__ = [ 'parse_file', 'print_ast' ]
