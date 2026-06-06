"""STDD guard CLI — intelligent enforcement gate (V2.9.4).

V2.9.4: Phase integrity checks prevent bypass via manual YAML editing.
Guard now verifies that the current phase was legitimately reached
(previous phases completed, gates confirmed) before allowing edits.
Also supports task_type-aware phase permissions (documentation tasks
need to edit during spec/slice phases).
"""

import sys
import argparse
from pathlib import Path

_PHASE_ORDER = ["understand", "spec", "slice", "build", "verify", "deliver"]
_GATE_PHASES = {"understand", "spec", "verify"}  # phases that require gate confirmation

# V2.9.3: Phases where code editing is permitted (task_type-aware in V2.9.4)
_EDITABLE_PHASES_BY_TYPE = {
    "code": {"build", "verify"},
    "documentation": {"understand", "spec", "slice", "build", "verify"},
    "configuration": {"understand", "spec", "slice", "build", "verify"},
    "data-migration": {"build", "verify"},
    "dependency-upgrade": {"build", "verify"},
}

# Fallback for backward compatibility
_EDITABLE_PHASES = {"build", "verify"}

# V2.9.3: Scope classification
#    micro  → batch is ideal
#    small  → batch ok, but monitor
#    medium → batch not recommended, suggest full STDD
#    large  → batch blocked, force full STDD
_SCOPE_MICRO = "micro"
_SCOPE_SMALL = "small"
_SCOPE_MEDIUM = "medium"
_SCOPE_LARGE = "large"

# Batch limits
_BATCH_MAX_FILES = 5       # warn if exceeded
_BATCH_MAX_FILES_HARD = 10  # block if exceeded (batch not suitable)
_BATCH_MAX_HOURS = 2        # warn if batch open longer

# Keyword signals for scope classification (V2.9.3)
# Scores: micro=1, small=2, medium=5, large=10
# Thresholds: >=20 large, >=10 medium, >=3 small, <3 micro
_MICRO_SIGNALS = [
    "修复", "fix", "bug", "热修", "hotfix", "小改",
    "typo", "改个", "补丁", "patch", "修一下", "改一下",
    "快速", "quick", "改个", "小调整",
]
_SMALL_SIGNALS = [
    "调整", "优化", "改进", "更新", "ui", "界面",
    "improve", "tweak", "update", "adjust", "enhance",
    "日志", "格式", "展示", "显示", "配置", "清理",
]
_MEDIUM_SIGNALS = [
    "重构", "refactor", "改版", "迁移", "替换", "改造",
    "feature", "添加", "增加", "新增", "模块",
    "功能", "逻辑", "数据处理", "性能",
]
_LARGE_SIGNALS = [
    "重写", "rewrite", "架构", "architecture",
    "大改", "overhaul", "子系统", "system",
    "新模块", "新增模块", "新功能",
    "api", "接口", "集成", "integration",
    "引擎", "engine", "平台", "platform",
]


def _classify_description(text: str) -> str:
    """Classify a change description into scope level.

    Returns one of: _SCOPE_MICRO, _SCOPE_SMALL, _SCOPE_MEDIUM, _SCOPE_LARGE

    Scoring: micro=1, small=2, medium=5, large=10
    Thresholds: >=20 large, >=10 medium, >=3 small, <3 micro
    """
    lower = text.lower()
    score = 0

    for kw in _MICRO_SIGNALS:
        if kw in lower:
            score += 1
    for kw in _SMALL_SIGNALS:
        if kw in lower:
            score += 2
    for kw in _MEDIUM_SIGNALS:
        if kw in lower:
            score += 5
    for kw in _LARGE_SIGNALS:
        if kw in lower:
            score += 10

    if score >= 20:
        return _SCOPE_LARGE
    elif score >= 10:
        return _SCOPE_MEDIUM
    elif score >= 3:
        return _SCOPE_SMALL
    else:
        return _SCOPE_MICRO


