---
name: chatgpt-image-download
description: Reliably extract and save ChatGPT-generated images from the OpenClaw managed browser when normal Download/Save clicks do not create a file. Use when ChatGPT image generation succeeds in the browser preview but the site download flow fails, saves the wrong file, returns 403 outside the logged-in session, or requires capturing the image through the active browser session.
---

# ChatGPT Image Download

Use this skill when a ChatGPT image is visible in the browser but ordinary save/download actions are unreliable.

## Goal

Save the actual generated image through the logged-in browser session instead of relying on an unauthenticated external fetch.

## Core workflow

1. Confirm the image is visible in ChatGPT.
2. Open the image preview when possible.
3. Inspect the live page with `openclaw browser evaluate` to identify the real in-session image URL.
4. Treat `403 Forbidden` from direct external fetches as expected for protected assets.
5. Use `openclaw browser waitfordownload <name>` before clicking **Save** or **Download**.
6. Copy the captured file from `/tmp/openclaw/downloads/` to the requested destination.
7. Verify the final file with `file` and `stat`.

## Why this skill exists

Typical failure modes:

- Clicking **Download** or **Save** appears to work, but no file lands in `~/Downloads`
- The wrong file gets saved
- Direct `curl` / Python / urllib download returns `403 Forbidden`
- The preview clearly shows the image, but the host cannot retrieve it outside the browser session

In these cases, use the browser session itself as the trusted download path.

## Minimal sequence

### 1. Confirm or open the image preview

```bash
openclaw browser --browser-profile openclaw snapshot --limit 260
openclaw browser --browser-profile openclaw click <image-ref>
```

### 2. Inspect live images in the page

```bash
openclaw browser --browser-profile openclaw evaluate --fn '() => Array.from(document.images).map((img,i)=>({i,alt:img.alt||"",src:img.currentSrc||img.src||"",w:img.naturalWidth,h:img.naturalHeight})).filter(x=>x.src)'
```

Match by `alt`, dimensions, and preview state.

### 3. Capture the browser-managed download

```bash
openclaw browser --browser-profile openclaw waitfordownload orange.png
openclaw browser --browser-profile openclaw click <save-ref>
```

Success looks like:

```text
downloaded: /tmp/openclaw/downloads/orange.png
```

### 4. Move and verify the file

```bash
cp -f /tmp/openclaw/downloads/orange.png "$HOME/下載/orange.png"
file -b --mime-type "$HOME/下載/orange.png"
stat -c 'size=%s bytes' "$HOME/下載/orange.png"
```

Healthy result example:

```text
image/png
size=1416031 bytes
```

## Decision rules

- If inline **Download** fails, open preview and try preview **Save**.
- If preview **Save** still does not land a file, use `waitfordownload`.
- If direct external fetch returns `403`, stop retrying external fetches.
- If the wrong file appears, ignore the naive download result and re-run with `waitfordownload` tied to the active preview action.

## Notes

- Prefer the browser session over `curl`, Python `urllib`, or other external fetch methods for protected ChatGPT assets.
- Verify the saved file before reporting success.
- Rename the verified file afterward if the user wants a cleaner filename.

## Reference files

- Read `references/troubleshooting.md` for symptom-to-fix mapping and the full recovery flow.
