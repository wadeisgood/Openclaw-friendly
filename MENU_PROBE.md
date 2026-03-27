# MENU_PROBE.md

Minimal MVP for GNOME Wayland context-menu probing.

## What works now

- GNOME Shell DBus screenshot API
  - fullscreen
  - active window
  - fixed area
- Basic OCR via tesseract (`chi_tra+eng`)
- JSON report written to `/tmp/menu-probe/report.json`

## Script

```bash
./tools_menu_probe.py
```

Outputs:

- `/tmp/menu-probe/before.png`
- `/tmp/menu-probe/window.png`
- `/tmp/menu-probe/area.png`
- `/tmp/menu-probe/before.txt`
- `/tmp/menu-probe/report.json`

## Current status

This is only the screenshot/OCR backbone.
It does **not yet** do:

- before/after diff for popup detection
- AT-SPI menu subtree dump
- OCR bounding boxes for `複製`
- matching OCR result to AT-SPI actionable nodes
- automatic menu action execution

## Planned next steps

1. Add `before` / `after` capture pair
2. Add image diff step to isolate newly appeared menu region
3. OCR cropped menu region
4. Dump AT-SPI subtree around popup menu
5. Match OCR text (`複製`) to actionable `menu item`
6. Try action-first execution
