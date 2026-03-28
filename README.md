# OpenClaw-friendly Skills

這個 repo 是一個**已整理、已納管的 OpenClaw skill 倉庫**，目前聚焦在三類明確問題：

- Linux GUI browser 修復
- Wayland 桌面控制能力診斷
- ChatGPT 圖片可靠下載

它只保留目前確定有維護、已打包、已提交到 git 的技能內容；本地工作區中的個人檔案、記憶檔、暫存技能與實驗資料不納入版本控制。

### 正式納管的 skills

- `skills/control-gui-setting/`
  - 修復 Linux 桌面環境下 OpenClaw managed browser 無法正常開啟 / 控制的問題
- `skills/desktop-control-wayland/`
  - 診斷 GNOME Wayland 桌面直接控制能力，例如 `ydotool`、portal、截圖權限
- `skills/chatgpt-image-download/`
  - 當 ChatGPT 已生成圖片，但一般 Download / Save 無法正常落地時，透過登入中的瀏覽器 session 可靠抓圖

### 根目錄打包檔

- `control-gui-setting.skill`
- `desktop-control-wayland.skill`
- `chatgpt-image-download.skill`

### 技能邊界

#### `control-gui-setting`
處理：browser 啟動失敗、GUI session 環境傳遞、OpenClaw managed browser 啟動與 tool exposure 判斷。

#### `desktop-control-wayland`
處理：Wayland 桌面控制能力檢查、`ydotoold` / `ydotool` 注入鏈、portal / screenshot / remote desktop capability。

#### `chatgpt-image-download`
處理：ChatGPT 圖片另存失敗、直接抓圖 403、透過登入中的瀏覽器 session 可靠下載圖片。

### 未納管內容

工作區裡可能還存在一些**本地用途**內容，例如：

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `memory/`
- `.openclaw/`
- `skills/clawteam/`
- 個人腳本、虛擬環境、簡報檔

這些內容不是這個 repo 的正式技能發布範圍，因此已透過 `.gitignore` 排除。

### 結構

```text
skills/
  chatgpt-image-download/
  control-gui-setting/
  desktop-control-wayland/
```

### 維護原則

- 名稱清楚
- 邊界單一
- SKILL.md 保持精簡
- 細節放到 `references/`
- 打包檔與來源內容同步更新
- 個人工作區資料不要直接混進 repo

---

This repository is a **curated and version-controlled OpenClaw skill collection**. It currently focuses on three concrete problem areas:

- Linux GUI browser repair
- Wayland desktop control diagnostics
- Reliable ChatGPT image download

Only maintained, packaged, and git-tracked skill content is kept in this repo. Personal workspace files, memory files, temporary skills, and experimental data are intentionally excluded from version control.

### Officially managed skills

- `skills/control-gui-setting/`
  - Repair OpenClaw managed browser launch/control issues on Linux desktop environments
- `skills/desktop-control-wayland/`
  - Diagnose GNOME Wayland desktop control capability such as `ydotool`, portals, and screenshot permissions
- `skills/chatgpt-image-download/`
  - Reliably download ChatGPT-generated images through the logged-in browser session when normal Download / Save does not create a file

### Packaged skill bundles at repo root

- `control-gui-setting.skill`
- `desktop-control-wayland.skill`
- `chatgpt-image-download.skill`

### Skill boundaries

#### `control-gui-setting`
Handles browser startup failures, GUI session environment propagation, and OpenClaw managed browser startup / tool exposure diagnosis.

#### `desktop-control-wayland`
Handles Wayland desktop control capability checks, `ydotoold` / `ydotool` input injection path, and portal / screenshot / remote desktop capability inspection.

#### `chatgpt-image-download`
Handles failed ChatGPT image saves, direct-fetch 403 responses, and reliable image capture through the authenticated browser session.

### Unmanaged local content

The workspace may still contain **local-only** content such as:

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `memory/`
- `.openclaw/`
- `skills/clawteam/`
- personal scripts, virtual environments, and slide decks

These are not part of the published skill repository scope, so they are excluded through `.gitignore`.

### Structure

```text
skills/
  chatgpt-image-download/
  control-gui-setting/
  desktop-control-wayland/
```

### Maintenance principles

- Use clear names
- Keep a single responsibility boundary per skill
- Keep SKILL.md concise
- Move details into `references/`
- Keep packaged bundles in sync with source content
- Do not mix personal workspace data into the repository
