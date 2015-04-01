#
# (C) Copyright 2015 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
"""
MoveCommandTool
===============

A MoveTool that uses AppTools' undo/redo infrastructure to create undoable move
commands.

"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from traits.api import Bool, Tuple

from enable.tools.move_tool import MoveTool

from .command_tool import BaseCommandTool
from .commands import MoveCommand


class MoveCommandTool(MoveTool, BaseCommandTool):
    """ Move tool which pushes MoveCommands onto a CommandStack

    This tool pushes a single MoveCommands onto its CommandStack at
    the end of the drag operation.  If the drag is cancelled, then no command
    is issued, and no commands are issued during the drag operation.

    """

    #-------------------------------------------------------------------------
    # 'MoveCommandTool' interface
    #-------------------------------------------------------------------------

    #: Whether or not subsequent moves can be merged with this one.
    mergeable = Bool

    #: The initial component position.
    _initial_position = Tuple(0, 0)

    #-------------------------------------------------------------------------
    # 'DragTool' interface
    #-------------------------------------------------------------------------

    def drag_start(self, event):
        if self.component:
            # we need to save the initial position to give to the Command
            self._initial_position = tuple(self.component.position)
        return super(MoveCommandTool, self).drag_start(event)

    def drag_end(self, event):
        """ End the drag operation, issuing a MoveCommands """
        if self.component:
            command = self.command(
                component=self.component,
                previous_position=self._initial_position,
                new_position=tuple(self.component.position),
                mergeable=self.mergeable)
            self.command_stack.push(command)
            event.handled = True

    def drag_cancel(self, event):
        """ Restore the component's position if the drag is cancelled.

        A drag is usually cancelled by receiving a mouse_leave event when
        `end_drag_on_leave` is True, or by the user pressing any of the
        `cancel_keys`.

        """
        if self.component:
            self.component.position = list(self._initial_position)

            event.handled = True

    #-------------------------------------------------------------------------
    # Trait handlers
    #-------------------------------------------------------------------------

    def _command_default(self):
        return MoveCommand
