#!/usr/bin/env python3
import json
from pathlib import Path

import pyatspi

OUT = Path('/tmp/menu-probe/atspi-dump.json')
OUT.parent.mkdir(parents=True, exist_ok=True)

ROLE_NAMES = {}
for name in dir(pyatspi):
    if name.startswith('ROLE_'):
        value = getattr(pyatspi, name)
        if isinstance(value, int):
            ROLE_NAMES[value] = name


def role_name(node):
    try:
        return ROLE_NAMES.get(node.getRole(), str(node.getRole()))
    except Exception:
        return 'ROLE_ERROR'


def iface_actions(node):
    try:
        a = node.queryAction()
        names = []
        for i in range(a.nActions):
            try:
                names.append(a.getName(i))
            except Exception:
                names.append(f'index:{i}')
        return names
    except Exception:
        return []


def extents(node):
    try:
        c = node.queryComponent()
        e = c.getExtents(pyatspi.DESKTOP_COORDS)
        return {'x': e.x, 'y': e.y, 'w': e.width, 'h': e.height}
    except Exception:
        return None


def dump_node(node, depth=0, max_depth=3):
    item = {
        'name': getattr(node, 'name', None),
        'role': role_name(node),
        'actions': iface_actions(node),
        'extents': extents(node),
        'childCount': getattr(node, 'childCount', 0),
    }
    if depth < max_depth:
        children = []
        try:
            for i in range(node.childCount):
                try:
                    children.append(dump_node(node.getChildAtIndex(i), depth + 1, max_depth))
                except Exception as e:
                    children.append({'error': str(e)})
        except Exception:
            pass
        item['children'] = children
    return item


def interesting(node):
    try:
        rn = role_name(node)
        nm = (getattr(node, 'name', '') or '').strip()
        if 'MENU' in rn:
            return True
        if nm and ('複製' in nm or 'copy' in nm.lower()):
            return True
        return False
    except Exception:
        return False


def walk(node, hits, path, depth=0, max_depth=6):
    try:
        if interesting(node):
            hits.append({
                'path': path,
                'node': dump_node(node, 0, 2),
            })
        if depth >= max_depth:
            return
        for i in range(node.childCount):
            child = node.getChildAtIndex(i)
            walk(child, hits, path + [i], depth + 1, max_depth)
    except Exception:
        return


def main():
    desktop = pyatspi.Registry.getDesktop(0)
    apps = []
    hits = []
    named_copy_hits = []
    menu_hits = []
    for i in range(desktop.childCount):
        app = desktop.getChildAtIndex(i)
        app_item = {
            'index': i,
            'name': getattr(app, 'name', None),
            'role': role_name(app),
            'childCount': getattr(app, 'childCount', 0),
        }
        apps.append(app_item)
        walk(app, hits, [i], 0, 6)
    for hit in hits:
        node = hit['node']
        role = node.get('role')
        name = (node.get('name') or '').strip()
        if 'MENU' in (role or ''):
            menu_hits.append({
                'path': hit['path'],
                'role': role,
                'name': name,
                'extents': node.get('extents'),
                'actions': node.get('actions'),
            })
        if name and ('複製' in name or 'copy' in name.lower()):
            named_copy_hits.append({
                'path': hit['path'],
                'role': role,
                'name': name,
                'extents': node.get('extents'),
                'actions': node.get('actions'),
            })
    out = {
        'apps': apps,
        'hits': hits,
        'menu_hits': menu_hits,
        'named_copy_hits': named_copy_hits,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(str(OUT))
    print(json.dumps({
        'appCount': len(apps),
        'hitCount': len(hits),
        'menuHitCount': len(menu_hits),
        'namedCopyHitCount': len(named_copy_hits),
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
