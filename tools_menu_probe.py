#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

OUT_DIR = Path('/tmp/menu-probe')
OUT_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'cmd': cmd,
        'returncode': p.returncode,
        'stdout': p.stdout,
        'stderr': p.stderr,
    }


def gnome_shell_screenshot(method, *args):
    cmd = [
        'gdbus', 'call', '--session',
        '--dest', 'org.gnome.Shell.Screenshot',
        '--object-path', '/org/gnome/Shell/Screenshot',
        '--method', f'org.gnome.Shell.Screenshot.{method}',
    ] + [str(a) for a in args]
    return run(cmd)


def parse_call_success(stdout: str):
    s = stdout.strip()
    return {'raw': s, 'success': 'true' in s.lower()}


def capture_fullscreen(name: str):
    path = OUT_DIR / name
    res = gnome_shell_screenshot('Screenshot', 'false', 'false', str(path))
    meta = parse_call_success(res['stdout'])
    meta['path'] = str(path)
    meta['exists'] = path.exists()
    meta['size'] = path.stat().st_size if path.exists() else None
    return {'call': res, 'meta': meta}


def capture_window(name: str):
    path = OUT_DIR / name
    res = gnome_shell_screenshot('ScreenshotWindow', 'true', 'false', 'false', str(path))
    meta = parse_call_success(res['stdout'])
    meta['path'] = str(path)
    meta['exists'] = path.exists()
    meta['size'] = path.stat().st_size if path.exists() else None
    return {'call': res, 'meta': meta}


def capture_area(name: str, x: int, y: int, w: int, h: int):
    path = OUT_DIR / name
    res = gnome_shell_screenshot('ScreenshotArea', x, y, w, h, 'false', str(path))
    meta = parse_call_success(res['stdout'])
    meta.update({'path': str(path), 'x': x, 'y': y, 'w': w, 'h': h})
    meta['exists'] = path.exists()
    meta['size'] = path.stat().st_size if path.exists() else None
    return {'call': res, 'meta': meta}


def ocr_image(path: str):
    txt_base = str(Path(path).with_suffix(''))
    res = run(['tesseract', path, txt_base, '-l', 'chi_tra+eng'])
    txt_path = Path(txt_base + '.txt')
    text = txt_path.read_text(errors='replace') if txt_path.exists() else ''
    return {
        'call': res,
        'text_path': str(txt_path),
        'text_exists': txt_path.exists(),
        'text': text,
    }


def main():
    report = {
        'fullscreen': capture_fullscreen('before.png'),
        'window': capture_window('window.png'),
        'area': capture_area('area.png', 100, 100, 800, 600),
    }

    if report['fullscreen']['meta']['exists']:
        report['fullscreen_ocr'] = ocr_image(report['fullscreen']['meta']['path'])

    out = OUT_DIR / 'report.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(str(out))


if __name__ == '__main__':
    main()
