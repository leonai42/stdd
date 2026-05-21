import argparse
import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

import yaml


VALID_CATEGORIES = [
    "hallucination",
    "scope_creep",
    "cascading_errors",
    "context_loss",
    "tool_misuse",
    "runtime_deviation",
    "pipeline_break",
    "content_quality",
    "instruction_decay",
    "coverage_vacuum",
    "contract_gap",
]

CATEGORY_LABELS = {
    "hallucination": "(a) 幻觉行为",
    "scope_creep": "(b) 范围蔓延",
    "cascading_errors": "(c) 级联错误",
    "context_loss": "(d) 上下文丢失",
    "tool_misuse": "(e) 工具误用",
    "runtime_deviation": "(f) 运行时行为偏差",
    "pipeline_break": "(g) 管线断链",
    "content_quality": "(h) 内容质量偏差",
    "instruction_decay": "(i) 指令衰减",
    "coverage_vacuum": "(j) 覆盖真空",
    "contract_gap": "(k) 契约断层",
}

SANITIZE_PATTERNS = [
    (re.compile(r"(/[^\s]*?/[^\s]*?\.[a-z]{2,4})"), "<project>/<module>"),
    (re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "<ip-address>"),
    (re.compile(r"\b[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.(?:com|org|net|io|cn|dev|ai|co|internal|local)\b"), "<domain>"),
]


def _get_experiences_dir(project_root: Path) -> Path:
    from ..utils import read_config
    config = read_config(project_root)
    exp_dir = config.get("experience", {}).get("dir", ".stdd/experiences")
    return project_root / exp_dir


def _ensure_dir(exp_dir: Path) -> None:
    exp_dir.mkdir(parents=True, exist_ok=True)


def _get_index_path(exp_dir: Path) -> Path:
    return exp_dir / ".experience-index.yaml"


def _load_index(exp_dir: Path) -> dict:
    index_path = _get_index_path(exp_dir)
    if not index_path.exists():
        index = _rebuild_index(exp_dir)
        _save_index(exp_dir, index)
        return index
    with open(index_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"last_id": 0, "total": 0}


def _save_index(exp_dir: Path, index: dict) -> None:
    index_path = _get_index_path(exp_dir)
    tmp_path = index_path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        yaml.dump(index, f, allow_unicode=True, default_flow_style=False)
    os.replace(tmp_path, index_path)


def _rebuild_index(exp_dir: Path) -> dict:
    index = {
        "last_id": 0,
        "total": 0,
        "by_category": {},
        "by_language": {},
        "by_lifecycle": {},
        "by_severity": {},
    }
    if not exp_dir.exists():
        return index

    for exp_file in sorted(exp_dir.glob("EXP-*.md")):
        data = _load_experience(exp_file)
        if data is None:
            continue
        eid = data.get("experience_id", exp_file.stem)
        _index_add_entry(index, eid, data)

    index["total"] = sum(len(v) for v in index.get("by_category", {}).values())
    if index["total"] > 0:
        ids = []
        for v in index.get("by_category", {}).values():
            ids.extend(v)
        index["last_id"] = max(int(x.split("-")[-1]) for x in ids) if ids else 0
    return index


def _index_add_entry(index: dict, eid: str, data: dict) -> None:
    cat = data.get("category", "unknown")
    lang = data.get("language") or "unknown"
    lc = data.get("lifecycle_state", "discovered")
    sev = data.get("severity", "medium")

    index.setdefault("by_category", {}).setdefault(cat, []).append(eid)
    index.setdefault("by_language", {}).setdefault(lang, []).append(eid)
    index.setdefault("by_lifecycle", {}).setdefault(lc, []).append(eid)
    index.setdefault("by_severity", {}).setdefault(sev, []).append(eid)


def _next_id(index: dict) -> str:
    last = index.get("last_id", 0)
    year = datetime.now().year
    next_num = last + 1
    return f"EXP-{year}-{next_num:04d}"


def _load_experience(filepath: Path) -> Optional[dict]:
    if not filepath.exists():
        return None
    content = filepath.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1]) or {}


def _sanitize(text: str) -> str:
    for pattern, replacement in SANITIZE_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def _format_table(experiences: list[dict]) -> str:
    if not experiences:
        return "  (无经验记录)"
    lines = []
    header = f"  {'ID':<16} {'Category':<22} {'Severity':<10} {'Occur':<6} {'Lifecycle':<12} Pattern"
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for e in experiences:
        cat_label = CATEGORY_LABELS.get(e.get("category", ""), e.get("category", ""))
        lines.append(
            f"  {e.get('experience_id', ''):<16} "
            f"{cat_label:<22} "
            f"{e.get('severity', ''):<10} "
            f"{e.get('occurrences', 0):<6} "
            f"{e.get('lifecycle_state', ''):<12} "
            f"{e.get('pattern', '')}"
        )
    return "\n".join(lines)


def _cmd_list(args: argparse.Namespace, exp_dir: Path) -> None:
    index = _load_index(exp_dir)
    experiences = []
    for exp_file in sorted(exp_dir.glob("EXP-*.md")):
        data = _load_experience(exp_file)
        if data is None:
            continue

        if args.category and data.get("category") != args.category:
            continue
        if args.language and data.get("language") != args.language:
            continue
        if args.lifecycle and data.get("lifecycle_state") != args.lifecycle:
            continue
        if args.severity and data.get("severity") != args.severity:
            continue

        experiences.append(data)

    if args.format == "json":
        print(json.dumps(experiences, ensure_ascii=False, indent=2))
    elif args.format == "yaml":
        print(yaml.dump(experiences, allow_unicode=True, default_flow_style=False))
    else:
        print()
        print(f"  经验库 ({len(experiences)}/{index.get('total', 0)} 条):")
        print(_format_table(experiences))
        print()


