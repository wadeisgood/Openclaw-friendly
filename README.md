# OpenClaw-friendly Skills

這個 repo 現在整理成一個**多 skill 技能倉庫**，不是只有單一 skill。

## 目前保留的 skill

- `skills/control-gui-setting/`
  - 修復 Linux 桌面環境下 OpenClaw managed browser 無法正常開啟 / 控制的問題
- `skills/desktop-control-wayland/`
  - 診斷 GNOME Wayland 桌面直接控制能力，例如 `ydotool`、portal、截圖權限
- `skills/chatgpt-image-download/`
  - 當 ChatGPT 已生成圖片，但一般 Download / Save 無法正常落地時，透過登入中的瀏覽器 session 可靠抓圖

## 根目錄打包檔

- `control-gui-setting.skill`
- `desktop-control-wayland.skill`
- `chatgpt-image-download.skill`

這些是對應 skill 的打包版本，可直接分發或安裝。

## 本次整理方向

已將 repo 內容朝以下原則收斂：

- **一個 skill 只負責一類問題**
- **避免不同 skill 重複描述同一套流程**
- **把 ChatGPT 圖片下載流程獨立成專門 skill**
- **讓 README 與實際 repo 結構一致**

## 技能邊界

### `control-gui-setting`
處理：
- browser 啟動失敗
- `$DISPLAY` / `WAYLAND_DISPLAY` / `DBUS_SESSION_BUS_ADDRESS` 傳遞問題
- systemd --user 環境未繼承 GUI session
- OpenClaw managed browser 啟動與 tool exposure 判斷

不處理：
- ChatGPT 圖片另存失敗
- Wayland 全桌面注入與截圖權限調查

### `desktop-control-wayland`
處理：
- Wayland 桌面控制能力檢查
- `ydotoold` / `ydotool` 注入鏈
- portal / screenshot / remote desktop capability

不處理：
- browser 啟動環境修復
- ChatGPT 圖片下載流程

### `chatgpt-image-download`
處理：
- ChatGPT 圖片已生成，但 Download / Save 無法落地
- 直接抓圖網址遭遇 403
- 使用 `openclaw browser waitfordownload` 從登入中的瀏覽器 session 可靠下載圖片

不處理：
- Linux GUI browser 啟動修復
- 通用 Wayland 桌面控制

## 結構

```text
skills/
  chatgpt-image-download/
  control-gui-setting/
  desktop-control-wayland/
```

## 維護原則

未來新增 skill 時，建議維持：

- 名稱清楚
- 邊界單一
- SKILL.md 保持精簡
- 細節放到 `references/`
- 打包檔與來源內容同步更新
