# SaveUtils – FreeCAD Workbench Addon

![SaveUtils Example in the FreeCAD File menu](https://jefftml.s3.amazonaws.com/thumbs/SaveUtilsExample1.png)

[SaveUtils](https://github.com/jefe317/SaveUtils/) adds two convenience commands to FreeCAD's **File** menu:

| Command | What it does |
|---|---|
| **Save As with Timestamp** | Saves a copy as `<basename>-YYYYMMDD-HHMMSS.FCStd` |
| **Save As Increment** | Saves a copy as `<basename>-01.FCStd`, `…-02.FCStd`, etc. |

Both commands switch FreeCAD to the newly saved file so you keep working in it.

## Behavior details

### Save As with Timestamp
- Pattern appended: `-YYYYMMDD-HHMMSS.FCStd`  
- If the current filename already ends with this pattern it is **replaced**, not doubled.  
  `design-20240101-120000.FCStd` → `design-20240315-093045.FCStd`
- Unsaved document: a file-picker dialog asks for a base filename first.

### Save As Increment
- Pattern appended: `-NN.FCStd` (always zero-padded to 2 digits).  
- If the filename already ends with `-N.FCStd` or `-NN.FCStd` the number is incremented:  
  `design-03.FCStd` → `design-04.FCStd`  
  `design-8.FCStd`  → `design-09.FCStd`
- Unsaved document: a file-picker dialog asks for a base filename first.

## Installation

### Manual (recommended for development)

1. Copy the `SaveUtils/` folder into your FreeCAD **Mod** directory:

   | OS | Path |
   |---|---|
   | Linux | `~/.local/share/FreeCAD/Mod/` |
   | macOS | `~/Library/Application Support/FreeCAD/Mod/` |
   | Windows | `%APPDATA%\FreeCAD\Mod\` |

2. Restart FreeCAD.  
   The two items appear near the top of **File → Save As with Timestamp / Save As Increment**.

### Via Addon Manager

If this repo is listed in a custom addon source, you can install it through  
**Tools → Addon Manager**.

## Requirements

- FreeCAD 0.20 or later  
- PySide2 (bundled with FreeCAD)

## License

GPL v3
