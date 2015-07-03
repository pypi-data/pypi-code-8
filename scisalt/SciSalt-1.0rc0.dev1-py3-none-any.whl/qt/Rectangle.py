import numpy as _np
import matplotlib as mpl

class Rectangle(object):
    def __init__(self,x,y,width,height,axes=None,alpha=0.5,fill=True):
        self._axes = axes
        self._rect = mpl.patches.Rectangle((x,y),width,height,facecolor='w',edgecolor='r',alpha=alpha,fill=fill,axes=self._axes)

    def get_rect(self):
        return self._rect
    patch = property(get_rect)

    def _get_sorted_x(self):
        x_a = self._rect.get_x()
        x_b = x_a + self._rect.get_width()
        return _np.sort([x_a,x_b])

    _sorted_x = property(_get_sorted_x)

    def _get_x0(self):
        return self._sorted_x[0]

    def _get_x1(self):
        return self._sorted_x[1]
    
    x0 = property(_get_x0,doc='The smaller x coordinate.')
    x1 = property(_get_x1,doc='The larger x coordinate.')

    def get_x(self):
        return self.x0

    def _get_sorted_y(self):
        y_a = self._rect.get_y()
        y_b = y_a + self._rect.get_height()
        return _np.sort([y_a,y_b])

    _sorted_y = property(_get_sorted_y)

    def _get_y0(self):
        return self._sorted_y[0]

    def _get_y1(self):
        return self._sorted_y[1]
    
    y0 = property(_get_y0,doc='The smaller y coordinate.')
    y1 = property(_get_y1,doc='The larger y coordinate.')

    def get_y(self):
        return self.y0

    def get_xy(self):
        return (self.get_x(),self.get_y())

    def get_width(self):
        return self.x1-self.x0

    def get_height(self):
        return self.y1-self.y0

    def set_xy(self,value):
        return self._rect.set_xy(value)

    def set_width(self,value):
        return self._rect.set_width(value)

    def set_height(self,value):
        return self._rect.set_height(value)
