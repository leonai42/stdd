from pathlib import Path
from typing import Optional


def find_change_dir(name: Optional[str] = None, project_root: Optional[Path] = None) -> Optional[Path]:
    if project_root is None:
        project_root = Path.cwd()
    changes_dir = project_root / "changes"
    if not changes_dir.exists():
        return None

    if name:
        exact = changes_dir / name
        if exact.exists() and exact.is_dir() and (exact / ".stdd.yaml").exists():
            return exact
        for d in sorted(changes_dir.iterdir(), reverse=True):
            if d.is_dir() and d.name.endswith(name) and (d / ".stdd.yaml").exists():
                from .utils import get_logger
                get_logger().info("📋 匹配到 change: %s", d.name)
                return d
        return None
    else:
        changes = [d for d in changes_dir.iterdir() if d.is_dir() and (d / ".stdd.yaml").exists()]
        if not changes:
            return None
        return sorted(changes, key=lambda d: d.stat().st_mtime, reverse=True)[0]
