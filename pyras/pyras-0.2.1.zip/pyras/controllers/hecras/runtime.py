"""
"""
import os
import time

import win32con
import win32gui
import win32process


class Runtime(object):
    """ """
    def __init__(self, parent):
        self.window = None
        self.parent = parent
        self.parent_pid = None
        self.parent_window = None
        self.get_pid()

    def close(self):
        """ """
        kill_process(self.parent_pid)

    def get_pid(self):
        """ """
        self.parent.ShowRas()
        window_text = 'HEC-RAS '

        def enumHandler(hwnd, lParam):
            if window_text in win32gui.GetWindowText(hwnd):
                self.parent_window = hwnd
                return None

        win32gui.EnumWindows(enumHandler, None)
        _, pid = win32process.GetWindowThreadProcessId(self.parent_window)
        win32gui.ShowWindow(self.parent_window, win32con.SW_HIDE)
        self.parent_pid = pid

    # %% Handle GUI waiting for routines that do not stop runtime
    def pause_bc(self, close=False):
        """ """
        self._pause(window_text='Bridge Culvert Data', close=close)

    def pause_geo(self, close=False):
        """ """
        self._pause(window_text='Geometric Data', close=close)

    def pause_iw(self, close=False):
        """ """
        self._pause(window_text='Inline Structure Data', close=close)

    def pause_lw(self, close=False):
        """ """
        self._pause(window_text='Lateral Structure Editor', close=close)

    def pause_multiple(self, close=False):
        """ """
        self._pause(window_text='Run Multiple Plans', close=close)

    def pause_plan(self, close=False):
        """ """
        self._pause(window_text='Steady Flow Analysis', close=close)

    def pause_quasi(self, close=False):
        """ """
        self._pause(window_text='Quasi Unsteady Flow Editor', close=close)

    def pause_sediment(self, close=False):
        """ """
        self._pause(window_text='Sediment Data', close=close)

    def pause_steady(self, close=False):
        """ """
        self._pause(window_text='Steady Flow Data', close=close)

    def pause_unsteady(self, close=False):
        """ """
        self._pause(window_text='Unsteady Flow Data', close=close)

    def pause_quality(self, close=False):
        """ """
        self._pause(window_text='Water Quality Data', close=close)

    def pause_xs(self, close=False):
        """ """
        self._pause(window_text='Cross Section Data', close=close)

    def pause(self, time_seconds):
        """ """
        time.sleep(time_seconds)

    def pause_text(self, window_text=None, close=False):
        self._pause(window_text, close)

    def _pause(self, window_text=None, close=False):
        """ """
        def enumHandler(hwnd, lParam):
            if window_text in win32gui.GetWindowText(hwnd):
                self.window = hwnd
        win32gui.EnumWindows(enumHandler, None)

        if close:
            # Close the window after a small amount of time
            win32gui.PostMessage(self.window, win32con.WM_CLOSE, 0, 0)
        else:
            pause_check = True
            while pause_check:
                time.sleep(0.5)  # Prevent fan noise from CPU "over use"
                if not win32gui.IsWindowVisible(self.window):
                    pause_check = False
                    self.window = None


def kill_process(pid):
    """ """
    try:
        killed = os.system('TASKKILL /PID {} /F >nul'.format(pid))
    except Exception:
        killed = 0
    return killed
