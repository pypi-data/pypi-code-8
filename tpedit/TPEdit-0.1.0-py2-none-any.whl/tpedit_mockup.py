# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Thu Jul 02 10:56:57 2015
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""
### Imports
# Standard Library
from __future__ import print_function, division
from __future__ import absolute_import
import logging

# Third Party
import wx
import wx.gizmos as wxdv
from docopt import docopt

# Package / Application
try:
    # Imports used for unittests
#    from . import __init__ as __pybank_init
#    from . import pbsql
    logging.debug("Imports for UnitTests")
except SystemError:
    try:
        # Imports used by Spyder
#        import __init__ as __pybank_init
#        import pbsql
        logging.debug("Imports for Spyder IDE")
    except ImportError:
         # Imports used by cx_freeze
#        from pybank import __init__ as __pybank_init
#        from pybank import pbsql
        logging.debug("imports for Executable")

__author__ = "Douglas Thor"
__version__ = "v0.1.0"

### Module Constants
YELLOW = wx.Colour(255, 255, 0)


### Classes
class MainApp(object):
    """
    """
    def __init__(self):
        self.app = wx.App()

        self.frame = MainFrame("XmlEdit_Mockup", (1200, 650))

        self.frame.Show()
        self.app.MainLoop()


class MainFrame(wx.Frame):
    """
    """
    def __init__(self, title, size):
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          title=title,
                          size=size,
                          )
        self._init_ui()

    def _init_ui(self):
        """ Initi UI Components """
        # Create the menu bar and bind events
        self.menu_bar = wx.MenuBar()
        self._create_menus()
#        self._bind_events()

        # Initialize default states
#        self._set_defaults()

        # Set the MenuBar and create a status bar
        self.SetMenuBar(self.menu_bar)
        self.CreateStatusBar()

        self.panel = MainPanel(self)

    def _create_menus(self):
        """ Create each menu for the menu bar """
        self._create_file_menu()
#        self._create_edit_menu()
#        self._create_view_menu()
#        self._create_tools_menu()
#        self._create_options_menu()
#        self._create_help_menu()

    def _create_file_menu(self):
        """
        Creates the File menu.

        wxIDs:
        ------
        + 101: New
        + 102: Open
        + 103: Exit

        """
        # Create the menu and items
        self.mfile = wx.Menu()
        self.mf_new = wx.MenuItem(self.mfile, 101, "&New\tCtrl+N",
                                  "Create a new FTI Test Program file")
        self.mf_open = wx.MenuItem(self.mfile, 102, "&Open\tCtrl+O",
                                   "Open a Test Program file")
        self.mf_exit = wx.MenuItem(self.mfile, 103, "&Exit\tCtrl+Q",
                                   "Exit the application")

        # Add menu items to the menu
        self.mfile.AppendItem(self.mf_new)
        self.mfile.AppendItem(self.mf_open)
        self.mfile.AppendSeparator()
        self.mfile.AppendItem(self.mf_exit)
        self.menu_bar.Append(self.mfile, "&File")


