"""stdd gate — CLI and file-token based Gate confirmation (V2.5)."""

import argparse
import sys
from pathlib import Path
from datetime import datetime

import yaml


VALID_GATES = [1, 2, 3]
GATE_PHASE_KEY = {
    1: ("understand", "phases", "understand", "confirmed_at"),
    2: ("spec", "phases", "spec", "confirmed_at"),
    3: ("verify", "phases", "verify", "confirmed_at"),
}


def _find_change_dir(name: str | None, project_root: Path) -> Path | None:
    changes_dir = project_root / "changes"
    if not changes_dir.exists():
        return None
    if name:
        return changes_dir / name
    dirs = sorted(changes_dir.iterdir(), key=lambda d: d.stat().st_mtime, reverse=True)
    return dirs[0] if dirs else None


def _check_gate_order(gate_num: int, change_dir: Path) -> tuple[bool, str]:
    """Check that previous gates are confirmed before confirming gate_num."""
    state_file = change_dir / ".stdd.yaml"
    if not state_file.exists():
        return False, f".stdd.yaml not found in {change_dir}"

    data = yaml.safe_load(state_file.read_text(encoding="utf-8")) or {}
    phases = data.get("phases", {})

    for g in range(1, gate_num):
        prev_label, *prev_path = GATE_PHASE_KEY[g]
        val = phases
        for key in prev_path:
            val = val.get(key) if isinstance(val, dict) else None
        if not val:
            return False, f"Gate {gate_num} cannot be confirmed: Gate {g} ({prev_label}) is not yet confirmed"

    return True, ""


def _check_file_token(gate_num: int, change_dir: Path) -> bool:
    """Check if GATE<N>_APPROVED file token exists."""
    token_file = change_dir / f"GATE{gate_num}_APPROVED"
    return token_file.exists()


def _confirm_gate(gate_num: int, change_dir: Path) -> str:
    """Write confirmed_at to .stdd.yaml for the given gate.

    Returns the confirmation timestamp or error message.
    """
    state_file = change_dir / ".stdd.yaml"
    data = yaml.safe_load(state_file.read_text(encoding="utf-8")) or {}

    label, section, phase_key, field = GATE_PHASE_KEY[gate_num]
    phases = data.setdefault("phases", {})
    phase_data = phases.setdefault(phase_key, {})

    existing = phase_data.get(field)
    if existing:
        return f"Gate {gate_num} already confirmed at {existing}"

    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    phase_data[field] = timestamp
    data["phases"][phase_key]["status"] = "completed"

    state_file.write_text(
        yaml.dump(data, allow_unicode=True, default_flow_style=False),
        encoding="utf-8"
    )
    return f"Gate {gate_num} confirmed for change {change_dir.name}"


def _read_gates_config(project_root: Path) -> dict:
    """Read gates.yaml config with defaults."""
    config_path = project_root / ".stdd" / "config.d" / "gates.yaml"
    if not config_path.exists():
        return {"confirmation": {"channels": ["dialog", "file_token", "cli"]}}
    return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}


def cmd_gate(args: argparse.Namespace) -> None:
    """CLI entry: stdd gate approve <change-name> --gate <N>."""
    project_root = Path.cwd()

    subcommand = getattr(args, "subcommand", "approve")
    if subcommand != "approve":
        print(f"  Unknown subcommand: {subcommand}. Use: approve")
        sys.exit(1)

    gate_num = getattr(args, "gate", None)
    if gate_num is None or gate_num not in VALID_GATES:
        print(f"  Invalid gate number: {gate_num}. Valid gates: {', '.join(str(g) for g in VALID_GATES)}")
        sys.exit(1)

    change_dir = _find_change_dir(getattr(args, "name", None), project_root)
    if change_dir is None:
        print("  No change found.")
        sys.exit(1)

    # Check if file token already confirms this gate
    if _check_file_token(gate_num, change_dir):
        # File token exists — sync it to .stdd.yaml if not already
        state_file = change_dir / ".stdd.yaml"
        data = yaml.safe_load(state_file.read_text(encoding="utf-8")) or {}
        label, _, phase_key, field = GATE_PHASE_KEY[gate_num]
        phase_data = data.get("phases", {}).get(phase_key, {})
        if not phase_data.get(field):
            _confirm_gate(gate_num, change_dir)
            print(f"  Gate {gate_num} confirmed (via file token).")
            return
        else:
            print(f"  Gate {gate_num} already confirmed at {phase_data[field]}")
            return

    # Validate gate order
    valid, err = _check_gate_order(gate_num, change_dir)
    if not valid:
        print(f"  {err}")
        sys.exit(1)

    result = _confirm_gate(gate_num, change_dir)
    print(f"  {result}")
