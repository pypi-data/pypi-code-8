#------------------------------------------------------------------------------
# Copyright (c) 2011, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#------------------------------------------------------------------------------

from pyface.qt import QtCore, QtGui
from kiva.cairo import CompiledPath, GraphicsContext, font_metrics_provider

from base_window import BaseWindow
from scrollbar import NativeScrollBar

class Window(BaseWindow):
    def _create_gc(self, size, pix_format="bgra32"):
        gc = GraphicsContext((size[0]+1, size[1]+1))
        gc.translate_ctm(0.5, 0.5)

        return gc

    def _window_paint(self, event):
        if self.control is None:
           return

        # self._gc is an image context
        w = self._gc.width()
        h = self._gc.height()
        data = self._gc.pixel_map.convert_to_argbarray()

        image = QtGui.QImage(data, w, h, QtGui.QImage.Format_ARGB32)

        rect = QtCore.QRect(0,0,w,h)
        painter = QtGui.QPainter(self.control)
        painter.drawImage(rect, image)



# EOF