class MainPanel(wx.Panel):
    """
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self._init_ui()

    def _init_ui(self):
        """
        """
        tree_style = (wx.TR_DEFAULT_STYLE
#                      | wx.TR_HAS_BUTTONS
                      | wx.TR_ROW_LINES
                      | wx.TR_COLUMN_LINES
                      | wx.TR_FULL_ROW_HIGHLIGHT
                      )
        self.tree = wxdv.TreeListCtrl(self,
                                      wx.ID_ANY,
                                      style=tree_style,
                                      )

        self.tree.AddColumn("MainColumn")
        self.tree.AddColumn("DataType")
        self.tree.AddColumn("TestProgram 1")
        self.tree.AddColumn("TestProgram 2")
        self.tree.AddColumn("TestProgram 3")
        self.tree.SetMainColumn(0)          # contains the tree
        self.tree.SetColumnWidth(0, 325)
        self.tree.SetColumnWidth(1, 200)
        self.tree.SetColumnWidth(2, 220)
        self.tree.SetColumnWidth(3, 220)
        self.tree.SetColumnWidth(4, 220)

        self.root = self.tree.AddRoot("Flow")
#        self.root = self.tree.GetRootItem()

        # add buncha items
        add_attribute(self.tree, self.root, "FlowType", "", "FTI.Flows6.Flows")
        properties = self.tree.AppendItem(self.root, "Properties")

        add_attribute(self.tree, properties, "DeviceType", "DeviceType", "Default")
        add_attribute(self.tree, properties, "ExceptionHandlingMethod", "ExceptionHandlingMethod", "Exceptions")
        add_attribute(self.tree, properties, "Name", "String", "ScreeningFlow")
        add_attribute(self.tree, properties, "Sites", "Sites:Values:UnsignedInt", "1")
        child = self.tree.AppendItem(properties, "StopOnFail")
        self.tree.SetItemText(child, "Boolean", 1)
        self.tree.SetItemText(child, "False", 2)
        self.tree.SetItemText(child, "True", 3)
        self.tree.SetItemText(child, "True", 4)
        self.tree.SetItemBackgroundColour(child, YELLOW)

        coordinators = self.tree.AppendItem(self.root, "Coordinators")
        add_attribute(self.tree, coordinators, "<placeholder>", "", "<placeholder>")

        root_test = self.tree.AppendItem(self.root, "Sequence (name of Root flow)")
        self.root_test = root_test
        properties = self.tree.AppendItem(root_test, "Properties")
        add_attribute(self.tree, properties, "Name", "String", "Sequence")
        add_attribute(self.tree, properties, "Channel", "DUTChannel", "None")

        ### Steps
        steps = self.tree.AppendItem(root_test, "Block: ConfigureDRDSBoard")
        self.block1 = steps
        add_attribute(self.tree, steps, "StepType", "", "FTI.Standards.SequenceStep")

        method = self.tree.AppendItem(steps, "Method")
        add_attribute(self.tree, method, "MethodType", "", "GanFETLibrary.ConfigureDRDSBoard")
        add_attribute(self.tree, method, "Shared", "Boolean", "True")

        method = self.tree.AppendItem(steps, "Properties (PropertyData)")
        add_attribute(self.tree, method, "Name", "String", "ConfigureDRDSBoard")
        add_attribute(self.tree, method, "Channel", "DUTChannel", "None")

        parameters = self.tree.AppendItem(steps, "Parameters")
        self.block1_params = parameters
        add_attribute(self.tree, parameters, "SenseConnect", "SenseConnectEnum", "Open")
        add_attribute(self.tree, parameters, "TabConnect", "Boolean", "True")
        add_attribute(self.tree, parameters, "VSense", "Double", "0")
        add_attribute(self.tree, parameters, "ISense", "Double", "1u")
        add_attribute(self.tree, parameters, "VTab", "Double", "0")
        add_attribute(self.tree, parameters, "ITab", "Double", "1u")

        ### KELVIN
        step = self.tree.AppendItem(steps, "1: KELVIN [TestNumber: Name] (Step)")
        self.step1 = step
        add_attribute(self.tree, step, "StepType", "", "FTI.Standards.MethodStep")

        method = self.tree.AppendItem(step, "Method")
        add_attribute(self.tree, method, "MethodType", "", "FETDCLibrary6.KELVIN")
        add_attribute(self.tree, method, "Shared", "Boolean", "True")

        method = self.tree.AppendItem(step, "Properties (PropertyData)")

        add_attribute(self.tree, method, "Skip", "Boolean", "False")
        add_attribute(self.tree, method, "IgnoreFail", "Boolean", "True")
        add_attribute(self.tree, method, "TestNumber", "UInt32", "1")
        add_attribute(self.tree, method, "Name", "String", "KELVIN")
        add_attribute(self.tree, method, "RendezvousingStep", "Booealn", "False")
        add_attribute(self.tree, method, "UseGoldenUnitData", "Booealn", "False")

        parameters = self.tree.AppendItem(step, "Parameters")
        self.step1_params = parameters
        add_attribute(self.tree, parameters, "PulseWidth", "Double", "300u")
        add_attribute(self.tree, parameters, "Samples", "Int32", "5")
        add_attribute(self.tree, parameters, "I_Apply", "IApplyEnum", "R25mA")
        add_attribute(self.tree, parameters, "EngMode", "Boolean", "True")
        add_attribute(self.tree, parameters, "RKELVIN_MAX", "", "RKELVIN_MAX")

        ### RDSON_LC
        step = self.tree.AppendItem(steps, "2: RDSON_LC [TestNumber: Name] (Step)")
        self.step2 = step
        add_attribute(self.tree, step, "StepType", "", "FTI.Standards.MethodStep")

        method = self.tree.AppendItem(step, "Method")
        add_attribute(self.tree, method, "MethodType", "", "FETDCLibrary6.RDSON")
        add_attribute(self.tree, method, "Shared", "Boolean", "True")

        method = self.tree.AppendItem(step, "Properties (PropertyData)")
        add_attribute(self.tree, method, "Skip", "Boolean", "False")
        child = self.tree.AppendItem(method, "IgnoreFail")
        self.tree.SetItemBackgroundColour(child, YELLOW)
        self.tree.SetItemText(child, "Boolean", 1)
        self.tree.SetItemText(child, "True", 2)
        self.tree.SetItemText(child, "True", 3)
        self.tree.SetItemText(child, "False", 4)
        add_attribute(self.tree, method, "TestNumber", "UInt32", "2")
        add_attribute(self.tree, method, "Name", "String", "RDSON_LC")
        add_attribute(self.tree, method, "RendezvousingStep", "Booealn", "False")
        add_attribute(self.tree, method, "UseGoldenUnitData", "Booealn", "False")

        parameters = self.tree.AppendItem(step, "Parameters")
        self.step2_params = parameters
        add_attribute(self.tree, parameters, "PulseWidth", "Double", "300u")
        child = self.tree.AppendItem(parameters, "ID")
        self.tree.SetItemBackgroundColour(child, YELLOW)
        self.tree.SetItemText(child, "Double", 1)
        self.tree.SetItemText(child, "4", 2)
        self.tree.SetItemText(child, "3", 3)
        self.tree.SetItemText(child, "4", 4)
        add_attribute(self.tree, parameters, "VGS", "Double", "0")
        add_attribute(self.tree, parameters, "Samples", "Int32", "5")
        add_attribute(self.tree, parameters, "DisconnectSense", "Boolean", "True")
        add_attribute(self.tree, parameters, "CurrentRange", "CurrentRangeEnum", "RangeAuto")
        add_attribute(self.tree, parameters, "GateRes10K", "Boolean", "False")
        add_attribute(self.tree, parameters, "StabilityCompensation", "StabilityCompensationEnum", "MediumFast")
        add_attribute(self.tree, parameters, "OneSiteAtATime", "OneSiteAtATimeEnum", "Normal_Behavior")
        add_attribute(self.tree, parameters, "RDSON_Max", "Double", "200m")
        add_attribute(self.tree, parameters, "RDSON_Min", "Double", "80m")

        ### Step not in block
        step = self.tree.AppendItem(root_test, "5: DynamicRDS_600V [TestNumber: Name] (Step)")
        self.step3 = step
        add_attribute(self.tree, step, "StepType", "", "FTI.Standards.MethodStep")

        method = self.tree.AppendItem(step, "Method")
        add_attribute(self.tree, method, "MethodType", "", "GaNFETLibrary.DynamicRDS")
        add_attribute(self.tree, method, "Shared", "Boolean", "True")

        method = self.tree.AppendItem(step, "Properties (PropertyData)")
        add_attribute(self.tree, method, "Skip", "Boolean", "False")
        add_attribute(self.tree, method, "IgnoreFail", "Boolean", "True")
        add_attribute(self.tree, method, "TestNumber", "UInt32", "5")
        add_attribute(self.tree, method, "Name", "String", "DynamicRDS_600V")
        add_attribute(self.tree, method, "RendezvousingStep", "Boolean", "False")
        add_attribute(self.tree, method, "UseGoldenUnitData", "Boolean", "False")

        parameters = self.tree.AppendItem(step, "Parameters (ConfigurationPropertyData.PropertyData)")
        self.step3_params = parameters
        add_attribute(self.tree, parameters, "VGSH", "Double", "0")
        add_attribute(self.tree, parameters, "VGSL", "Double", "-30")
        add_attribute(self.tree, parameters, "VDS_Stress", "Double", "600")
        add_attribute(self.tree, parameters, "IRangeX10", "Boolean", "False")
        add_attribute(self.tree, parameters, "ID_Meas", "Double", "6")
        add_attribute(self.tree, parameters, "ID_Adjust", "Double", "0")
        add_attribute(self.tree, parameters, "VDS_Meas", "Double", "0")
        add_attribute(self.tree, parameters, "VForce", "Boolean", "False")
        add_attribute(self.tree, parameters, "MeasDelay", "Double", "5u")
        add_attribute(self.tree, parameters, "MeasTime", "Double", "5u")
        add_attribute(self.tree, parameters, "StressTime", "Double", "100m")
        add_attribute(self.tree, parameters, "DischargeTime", "Double", "800n")
        add_attribute(self.tree, parameters, "WriteFile", "Boolean", "False")
        add_attribute(self.tree, parameters, "SampleRate", "Int32", "1")
        add_attribute(self.tree, parameters, "RDS_MAX", "Double", "250m")
        add_attribute(self.tree, parameters, "RDS_MIN", "Double", "80m")

        child = self.tree.AppendItem(parameters, "RDS_Shift_Max")
        self.tree.SetItemBackgroundColour(child, YELLOW)
        self.tree.SetItemText(child, "Double", 1)
        self.tree.SetItemText(child, "25", 2)
        self.tree.SetItemText(child, "20", 3)
        self.tree.SetItemText(child, "25", 4)

        add_attribute(self.tree, parameters, "RDS_Shift_Min", "Double", "-15")

        # Expand some items by default
        self.tree.Expand(self.root)
        self.tree.Expand(self.root_test)
        self.tree.Expand(self.block1)
        self.tree.Expand(self.step1)
        self.tree.Expand(self.step1_params)
        self.tree.Expand(self.step2)
        self.tree.Expand(self.step2_params)
        self.tree.Expand(self.step3)
        self.tree.Expand(self.step3_params)

        # Add a logging window
        log_style = (wx.TE_MULTILINE
                     | wx.TE_PROCESS_ENTER
                     )
        self.log = wx.TextCtrl(self, wx.ID_ANY, style=log_style)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.tree, 4, wx.EXPAND)
        self.vbox.Add(self.log, 1, wx.EXPAND)
        self.SetSizer(self.vbox)

        self._bind_events()

    def _bind_events(self):
        """
        """
        self.tree.GetMainWindow().Bind(wx.EVT_LEFT_DCLICK, self._on_dclick)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, None)

    def _on_dclick(self, event):
        """
        """
        pos = event.GetPosition()
        item, flags, col = self.tree.HitTest(pos)
        msg_text = """Double-clicking on an item will copy the value
too all open files:

Item: '{}', Value: '{}' propagated to all open files!"""
        if item:
            item_text = self.tree.GetItemText(item)
            col_text = self.tree.GetItemText(item, col)
            msg_text = msg_text.format(item_text, col_text)
            dialog = wx.MessageDialog(self,
                                      msg_text,
                                      "Item Propagated",
                                      wx.OK,
                                      )

        dialog.ShowModal()
        dialog.Destroy()


def add_tp_values(tree, child, value):
    """ """
    for _i in range(2, 5):
        tree.SetItemText(child, value, _i)


def add_attribute(tree, parent, name, databype, value):
    """ """
    child = tree.AppendItem(parent, name)
    tree.SetItemText(child, databype, 1)
    add_tp_values(tree, child, value)


def main():
    """ Main Code """
    docopt(__doc__, version=__version__)
    MainApp()


if __name__ == "__main__":
    main()
