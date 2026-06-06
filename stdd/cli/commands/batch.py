"""STDD batch CLI — lightweight change batch management (V2.9.3).

Batch mode solves the "N micro-changes" problem during debugging/hotfix
sessions. Instead of creating a separate change for each small fix, the
user opens a batch, makes all related edits (guard allows them), adds
each fix as an item, then closes and archives a single batch record.

V2.9.3: batch open now validates description scope against guard's
classifier. Descriptions signaling large changes (重构/架构/新模块)
are rejected with a suggestion to use full STDD.

Usage:
    stdd batch open "修复界面展示bug"     # opens a batch
    stdd batch add "fix: fees 展示为负值" # adds item to current batch
    stdd batch close                      # closes the batch
    stdd batch archive                    # archives to archive/
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

# V2.9.3: Import scope classifier from guard
try:
    from stdd.cli.commands.guard import _classify_description, _SCOPE_LARGE, _SCOPE_MEDIUM
except ImportError:
    # Fallback: guard module not importable (shouldn't happen but be safe)
    def _classify_description(text: str) -> str:
        return "micro"

    _SCOPE_LARGE = "large"
    _SCOPE_MEDIUM = "medium"


def _get_batches_dir(project_root: Path) -> Path:
    """Get _batch directory path."""
    return project_root / "changes" / "_batch"


def _find_open_batch(project_root: Path) -> Path:
    """Find the currently open (unclosed) batch directory."""
    import yaml
    batches_dir = _get_batches_dir(project_root)
    if not batches_dir.is_dir():
        return None

    for batch_dir in sorted(
        [d for d in batches_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    ):
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
        batch_id = now.strftime("%Y-%m-%d-%H%M")
        batch_dir = _get_batches_dir(project_root) / batch_id

    batch_dir.mkdir(parents=True, exist_ok=True)
    (batch_dir / "items").mkdir(exist_ok=True)

    stdd_yaml = batch_dir / ".stdd.yaml"
    stdd_yaml.write_text(yaml.dump({
        "mode": "batch",
        "batch_type": strategy,
        "batch_id": batch_id,
        "description": "",
        "created_at": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "closed_at": None,
        "max_items": 5,
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
    desc = data.get("description", "")
    items = data.get("items", [])
    lines = [f"# Batch {batch_dir.name} — 归档摘要", ""]
    if desc:
        lines.append(f"**描述:** {desc}")
        lines.append("")
    lines.append(f"- 闭合时间: {now}")
    lines.append(f"- 变更数量: {len(items)}")
    lines.append(f"- 批次策略: {data.get('batch_type', 'monthly')}")
    lines.append("")
    lines.append("## 变更列表")
    lines.append("")
    for item in items:
        timestamp = item.get("added_at", "")
        description = item.get("description", str(item))
        lines.append(f"- [{timestamp}] {description}")
    lines.append("")

    (batch_dir / "archive-summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ 批次 {batch_dir.name} 已闭合 ({len(items)} 项)")


# ------- new commands (V2.9.3) -------

def _cmd_batch_open(project_root: Path, description: str = "", strategy: str = "monthly") -> None:
    """Open a new batch. Validates scope before opening.

    V2.9.3: Scope validation. If the description signals a large change,
    the batch is rejected and full STDD is recommended.
    """
    # V2.9.3: Validate scope
    if description:
        scope = _classify_description(description)
        if scope == _SCOPE_LARGE:
            print(f"  🚫 batch 不适合大型变更。")
            print(f"     描述 '{description}' 被判定为 {scope} 级别。")
            print(f"     请用 full STDD 流程:")
            print(f"       /stdd-understand")
            return
        if scope == _SCOPE_MEDIUM:
            print(f"  ⚠️  描述 '{description}' 看起来是中等规模变更。")
            print(f"     batch 适合微修复 (<5 文件, <100 行)。")
            print(f"     如果确认只用 batch，请用更小的描述重新 open。")
            print(f"     如果是较大改动，建议: /stdd-understand")
            return

    # V2.9.4: Warn if an active STDD change exists (batch should not replace full flow)
    import yaml as _yaml
    changes_dir = project_root / "changes"
    if changes_dir.is_dir():
        for cd in sorted(
            [d for d in changes_dir.iterdir() if d.is_dir() and d.name != "_batch"],
            key=lambda d: d.stat().st_mtime, reverse=True,
        ):
            stdd_yaml = cd / ".stdd.yaml"
            if stdd_yaml.exists():
                cd_data = _yaml.safe_load(stdd_yaml.read_text(encoding="utf-8")) or {}
                phase = cd_data.get("current_phase") or cd_data.get("phase", "")
                if phase in ("build", "verify") and cd_data.get("status") == "active":
                    print(f"  ⚠️  检测到进行中的 change: {cd.name} (phase: {phase})")
                    print(f"     建议在此 change 中完成修改，而非单独开 batch。")
                    print(f"     继续创建 batch 请确认。")
                    break

    # Close existing open batch if any
    existing = _find_open_batch(project_root)
    if existing:
        print(f"  已有打开批次 {existing.name}，先闭合...")
        _close_batch(existing)

    batch_dir = _create_batch(project_root, strategy)

    if description:
        import yaml
        stdd_yaml = batch_dir / ".stdd.yaml"
        data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
        data["description"] = description
        stdd_yaml.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")

    print(f"  ✅ 批次已打开: {batch_dir.name}")
    if description:
        print(f"     范围判定: {_classify_description(description)}")
        print(f"     {description}")
    print(f"  💡 现在可以直接编辑文件，Guard 已放行。")
    print(f"     用 'stdd batch add <描述>' 记录每次修复")
    print(f"     完成后 'stdd batch close' 闭合批次")


def _cmd_batch_add(project_root: Path, description: str) -> None:
    """Add an item to the current open batch.

    V2.9.4: Refuses if >3 files have been modified since batch opened,
    suggesting upgrade to a full STDD change instead.
    """
    batch = _find_open_batch(project_root)
    if batch is None:
        print("  当前无打开的批次。请先 'stdd batch open \"描述\"'")
        return

    import yaml
    import subprocess
    stdd_yaml = batch / ".stdd.yaml"
    data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))

    # V2.9.4: Check git diff scope — refuse if too many files changed
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=str(project_root), timeout=5,
        )
        if result.returncode == 0:
            changed = [f for f in result.stdout.strip().split("\n") if f]
            if len(changed) > 3:
                print(f"  🚫 已修改 {len(changed)} 个文件，超出 batch 适用范围。")
                print(f"     batch 适合 ≤3 个文件的微修复。")
                print(f"     请用 'stdd new <name>' 创建 change 走完整 STDD 流程。")
                return
    except Exception:
        pass  # git not available — skip check

    items = data.get("items", [])
    max_items = data.get("max_items", 5)
    if len(items) >= max_items:
        print(f"  批次已满 ({max_items} 项)，请升级为 change 或先 close 再 open 新批次。")
        return

    items.append({
        "description": description,
        "added_at": datetime.now().isoformat(),
    })
    data["items"] = items
    stdd_yaml.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")

    print(f"  ✅ [{len(items)}/{max_items}] {description}")


def _cmd_batch_archive(project_root: Path) -> None:
    """Close batch (if open) and archive it to archive/."""
    import yaml

    batch = _find_open_batch(project_root)
    if batch is None:
        # Try to find the most recent closed batch to archive
        batches_dir = _get_batches_dir(project_root)
        if not batches_dir.is_dir():
            print("  无批次可归档")
            return

        closed_batches = []
        for d in batches_dir.iterdir():
            if not d.is_dir():
                continue
            stdd_yaml = d / ".stdd.yaml"
            if stdd_yaml.exists():
                data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
                if data and data.get("closed_at"):
                    closed_batches.append(d)
        if not closed_batches:
            print("  无已闭合批次可归档。请先 'stdd batch open' 创建批次。")
            return
        batch = max(closed_batches, key=lambda d: d.stat().st_mtime)
        print(f"  选取最近闭合批次: {batch.name}")
    else:
        # Close it first
        _close_batch(batch)

    # Move to archive
    archive_dir = project_root / "archive"
    archive_dir.mkdir(exist_ok=True)

    dest = archive_dir / batch.name
    if dest.exists():
        # Add suffix to avoid collision
        dest = archive_dir / f"{batch.name}-{datetime.now().strftime('%H%M%S')}"

    shutil.move(str(batch), str(dest))

    # Generate an archive index entry
    import yaml
    stdd_yaml = dest / ".stdd.yaml"
    items_count = 0
    if stdd_yaml.exists():
        data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
        items_count = len(data.get("items", []))

    print(f"  ✅ 批次已归档: archive/{dest.name}")
    print(f"     包含 {items_count} 项变更")


# ------- existing commands -------

def _cmd_batch_status(project_root: Path) -> None:
    """Show current batch status."""
    batch = _find_open_batch(project_root)
    if batch is None:
        print("  当前无打开的批次")
        print("  用 'stdd batch open \"描述\"' 开始一个调试/修复批次")
        return

    import yaml
    data = yaml.safe_load((batch / ".stdd.yaml").read_text(encoding="utf-8"))
    items = data.get("items", [])
    desc = data.get("description", "")
    print(f"  批次: {batch.name}")
    if desc:
        print(f"  描述: {desc}")
    print(f"  策略: {data.get('batch_type', 'monthly')}")
    print(f"  创建: {data.get('created_at', '?')}")
    print(f"  变更数: {len(items)}/{data.get('max_items', 20)}")
    if items:
        for i, item in enumerate(items, 1):
            ts = item.get("added_at", "")[:16] if isinstance(item, dict) else ""
            desc_text = item.get("description", str(item)) if isinstance(item, dict) else str(item)
            print(f"    {i}. [{ts}] {desc_text}")


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
        desc = ""
        n_items = 0
        status = "?"
        if stdd_yaml.exists():
            data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
            if data.get("closed_at"):
                status = "已闭合"
            else:
                status = "进行中"
            desc = data.get("description", "")
            n_items = len(data.get("items", []))
        print(f"    {b.name}  [{status}] ({n_items}项) {desc[:40]}")


def _cmd_batch_close(project_root: Path, force: bool = False) -> None:
    """Close the current open batch.

    V2.9.4: Warns if batch has ≤1 item and has been open <1 hour, unless --force.
    """
    import yaml
    batch = _find_open_batch(project_root)
    if batch is None:
        print("  当前无打开的批次可闭合")
        return

    # V2.9.4: Lightweight guard — warn if closing a near-empty young batch
    if not force:
        stdd_yaml = batch / ".stdd.yaml"
        if stdd_yaml.exists():
            data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
            items = data.get("items", [])
            created_str = data.get("created_at", "")
            if len(items) <= 1 and created_str:
                try:
                    created = datetime.fromisoformat(created_str)
                    age_minutes = (datetime.now() - created).total_seconds() / 60
                    if age_minutes < 60:
                        print(f"  ⚠️  批次仅 {len(items)} 项、才开了 {int(age_minutes)} 分钟。")
                        print(f"     batch 适合收纳多个小修复，不建议频繁开关。")
                        print(f"     如果确认要闭合，请用 'stdd batch close --force'。")
                        return
                except ValueError:
                    pass

    _close_batch(batch)


# ------- dispatcher -------

def cmd_batch(args: argparse.Namespace) -> None:
    """Entry point for batch command."""
    project_root = Path.cwd()
    action = getattr(args, "action", "status")

    if action == "open":
        description = getattr(args, "description", "") or ""
        strategy = getattr(args, "strategy", "monthly") or "monthly"
        _cmd_batch_open(project_root, description, strategy)
    elif action == "add":
        description = getattr(args, "description", None)
        if not description:
            print("  用法: stdd batch add \"修复描述\"")
            return
        _cmd_batch_add(project_root, description)
    elif action == "archive":
        _cmd_batch_archive(project_root)
    elif action == "close":
        _cmd_batch_close(project_root, force=getattr(args, "force", False))
    elif action == "list":
        _cmd_batch_list(project_root)
    else:  # status
        _cmd_batch_status(project_root)