def _cmd_add(args: argparse.Namespace, exp_dir: Path) -> None:
    if args.category not in VALID_CATEGORIES:
        print(f" 无效的 category: '{args.category}'")
        print(f" 有效值: {', '.join(VALID_CATEGORIES)}")
        sys.exit(1)

    _ensure_dir(exp_dir)
    index = _load_index(exp_dir)

    eid = _next_id(index)
    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter = {
        "experience_id": eid,
        "category": args.category,
        "pattern": args.pattern,
        "root_cause": args.root_cause or "",
        "detection_trigger": args.detection_trigger or "",
        "fix_template": args.fix_template or "",
        "language": args.language,
        "tags": [t.strip() for t in (args.tags or "").split(",") if t.strip()],
        "occurrences": 1,
        "severity": args.severity or "medium",
        "confidence": 0.5,
        "source_change": args.source_change or "manual",
        "source_file": "",
        "lifecycle_state": "discovered",
        "first_seen": today,
        "last_seen": today,
    }

    body = args.body or ""
    content = f"---\n{yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False)}---\n\n{body}\n"

    exp_file = exp_dir / f"{eid}.md"
    exp_file.write_text(content, encoding="utf-8")

    _index_add_entry(index, eid, frontmatter)
    index["last_id"] = index.get("last_id", 0) + 1
    index["total"] = sum(len(v) for v in index.get("by_category", {}).values())
    _save_index(exp_dir, index)

    print(f" 经验已创建: {eid} ({CATEGORY_LABELS.get(args.category, args.category)})")


def _cmd_stats(args: argparse.Namespace, exp_dir: Path) -> None:
    index = _load_index(exp_dir)

    if args.format == "json":
        print(json.dumps(index, ensure_ascii=False, indent=2))
        return

    print()
    print("  经验库统计")
    print(f"  {'─' * 40}")
    print(f"  总经验数: {index.get('total', 0)}")

    by_cat = index.get("by_category", {})
    if by_cat:
        print("\n  按失败模式分类:")
        for cat, ids in sorted(by_cat.items(), key=lambda x: -len(x[1])):
            label = CATEGORY_LABELS.get(cat, cat)
            print(f"    {label}: {len(ids)} 条")

    by_lang = index.get("by_language", {})
    if by_lang:
        print("\n  按语言分类:")
        for lang, ids in sorted(by_lang.items(), key=lambda x: -len(x[1])):
            print(f"    {lang}: {len(ids)} 条")

    by_sev = index.get("by_severity", {})
    if by_sev:
        print("\n  按严重程度:")
        for sev, ids in sorted(by_sev.items(), key=lambda x: -len(x[1])):
            print(f"    {sev}: {len(ids)} 条")

    by_lc = index.get("by_lifecycle", {})
    if by_lc:
        print("\n  按生命周期:")
        for lc, ids in sorted(by_lc.items(), key=lambda x: -len(x[1])):
            print(f"    {lc}: {len(ids)} 条")
    print()


def _cmd_export(args: argparse.Namespace, exp_dir: Path) -> None:
    experiences = []
    for exp_file in sorted(exp_dir.glob("EXP-*.md")):
        data = _load_experience(exp_file)
        if data is None:
            continue
        content = exp_file.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        body = parts[2].strip() if len(parts) >= 3 else ""

        if not getattr(args, "no_sanitize", False):
            body = _sanitize(body)
            for key in ("pattern", "root_cause", "detection_trigger", "fix_template"):
                if key in data and data[key]:
                    data[key] = _sanitize(str(data[key]))
            if "source_file" in data:
                data["source_file"] = _sanitize(str(data["source_file"]))
            if "source_change" in data and data["source_change"]:
                data["source_change"] = _sanitize(str(data["source_change"]))

        experiences.append({"frontmatter": data, "body": body})

    result = json.dumps(experiences, ensure_ascii=False, indent=2) if args.format == "json" else yaml.dump(experiences, allow_unicode=True, default_flow_style=False)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f" 已导出 {len(experiences)} 条经验到: {args.output}")
    else:
        print(result)


def _cmd_pull(args: argparse.Namespace, exp_dir: Path) -> None:
    print()
    print(" 此功能将在 V2.5 正式支持。")
    print(f" 届时可通过 `stdd experience pull {args.pack_name}` 从社区经验池下载经验包。")
    print(" 当前 V2.4 请使用 `stdd experience add` 手动添加项目经验。")
    print()


def cmd_experience(args: argparse.Namespace) -> None:
    from ..utils import get_logger
    get_logger()

    project_root = Path.cwd()
    exp_dir = _get_experiences_dir(project_root)

    subcommand = getattr(args, "subcommand", "list")

    if subcommand == "list":
        _cmd_list(args, exp_dir)
    elif subcommand == "add":
        _cmd_add(args, exp_dir)
    elif subcommand == "stats":
        _cmd_stats(args, exp_dir)
    elif subcommand == "export":
        _cmd_export(args, exp_dir)
    elif subcommand == "pull":
        _cmd_pull(args, exp_dir)
    else:
        print(f" 未知子命令: {subcommand}")
        print(" 可用: list, add, stats, export, pull")
        sys.exit(1)
