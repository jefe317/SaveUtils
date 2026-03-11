"""
SaveUtils.py  -  core logic for the SaveUtils FreeCAD addon.
"""

import re
import os
import datetime

import FreeCAD
import FreeCADGui
from PySide2 import QtWidgets   # FreeCAD 0.21+ ships PySide2

FreeCAD.Console.PrintMessage("=== SaveUtils: SaveUtils.py loading ===\n")

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------
_TS_PATTERN  = re.compile(r'-\d{8}-\d{6}\.FCStd$', re.IGNORECASE)
_INC_PATTERN = re.compile(r'-(\d{1,2})\.FCStd$',   re.IGNORECASE)
_EXT_PATTERN = re.compile(r'\.FCStd$',              re.IGNORECASE)


def _strip_fcstd(path):
    return _EXT_PATTERN.sub('', path)


def _get_base_path():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        QtWidgets.QMessageBox.warning(
            FreeCADGui.getMainWindow(), "SaveUtils", "No active document.")
        return None
    return doc.FileName or None


def _ask_base_filename(title):
    path, _ = QtWidgets.QFileDialog.getSaveFileName(
        FreeCADGui.getMainWindow(),
        title,
        os.path.expanduser("~/untitled"),
        "FreeCAD files (*.FCStd)"
    )
    if not path:
        return None
    return _strip_fcstd(path)


def _save_as(new_path):
    doc = FreeCAD.ActiveDocument
    try:
        doc.saveAs(new_path)
        FreeCAD.Console.PrintMessage(f"SaveUtils: saved as '{new_path}'\n")
        return True
    except Exception as exc:
        QtWidgets.QMessageBox.critical(
            FreeCADGui.getMainWindow(), "SaveUtils error",
            f"Could not save file:\n{exc}")
        return False


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

class CmdSaveTimestamp:
    def GetResources(self):
        return {
            'MenuText': 'Save As with Timestamp',
            'ToolTip':  'Save a copy appending -YYYYMMDD-HHMMSS to the filename',
            'Pixmap':   '',
        }

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        current = _get_base_path()
        if current:
            base = _TS_PATTERN.sub('', current) if _TS_PATTERN.search(current) else _strip_fcstd(current)
        else:
            base = _ask_base_filename("Save As with Timestamp – choose base filename")
            if base is None:
                return
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        _save_as(f"{base}-{stamp}.FCStd")


class CmdSaveIncrement:
    def GetResources(self):
        return {
            'MenuText': 'Save As Increment',
            'ToolTip':  'Save a copy incrementing the trailing -NN counter',
            'Pixmap':   '',
        }

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        current = _get_base_path()
        if current:
            m = _INC_PATTERN.search(current)
            if m:
                new_num = int(m.group(1)) + 1
                base    = current[:m.start()]
                _save_as(f"{base}-{new_num:02d}.FCStd")
            else:
                _save_as(f"{_strip_fcstd(current)}-01.FCStd")
        else:
            base = _ask_base_filename("Save As Increment – choose base filename")
            if base is None:
                return
            _save_as(f"{base}-01.FCStd")


# ---------------------------------------------------------------------------
# Menu injection
# ---------------------------------------------------------------------------

def install():
    FreeCAD.Console.PrintMessage("=== SaveUtils: install() called ===\n")

    # Register commands
    FreeCADGui.addCommand('SaveUtils_Timestamp', CmdSaveTimestamp())
    FreeCADGui.addCommand('SaveUtils_Increment', CmdSaveIncrement())

    _inject_menu()


def _inject_menu():
    mw = FreeCADGui.getMainWindow()
    if mw is None:
        FreeCAD.Console.PrintError("=== SaveUtils: main window not found ===\n")
        return

    menubar   = mw.menuBar()
    file_menu = None

    # Search by objectName first (most reliable), then fall back to display text
    for action in menubar.actions():
        menu = action.menu()
        if menu is None:
            continue
        obj_name = menu.objectName().replace('&', '').strip().lower()
        disp_name = action.text().replace('&', '').strip().lower()
        if obj_name in ('file', '&file') or disp_name == 'file':
            file_menu = menu
            break

    if file_menu is None:
        FreeCAD.Console.PrintError("=== SaveUtils: File menu not found ===\n")
        FreeCAD.Console.PrintMessage(
            "=== SaveUtils: menus found: " +
            str([(a.text(), a.menu().objectName() if a.menu() else '') for a in menubar.actions()])
            + " ===\n")
        return

    # Avoid duplicates
    for act in file_menu.actions():
        if act.text() == 'Save As with Timestamp':
            FreeCAD.Console.PrintMessage("=== SaveUtils: already installed, skipping ===\n")
            return

    # Build plain QActions
    ts_action = QtWidgets.QAction('Save As with Timestamp', file_menu)
    ts_action.setToolTip('Save a copy appending -YYYYMMDD-HHMMSS to the filename')
    ts_action.triggered.connect(lambda: FreeCADGui.runCommand('SaveUtils_Timestamp'))

    inc_action = QtWidgets.QAction('Save As Increment', file_menu)
    inc_action.setToolTip('Save a copy incrementing the trailing -NN counter')
    inc_action.triggered.connect(lambda: FreeCADGui.runCommand('SaveUtils_Increment'))

    # Insert before the first separator
    actions       = file_menu.actions()
    insert_before = next((a for a in actions if a.isSeparator()), None)

    if insert_before:
        file_menu.insertAction(insert_before, ts_action)
        file_menu.insertAction(insert_before, inc_action)
        file_menu.insertSeparator(insert_before)
    else:
        file_menu.addSeparator()
        file_menu.addAction(ts_action)
        file_menu.addAction(inc_action)

    FreeCAD.Console.PrintMessage("=== SaveUtils: menu items injected ===\n")
