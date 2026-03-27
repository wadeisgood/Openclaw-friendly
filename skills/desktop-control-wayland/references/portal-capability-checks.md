# Portal Capability Checks

## What was observed

The desktop exposed these relevant interfaces/capabilities:

- `org.freedesktop.portal.Screenshot`
- `org.freedesktop.portal.RemoteDesktop`
- `org.freedesktop.portal.ScreenCast`
- `org.freedesktop.portal.InputCapture`
- `org.gnome.Mutter.RemoteDesktop`
- `org.gnome.Mutter.ScreenCast`

This means the system has the correct class of Wayland-native desktop control/capture services.

## Practical screenshot test

A direct GNOME Shell screenshot DBus call was attempted:

```bash
gdbus call --session \
  --dest org.gnome.Shell.Screenshot \
  --object-path /org/gnome/Shell/Screenshot \
  --method org.gnome.Shell.Screenshot.Screenshot \
  false false /tmp/openclaw-shell-screenshot.png
```

Result:

```text
GDBus.Error:org.freedesktop.DBus.Error.AccessDenied: Screenshot is not allowed
```

## Interpretation

The interface exists, but the current caller/session does not yet have the permissions or portal session context required to use it.

## Operational meaning

- Capability discovery: **yes**
- Usable screenshot pipeline from current context: **not yet**
- More permission/session work is needed before this becomes a stable automation building block.
