"""STDD batch CLI — lightweight change batch management (V2.9)."""

import argparse
from datetime import datetime
from pathlib import Path


def _get_batches_dir(project_root: Path) -> Path:
    """Get _batch directory path."""
    return project_root / "changes" / "_batch"


def _find_open_batch(project_root: Path) -> Path:
    """Find the currently open (unclosed) batch directory."""
    import yaml
    batches_dir = _get_batches_dir(project_root)
    if not batches_dir.is_dir():
        return None

    for batch_dir in sorted(batches_dir.iterdir(), reverse=True):
        if not batch_dir.is_dir():
            continue
        stdd_yaml = batch_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
            if data and not data.get("closed_at"):
                return batch_dir
    return None


def _create_batch(project_root: Path, strategy: str = "monthly") -> Path:
    """Create a new batch directory."""
    import yaml
    now = datetime.now()
    if strategy == "weekly":
        iso = now.isocalendar()
        batch_id = f"{now.year}-W{iso.week:02d}-{now.strftime('%m%d')}"
    elif strategy == "count_based":
        batches_dir = _get_batches_dir(project_root)
        batches_dir.mkdir(parents=True, exist_ok=True)
        existing = [d for d in batches_dir.iterdir() if d.is_dir() and d.name.startswith("batch-")]
        batch_id = f"batch-{len(existing) + 1:03d}"
    else:  # monthly (default)
        batch_id = now.strftime("%Y-%m-%d")

    batch_dir = _get_batches_dir(project_root) / batch_id

    # Handle same-day collision
    if batch_dir.exists():
        batch_id = now.strftime("%Y-%m-%d-%H")
        batch_dir = _get_batches_dir(project_root) / batch_id

    batch_dir.mkdir(parents=True, exist_ok=True)
    (batch_dir / "items").mkdir(exist_ok=True)

    stdd_yaml = batch_dir / ".stdd.yaml"
    stdd_yaml.write_text(yaml.dump({
        "mode": "batch",
        "batch_type": strategy,
        "batch_id": batch_id,
        "created_at": now.strftime("%Y-%m-%d"),
        "closed_at": None,
        "max_items": 20,
        "items": [],
    }, allow_unicode=True, default_flow_style=False), encoding="utf-8")

    return batch_dir


def _close_batch(batch_dir: Path) -> None:
    """Close a batch and generate archive-summary.md."""
    import yaml
    now = datetime.now().isoformat()

    stdd_yaml = batch_dir / ".stdd.yaml"
    data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8")) if stdd_yaml.exists() else {}
    data["closed_at"] = now
    stdd_yaml.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")

    # Generate summary
    items = data.get("items", [])
    lines = [f"# Batch {batch_dir.name} — 归档摘要", ""]
    lines.append(f"- 闭合时间: {now}")
    lines.append(f"- 变更数量: {len(items)}")
    lines.append(f"- 批次策略: {data.get('batch_type', 'monthly')}")
    lines.append("")
    lines.append("## 变更列表")
    lines.append("")
    for item in items:
        lines.append(f"- {item}")
    lines.append("")

    (batch_dir / "archive-summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ 批次 {batch_dir.name} 已闭合 ({len(items)} 项)")


def _cmd_batch_status(project_root: Path) -> None:
    """Show current batch status."""
    batch = _find_open_batch(project_root)
    if batch is None:
        print("  当前无打开的批次")
        return

    import yaml
    data = yaml.safe_load((batch / ".stdd.yaml").read_text(encoding="utf-8"))
    items = data.get("items", [])
    print(f"  批次: {batch.name}")
    print(f"  策略: {data.get('batch_type', 'monthly')}")
    print(f"  创建: {data.get('created_at', '?')}")
    print(f"  变更数: {len(items)}")
    if items:
        for i, item in enumerate(items, 1):
            print(f"    {i}. {item}")


def _cmd_batch_list(project_root: Path) -> None:
    """List all batch directories."""
    batches_dir = _get_batches_dir(project_root)
    if not batches_dir.is_dir():
        print("  无批次目录")
        return

    import yaml
    batches = sorted(
        [d for d in batches_dir.iterdir() if d.is_dir()],
        key=lambda d: d.name, reverse=True,
    )
    if not batches:
        print("  无批次")
        return

    print(f"  批次列表 ({len(batches)}):")
    for b in batches:
        stdd_yaml = b / ".stdd.yaml"
        status = "?"
        if stdd_yaml.exists():
            data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
            if data.get("closed_at"):
                status = "已闭合"
            else:
                status = "进行中"
        print(f"    {b.name}  [{status}]")


def _cmd_batch_close(project_root: Path) -> None:
    """Close the current open batch."""
    batch = _find_open_batch(project_root)
    if batch is None:
        print("  当前无打开的批次可闭合")
        return
    _close_batch(batch)


def cmd_batch(args: argparse.Namespace) -> None:
    """Entry point for batch command."""
    project_root = Path.cwd()
    action = getattr(args, "action", "status")

    if action == "list":
        _cmd_batch_list(project_root)
    elif action == "close":
        _cmd_batch_close(project_root)
    else:  # status
        _cmd_batch_status(project_root)
