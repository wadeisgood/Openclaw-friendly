---
name: desktop-control-wayland
description: Diagnose and partially enable direct desktop control on a GNOME Wayland Linux machine, focusing on keyboard/mouse injection via ydotool/ydotoold and screenshot/desktop-portal capability checks. Use when a user wants the agent to control the local desktop itself rather than only a managed browser, especially on Ubuntu/GNOME Wayland systems such as wade-desktop.
---

# Desktop Control on GNOME Wayland

Use this skill when the goal is to control the **desktop itself** on a Wayland Linux session, not just a browser page.

## Scope

This skill currently covers:

- verifying Wayland desktop control prerequisites
- bringing up `ydotoold`
- validating whether `ydotool` can talk to its backend
- checking whether screenshot/remote-desktop portals exist
- documenting known limits and what is still missing for a production-quality workflow

This skill does **not** claim full desktop automation is solved in every case. It documents the tested working pieces and the known blockers.

## Tested environment

The workflow was tested on a machine with:

- GNOME Wayland
- `DISPLAY=:0`
- `WAYLAND_DISPLAY=wayland-0`
- `XDG_SESSION_TYPE=wayland`

## Key findings

### 1. `ydotool` is the most direct input-injection candidate

Useful because GNOME Wayland does not support classic X11 tooling in the usual way.

Installed commands observed:

- `ydotool`
- `ydotoold`

Useful subcommands seen:

- `type`
- `recorder`
- `mousemove`
- `key`
- `click`

### 2. `ydotoold` must be running

If `ydotool` reports:

```text
ydotoold backend unavailable
```

then start `ydotoold` first.

Example:

```bash
nohup ydotoold >/tmp/ydotoold.log 2>&1 &
sleep 2
```

Healthy signs:

```text
ydotoold: listening on socket /tmp/.ydotool_socket
```

And subsequent `ydotool` commands should say:

```text
Using ydotoold backend
```

### 3. Backend connectivity is not the same as visible desktop control success

A successful backend message means the injection chain exists. It does **not** automatically prove that:

- the intended window has focus
- mouse coordinates are correct
- input was accepted by the GUI target
- the action caused a visible desktop change

Always separate these two levels:

1. **backend connectivity**
2. **observable desktop effect**

### 4. Wayland screenshot / remote desktop capabilities exist, but may still be access-gated

The following interfaces were observed on the system bus/session bus side:

- `org.freedesktop.portal.Screenshot`
- `org.freedesktop.portal.RemoteDesktop`
- `org.freedesktop.portal.ScreenCast`
- `org.freedesktop.portal.InputCapture`
- `org.gnome.Mutter.RemoteDesktop`
- `org.gnome.Mutter.ScreenCast`

This means the machine has the **right class of capabilities** for Wayland-native control and capture.

### 5. Screenshot capability may still be denied at runtime

A practical GNOME screenshot DBus attempt returned:

```text
GDBus.Error:org.freedesktop.DBus.Error.AccessDenied: Screenshot is not allowed
```

Interpretation:

- the interface exists
- the capability is not fully granted to the current caller/session
- further policy / approval / portal-session work is needed

## Recommended workflow

### Step 1: verify environment

```bash
printf 'DISPLAY=%s\nWAYLAND_DISPLAY=%s\nXDG_SESSION_TYPE=%s\n' "$DISPLAY" "$WAYLAND_DISPLAY" "$XDG_SESSION_TYPE"
```

Expected for this workflow:

```text
DISPLAY=:0
WAYLAND_DISPLAY=wayland-0
XDG_SESSION_TYPE=wayland
```

### Step 2: verify tool presence

```bash
command -v ydotool
command -v ydotoold
command -v gdbus
command -v busctl
```

### Step 3: bring up `ydotoold`

```bash
nohup ydotoold >/tmp/ydotoold.log 2>&1 &
sleep 2
sed -n '1,40p' /tmp/ydotoold.log
```

### Step 4: verify backend connectivity

```bash
ydotool key 42:1 42:0
ydotool mousemove 1 1
```

Success indicator:

```text
Using ydotoold backend
```

### Step 5: verify portal presence

```bash
gdbus introspect --session --dest org.freedesktop.portal.Desktop --object-path /org/freedesktop/portal/desktop
```

Look for:

- `org.freedesktop.portal.Screenshot`
- `org.freedesktop.portal.RemoteDesktop`
- `org.freedesktop.portal.ScreenCast`
- `org.freedesktop.portal.InputCapture`

### Step 6: attempt screenshot capture

A simple GNOME screenshot DBus attempt:

```bash
gdbus call --session \
  --dest org.gnome.Shell.Screenshot \
  --object-path /org/gnome/Shell/Screenshot \
  --method org.gnome.Shell.Screenshot.Screenshot \
  false false /tmp/openclaw-shell-screenshot.png
```

If it fails with AccessDenied, note that the interface exists but is not yet usable from the current context.

## Known limits from testing

### `ydotool`

- Backend connectivity was achieved.
- A visible, fully verified desktop-effect workflow was **not** completed yet.
- One attempted absolute mouse-move form failed because this build did not accept `--absolute`.
- You may need target-specific focus logic or different coordinate handling.

### Screenshot / desktop capture

- Portal and GNOME screenshot interfaces exist.
- A direct screenshot call was denied.
- Additional permission / session negotiation is still required before this becomes a dependable capture path.

## Practical conclusion

As of current testing:

- **Keyboard/mouse injection path:** partially working (`ydotoold` + `ydotool` backend connected)
- **Desktop screenshot path:** capability exists but is still permission-gated
- **Production-ready full desktop control:** not yet complete

## When to use this skill vs browser automation

Use this skill when the user specifically wants:

- desktop-wide control
- keyboard/mouse event injection
- screen capture outside the managed browser
- Wayland-native desktop automation investigation

Use browser automation instead when the task can stay inside a supported browser surface. Browser automation is still the more reliable option for most web workflows.

## References

- `references/ydotool-notes.md`
- `references/portal-capability-checks.md`
