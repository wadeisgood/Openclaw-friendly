# ydotool Notes

## Observed commands

`ydotool --help` showed:

- `type`
- `recorder`
- `mousemove`
- `key`
- `click`

## Important behavior

If `ydotoold` is not running, `ydotool` may report:

```text
ydotoold backend unavailable
```

Starting the daemon directly with:

```bash
nohup ydotoold >/tmp/ydotoold.log 2>&1 &
```

produced:

```text
ydotoold: listening on socket /tmp/.ydotool_socket
```

After that, test commands reported:

```text
Using ydotoold backend
```

## Caveat

A working backend is not the same as a fully verified visible desktop effect. Focus, coordinate mapping, and target window state still matter.

## Tested command snippets

```bash
ydotool key 42:1 42:0
ydotool mousemove 1 1
ydotool type --delay 80 'OPENCLAW_YDOTOOL_TEST'
```

## Notes about coordinates

One attempted form using `--absolute` was not accepted by the installed build, so command syntax must be matched to the local `ydotool` version.
