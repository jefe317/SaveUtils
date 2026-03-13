"""
SaveUtils FreeCAD Addon - InitGui.py
"""

import FreeCAD
import FreeCADGui

FreeCAD.Console.PrintMessage("=== SaveUtils: InitGui.py loading ===\n")


class SaveUtilsWorkbench(FreeCADGui.Workbench):
    MenuText = "SaveUtils"
    ToolTip  = "Save utility commands"

    def Initialize(self):
        pass

    def Activated(self):
        pass

    def Deactivated(self):
        pass


FreeCADGui.addWorkbench(SaveUtilsWorkbench())


def _on_workbench_activated(name):
    # NoneWorkbench fires before the UI is ready — skip it
    if name == "NoneWorkbench":
        return

    # Disconnect immediately so this only runs once
    try:
        FreeCADGui.getMainWindow().workbenchActivated.disconnect(_on_workbench_activated)
    except Exception:
        pass

    try:
        import SaveUtils
        SaveUtils.install()
    except Exception as e:
        FreeCAD.Console.PrintError(f"=== SaveUtils install error: {e} ===\n")


FreeCADGui.getMainWindow().workbenchActivated.connect(_on_workbench_activated)
