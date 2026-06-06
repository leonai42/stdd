"""STDD phase CLI — advance and check change phase (V2.9.4)."""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import yaml

_PHASE_ORDER = ["understand", "spec", "slice", "build", "verify", "deliver"]
_PHASE_LABELS = {
    "understand": "Phase 1: UNDERSTAND",
    "spec": "Phase 2: SPEC",
    "slice": "Phase 3: SLICE",
    "build": "Phase 4: BUILD",
    "verify": "Phase 5: VERIFY",
    "deliver": "Phase 6: DELIVER",
}


def _find_change(project_root: Path, name: str = None) -> Path:
    """Find change dir by name (most recent if None)."""
    changes_dir = project_root / "changes"
    if not changes_dir.is_dir():
        return None
    if name:
        return changes_dir / name
    candidates = sorted(
        [d for d in changes_dir.iterdir() if d.is_dir() and d.name != "_batch" and (d / ".stdd.yaml").exists()],
        key=lambda d: d.stat().st_mtime, reverse=True,
    )
    return candidates[0] if candidates else None


def cmd_phase(args: argparse.Namespace) -> None:
    """Advance or check change phase."""
    project_root = Path.cwd()
    action = getattr(args, "phase_action", "status")
    change_name = getattr(args, "name", None)

    change_dir = _find_change(project_root, change_name)
    if change_dir is None:
        print("  No change found.")
        sys.exit(1)

    stdd_yaml = change_dir / ".stdd.yaml"
    if not stdd_yaml.exists():
        print(f"  .stdd.yaml not found in {change_dir.name}")
        sys.exit(1)

    data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
    current = data.get("current_phase", "understand")

    if action == "status":
        idx = _PHASE_ORDER.index(current) if current in _PHASE_ORDER else -1
        print(f"  Change: {change_dir.name}")
        print(f"  Current phase: {_PHASE_LABELS.get(current, current)}")
        print(f"  Status: {data.get('phases', {}).get(current, {}).get('status', 'unknown')}")
        print(f"  Mode: {data.get('mode', 'standard')}")
        print(f"  Task type: {data.get('task_type', 'code')}")
        # Show next phase
        if idx >= 0 and idx + 1 < len(_PHASE_ORDER):
            nxt = _PHASE_ORDER[idx + 1]
            print(f"  Next: {_PHASE_LABELS.get(nxt, nxt)}")
        return

    if action == "advance":
        idx = _PHASE_ORDER.index(current) if current in _PHASE_ORDER else -1
        if idx < 0:
            print(f"  Unknown phase: {current}")
            sys.exit(1)
        if idx + 1 >= len(_PHASE_ORDER):
            print(f"  Already at final phase: {_PHASE_LABELS.get(current, current)}")
            sys.exit(0)

        # Mark current phase completed
        phases = data.setdefault("phases", {})
        phases.setdefault(current, {})["status"] = "completed"
        phases.setdefault(current, {})["confirmed_at"] = datetime.now().isoformat()

        # Advance to next
        nxt = _PHASE_ORDER[idx + 1]
        data["current_phase"] = nxt
        phases.setdefault(nxt, {})["status"] = "in_progress"
        data["last_modified"] = datetime.now().isoformat()

        stdd_yaml.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")

        print(f"  {_PHASE_LABELS[current]} → {_PHASE_LABELS[nxt]}")
        print(f"  Change: {change_dir.name}")
        if nxt == "build":
            print(f"  💡 Build phase — Guard 已放行 Edit/Write")

    elif action == "set":
        target = getattr(args, "target_phase", None)
        if not target:
            print("  Usage: stdd phase set <phase>")
            sys.exit(1)
        if target not in _PHASE_ORDER:
            print(f"  Invalid phase: {target}. Valid: {', '.join(_PHASE_ORDER)}")
            sys.exit(1)
        data["current_phase"] = target
        data.setdefault("phases", {}).setdefault(target, {})["status"] = "in_progress"
        data["last_modified"] = datetime.now().isoformat()
        stdd_yaml.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")
        print(f"  Phase set to {_PHASE_LABELS[target]}")
        print(f"  Change: {change_dir.name}")