def _count_changed_files(project_root: Path) -> int:
    """Count files changed in the working tree (untracked not counted)."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=str(project_root),
            timeout=5,
        )
        if result.returncode == 0:
            files = [f for f in result.stdout.strip().split("\n") if f]
            return len(files)
    except Exception:
        pass
    return 0


def _count_batch_files_so_far(project_root: Path) -> int:
    """Estimate files touched in current batch by counting tracked changes."""
    return _count_changed_files(project_root)


def _find_open_batch(project_root: Path):
    """Find the currently open (unclosed) batch. Returns (batch_dir, batch_data) or (None, None)."""
    import yaml as _yaml
    batches_dir = project_root / "changes" / "_batch"
    if not batches_dir.is_dir():
        return None, None

    for batch_dir in sorted(
        [d for d in batches_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    ):
        stdd_yaml = batch_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            data = _yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
            if data and not data.get("closed_at"):
                return batch_dir, data
    return None, None


def _find_active_change(project_root: Path) -> tuple:
    """Find the most recent active change. Returns (change_dir, phase) or (None, None)."""
    changes_dir = project_root / "changes"
    if not changes_dir.is_dir():
        return None, None

    for change_dir in sorted(
        [d for d in changes_dir.iterdir() if d.is_dir() and d.name != "_batch"],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    ):
        stdd_yaml = change_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            import yaml
            data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
            if data:
                status = data.get("status", "")
                phase = data.get("current_phase") or data.get("phase", "")
                if status in ("active", "in_progress", "pending") or phase in (
                    "understand", "spec", "slice", "build", "verify"
                ):
                    return change_dir, phase
    return None, None


def _check_phase_integrity(data: dict, current_phase: str) -> tuple:
    """Check that the current phase was legitimately reached.

    Returns (ok: bool, reason: str).
    A phase is legitimate if all previous phases have status=="completed"
    AND all required gate phases have confirmed_at timestamps.
    """
    if current_phase not in _PHASE_ORDER:
        return False, f"Unknown phase: {current_phase}"

    idx = _PHASE_ORDER.index(current_phase)
    phases = data.get("phases", {})

    # Check all previous phases are completed
    for i in range(idx):
        prev = _PHASE_ORDER[i]
        prev_status = phases.get(prev, {}).get("status", "pending")
        if prev_status != "completed":
            return False, (
                f"Phase 完整性异常：当前 phase='{current_phase}' 但 "
                f"Phase '{prev}' 状态为 '{prev_status}'（应为 'completed'）。"
                " 请用 'stdd phase advance' 逐步推进，不要手动修改 .stdd.yaml。"
            )

    # Check required gate phases have confirmed_at
    for gp in _GATE_PHASES:
        gp_idx = _PHASE_ORDER.index(gp)
        if gp_idx < idx:  # this gate should have been passed
            gp_data = phases.get(gp, {})
            if not gp_data.get("confirmed_at"):
                return False, (
                    f"Gate 缺失：Phase '{gp}' 经过了 Gate "
                    f"({['Gate 1','Gate 2','Gate 3'][['understand','spec','verify'].index(gp)]})"
                    " 但未确认 (confirmed_at 为空)。"
                    " 请先完成 Gate 确认。"
                )

    return True, ""


# ---- V2.9.3: Scope assessment & recommendation ----

def _assess_and_recommend(project_root: Path,
                          batch_dir=None,
                          batch_data: dict = None,
                          enforce: bool = True) -> dict:
    """Assess current change scope and return recommendation.

    Returns dict with keys:
        allow: bool          -- whether to allow the edit
        mode: str            -- recommended mode (batch / full-stdd)
        scope: str           -- classified scope level
        reason: str          -- human-readable explanation
        file_count: int      -- files changed so far
    """
    file_count = _count_changed_files(project_root)
    result = {
        "allow": True,
        "mode": "batch",
        "scope": _SCOPE_MICRO,
        "reason": "",
        "file_count": file_count,
    }

    if not enforce:
        result["reason"] = "enforce_stdd disabled"
        return result

    # If we have an open batch, check its description and current state
    if batch_dir and batch_data:
        desc = batch_data.get("description", "")
        desc_scope = _classify_description(desc)
        items = batch_data.get("items", [])

        # File-count based escalation
        if file_count > _BATCH_MAX_FILES_HARD:
            result["allow"] = False
            result["mode"] = "full-stdd"
            result["scope"] = _SCOPE_LARGE
            result["reason"] = (
                f"已修改 {file_count} 个文件，超出 batch 上限 ({_BATCH_MAX_FILES_HARD})。"
                " 请用 'stdd new' 创建 full change，走完整 STDD 流程。"
            )
            return result

        if file_count > _BATCH_MAX_FILES:
            result["scope"] = _SCOPE_MEDIUM
            result["mode"] = "full-stdd"
            # Still allow, but with strong warning
            result["reason"] = (
                f"⚠️  已修改 {file_count} 个文件 (batch 推荐上限 {_BATCH_MAX_FILES})。"
                " 建议转 full STDD: 'stdd new <change-name>'"
            )
            return result

        # Scope based on batch description
        if desc_scope == _SCOPE_LARGE:
            result["allow"] = False
            result["mode"] = "full-stdd"
            result["scope"] = _SCOPE_LARGE
            result["reason"] = (
                f"batch 描述 '{desc}' 判定为大型变更。"
                " 请用 full STDD 流程: /stdd-understand 启动。"
            )
            return result

        if desc_scope == _SCOPE_MEDIUM:
            result["scope"] = _SCOPE_MEDIUM
            result["mode"] = "full-stdd"
            result["reason"] = (
                f"⚠️  batch 描述 '{desc}' 看起来是中大型变更。"
                " batch 适合微修复；建议转为 full STDD。"
                " 继续用 batch 请确保范围可控。"
            )
            # Still allow for medium — warn but don't block
            return result

        # Small/micro — batch is fine
        result["scope"] = desc_scope
        result["mode"] = "batch"
        result["reason"] = f"batch: {batch_dir.name} ({len(items)} items)"
        return result

    # No batch and no active change → assess what's happening
    if file_count > 0:
        if file_count <= 2:
            result["scope"] = _SCOPE_MICRO
            result["reason"] = (
                f"检测到 {file_count} 个文件改动，属于微修复范围。"
                " 用 'stdd batch open \"描述\"' 快速开始。"
            )
        elif file_count <= 5:
            result["scope"] = _SCOPE_SMALL
            result["reason"] = (
                f"检测到 {file_count} 个文件改动。"
                " 微修复用 'stdd batch open \"描述\"'，较大改动用 'stdd new'。"
            )
        else:
            result["scope"] = _SCOPE_MEDIUM
            result["reason"] = (
                f"检测到 {file_count} 个文件改动，建议走 full STDD。"
                " /stdd-understand 启动完整流程。"
            )
    else:
        result["reason"] = (
            "无 active change。微修复用 'stdd batch open \"描述\"'，"
            "新功能/重构用 '/stdd-understand'。"
        )

    result["mode"] = "none"
    return result


# ---- CLI commands ----

def cmd_guard_check(args: argparse.Namespace) -> int:
    """Check if currently in a valid STDD flow.

    V2.9.3: Intelligent classification. Instead of just allow/block,
    suggests the appropriate mode (batch vs full STDD) based on scope.

    Exit codes:
        0 — allowed (batch open, or active change in editable phase)
        2 — blocked (no active flow, or batch exceeded limits)
    """
    project_root = Path.cwd()

    # Check if enforce_stdd is enabled
    enforce = True
    config_file = project_root / ".stdd" / "config.d" / "project.yaml"
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        enforce = config.get("enforce_stdd", True)

    if not enforce:
        return 0

    # find active change
    active_dir, phase = _find_active_change(project_root)

    # Full STDD change: check phase integrity + task_type permissions
    if active_dir:
        stdd_yaml = active_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            import yaml
            change_data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8")) or {}
            task_type = change_data.get("task_type", "code") or "code"

            # V2.9.4: Phase integrity check
            integrity_ok, integrity_reason = _check_phase_integrity(change_data, phase)
            if not integrity_ok:
                if getattr(args, "platform", "cli") == "claude-code":
                    import sys as _sys
                    print(f"  [STDD Guard] 🚫 {integrity_reason}", file=_sys.stderr)
                else:
                    print(f"  [STDD Guard] 🚫 {integrity_reason}")
                return 2

            # V2.9.4: task_type-aware editable phases
            editable = _EDITABLE_PHASES_BY_TYPE.get(task_type, _EDITABLE_PHASES)
            if phase in editable:
                if not getattr(args, "quiet", False):
                    print(f"  [STDD Guard] Active change: {active_dir.name} "
                          f"(phase: {phase}, task: {task_type}) — ✅")
                return 0

    # Check for open batch → intelligent assessment
    batch_dir, batch_data = _find_open_batch(project_root)
    if batch_dir:
        assessment = _assess_and_recommend(
            project_root, batch_dir=batch_dir, batch_data=batch_data, enforce=enforce
        )
        if not assessment["allow"]:
            # Batch exceeded limits — block
            if getattr(args, "platform", "cli") == "claude-code":
                import sys as _sys
                print(f"  [STDD Guard] 🚫 Blocked: {assessment['reason']}", file=_sys.stderr)
            else:
                print(f"  [STDD Guard] 🚫 Blocked: {assessment['reason']}")
            return 2

        if not getattr(args, "quiet", False):
            icon = "⚠️" if assessment["mode"] == "full-stdd" else "✅"
            print(f"  [STDD Guard] {icon} {assessment['reason']}")
        return 0

    # No active flow at all → block with intelligent suggestion
    assessment = _assess_and_recommend(project_root, enforce=enforce)

    # Check for allow_bypass
    allow_bypass = False
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        allow_bypass = config.get("allow_bypass", False)

    strict = getattr(args, "strict", False)
    if allow_bypass and not strict:
        print(f"  [STDD Guard] {assessment['reason']}")
        print("  [STDD Guard] allow_bypass is enabled — allowing anyway.")
        return 0

    # Block with intelligent suggestion
    platform = getattr(args, "platform", "cli")
    if active_dir:
        reason = f"当前 Phase '{phase}' 不允许编辑。只有 Phase 4/5 允许。"
    else:
        reason = assessment["reason"]

    if platform == "claude-code":
        import sys as _sys
        print("  [STDD Guard] ⛔ Blocked — 未进入可编辑流程", file=_sys.stderr)
        print(f"  [STDD Guard] {reason}", file=_sys.stderr)
    else:
        print(f"  [STDD Guard] ⛔ Blocked — {reason}")
    return 2


def cmd_guard_status(args: argparse.Namespace) -> None:
    """Display current STDD guard status with scope assessment."""
    project_root = Path.cwd()
    batch_dir, batch_data = _find_open_batch(project_root)
    active_dir, phase = _find_active_change(project_root)

    config_file = project_root / ".stdd" / "config.d" / "project.yaml"
    enforce = True
    allow_bypass = False
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        enforce = config.get("enforce_stdd", True)
        allow_bypass = config.get("allow_bypass", False)

    # V2.9.3: Intelligent assessment
    assessment = _assess_and_recommend(
        project_root, batch_dir=batch_dir, batch_data=batch_data, enforce=enforce
    )

    task_type = "code"
    editable = (phase in _EDITABLE_PHASES if phase else False) or (batch_dir is not None)
    if active_dir:
        stdd_yaml = active_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            change_data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8")) or {}
            task_type = change_data.get("task_type", "code") or "code"
            editable_phases = _EDITABLE_PHASES_BY_TYPE.get(task_type, _EDITABLE_PHASES)
            editable = phase in editable_phases
            integrity_ok, _ = _check_phase_integrity(change_data, phase)

    print("  STDD Guard Status (V2.9.4 智能门禁):")
    print(f"    enforce_stdd:  {enforce}")
    print(f"    allow_bypass:  {allow_bypass}")
    print(f"    task_type:      {task_type}")
    print(f"    editable phases: {sorted(_EDITABLE_PHASES_BY_TYPE.get(task_type, _EDITABLE_PHASES))}")
    print(f"    changed files:  {assessment['file_count']}")
    print(f"    scope:          {assessment['scope']}")
    print(f"    recommended:    {assessment['mode']}")
    if active_dir and not editable:
        print(f"    phase integrity: {'✅' if integrity_ok else '❌ BYPASS DETECTED'}")

    if batch_dir:
        desc = (batch_data or {}).get("description", "") if batch_data else ""
        items = (batch_data or {}).get("items", []) if batch_data else []
        desc_scope = _classify_description(desc)
        print(f"    open batch:     {batch_dir.name} — ✅ 可编辑")
        print(f"      description:  {desc}")
        print(f"      desc scope:   {desc_scope}")
        print(f"      items:        {len(items)}")
        if assessment["mode"] == "full-stdd" and assessment["allow"]:
            print(f"      ⚠️  {assessment['reason']}")

    if active_dir:
        status = "✅ 可编辑" if editable else "🔒 只读"
        print(f"    active change:  {active_dir.name} (phase: {phase}) — {status}")
    else:
        print(f"    active change:  None — 🔒 只读")


def cmd_guard_init(args: argparse.Namespace) -> None:
    """Initialize guard hooks for the current project."""
    project_root = Path.cwd()
    platform = getattr(args, "platform", "claude-code")

    if platform == "claude-code":
        import json
        settings_file = project_root / ".claude" / "settings.local.json"

        if settings_file.exists():
            settings = json.loads(settings_file.read_text(encoding="utf-8"))
        else:
            settings = {"permissions": {"allow": []}}

        if "hooks" not in settings:
            settings["hooks"] = {}

        if "PreToolUse" not in settings["hooks"]:
            settings["hooks"]["PreToolUse"] = []

        guard_exists = False
        for hook in settings["hooks"]["PreToolUse"]:
            if "stdd guard" in str(hook.get("hooks", [])):
                guard_exists = True
                break

        if not guard_exists:
            settings["hooks"]["PreToolUse"].append({
                "matcher": "Edit|Write",
                "hooks": [{
                    "type": "command",
                    "command": "stdd guard check --platform claude-code"
                }]
            })

        settings_file.parent.mkdir(parents=True, exist_ok=True)
        settings_file.write_text(
            json.dumps(settings, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print("  [STDD Guard] Claude Code PreToolUse hook deployed.")
        print("  [STDD Guard] All Edit/Write operations will be checked.")
    else:
        print(f"  [STDD Guard] Platform '{platform}' not supported for auto-init.")
        print(f"  [STDD Guard] See docs for manual guard configuration.")


def cmd_guard_disable(args: argparse.Namespace) -> None:
    """Temporarily remove the guard hook (reversible with 'enable')."""
    project_root = Path.cwd()
    import json
    settings_file = project_root / ".claude" / "settings.local.json"

    if not settings_file.exists():
        print("  [STDD Guard] No settings.local.json found. Nothing to disable.")
        return

    settings = json.loads(settings_file.read_text(encoding="utf-8"))
    hooks = settings.get("hooks", {}).get("PreToolUse", [])

    removed = False
    new_hooks = []
    for hook in hooks:
        if "stdd guard" in str(hook.get("hooks", [])):
            removed = True
        else:
            new_hooks.append(hook)

    if removed:
        settings["hooks"]["PreToolUse"] = new_hooks
        if not new_hooks:
            del settings["hooks"]["PreToolUse"]
            if not settings["hooks"]:
                del settings["hooks"]
        settings_file.write_text(
            json.dumps(settings, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print("  [STDD Guard] Hook disabled. Run 'stdd guard enable' to re-enable.")
    else:
        print("  [STDD Guard] No guard hook found. Already disabled.")


def cmd_guard_enable(args: argparse.Namespace) -> None:
    """Re-enable the guard hook after disable."""
    cmd_guard_init(args)


def cmd_guard(args: argparse.Namespace) -> None:
    """Entry point for guard command."""
    action = getattr(args, "action", "check")

    if action == "check":
        exit_code = cmd_guard_check(args)
        if exit_code != 0:
            sys.exit(exit_code)
    elif action == "status":
        cmd_guard_status(args)
    elif action == "init":
        cmd_guard_init(args)
    elif action == "disable":
        cmd_guard_disable(args)
    elif action == "enable":
        cmd_guard_enable(args)
    else:
        print(f"  Unknown guard action: {action}")
        sys.exit(1)
