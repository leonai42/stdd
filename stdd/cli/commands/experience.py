import argparse
import sys
import os
import re
import json
import time
import tarfile
import tempfile
import io
from pathlib import Path
from datetime import datetime
from typing import Optional

import yaml
import requests


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

# Valid lifecycle state transitions
# discovered → verified → deposited
#                        → shared → merged
# ANY        → retired
VALID_TRANSITIONS = {
    "discovered": {"verified", "retired"},
    "verified": {"deposited", "shared", "retired"},
    "deposited": {"retired"},
    "shared": {"merged", "retired"},
    "merged": {"retired"},
    "retired": set(),  # terminal state
}


def _check_transition(current: str, target: str) -> tuple[bool, str]:
    """Validate lifecycle state transition. Returns (valid, error_message)."""
    current = current or "discovered"
    if current == target:
        return True, ""  # idempotent
    allowed = VALID_TRANSITIONS.get(current, set())
    if target not in allowed:
        return False, f"Invalid transition: '{current}' → '{target}'. Allowed: {', '.join(sorted(allowed)) if allowed else 'none (terminal)'}"
    return True, ""


def _auto_promote(data: dict) -> str | None:
    """Check and return target state if auto-promotion conditions are met. Returns None if no change."""
    state = data.get("lifecycle_state", "discovered")
    occurrences = data.get("occurrences", 1)
    confidence = data.get("confidence", 0.5)

    if state == "discovered" and occurrences >= 2 and confidence >= 0.7:
        return "verified"
    if state == "verified" and occurrences >= 3 and confidence >= 0.8:
        return "deposited"
    return None


PROJECT_TYPE_MAP = {
    ".py": "python",
    ".go": "go",
    ".java": "java",
    ".rs": "rust",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "static_site",
    ".html": "static_site",
    ".css": "static_site",
    ".vue": "static_site",
    ".md": "docs",
    ".yaml": "config",
    ".yml": "config",
    ".toml": "config",
    ".json": "config",
}


def _detect_project_type(change_dir: Path) -> str | None:
    """Detect project type from change directory file extensions. Returns None if undetectable."""
    if not change_dir.exists():
        return None
    ext_counts = {}
    for f in change_dir.rglob("*"):
        if f.is_file():
            ext = f.suffix.lower()
            if ext in PROJECT_TYPE_MAP:
                ptype = PROJECT_TYPE_MAP[ext]
                ext_counts[ptype] = ext_counts.get(ptype, 0) + 1
    if not ext_counts:
        return None
    # Return the most common type
    return max(ext_counts, key=ext_counts.get)


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
    lock_path = index_path.with_suffix(".lock")
    tmp_path = index_path.with_suffix(".tmp")

    # Acquire lock with retry
    for attempt in range(5):
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            if attempt < 4:
                time.sleep(0.05 * (attempt + 1))
            else:
                # Last attempt: force overwrite stale lock (> 5s old)
                try:
                    lock_age = time.time() - os.path.getmtime(lock_path)
                    if lock_age > 5:
                        os.remove(lock_path)
                        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                        os.close(fd)
                        break
                except OSError:
                    pass
                print("  警告: 无法获取经验索引锁，写入可能冲突。")
                # Fall through to write anyway

    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            yaml.dump(index, f, allow_unicode=True, default_flow_style=False)
        os.replace(tmp_path, index_path)
    finally:
        try:
            os.remove(lock_path)
        except OSError:
            pass


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
    show_all = getattr(args, "all", False)
    experiences = []
    for exp_file in sorted(exp_dir.glob("EXP-*.md")):
        data = _load_experience(exp_file)
        if data is None:
            continue

        # Hide retired by default
        if not show_all and data.get("lifecycle_state") == "retired":
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
        "community_votes_useful": 0,
        "community_votes_unuseful": 0,
        "adoption_count": 0,
        "project_type": getattr(args, "project_type", None) or _detect_project_type(Path.cwd() / "changes"),
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
    publish = getattr(args, "publish", False)
    no_sanitize = getattr(args, "no_sanitize", False)

    if publish and no_sanitize:
        print("  Warning: exporting without sanitization — review before sharing")

    experiences = []
    for exp_file in sorted(exp_dir.glob("EXP-*.md")):
        data = _load_experience(exp_file)
        if data is None:
            continue
        eid = data.get("experience_id", exp_file.stem)

        content = exp_file.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        body = parts[2].strip() if len(parts) >= 3 else ""

        if not no_sanitize:
            body = _sanitize(body)
            for key in ("pattern", "root_cause", "detection_trigger", "fix_template"):
                if key in data and data[key]:
                    data[key] = _sanitize(str(data[key]))
            if "source_file" in data:
                data["source_file"] = _sanitize(str(data["source_file"]))
            if "source_change" in data and data["source_change"]:
                data["source_change"] = _sanitize(str(data["source_change"]))

        if publish:
            data["lifecycle_state"] = "shared"
            full_content = f"---\n{yaml.dump(data, allow_unicode=True, default_flow_style=False)}---\n{body}"
            exp_file.write_text(full_content, encoding="utf-8")

        experiences.append({"frontmatter": data, "body": body})

    if publish:
        # Create tar.gz package
        tar_name = args.output or f"{getattr(args, 'experience_id', 'experiences')}.tar.gz"
        if not tar_name.endswith(".tar.gz"):
            tar_name += ".tar.gz"
        tar_path = Path(tar_name) if os.path.isabs(tar_name) else Path.cwd() / tar_name

        with tarfile.open(tar_path, "w:gz") as tar:
            for exp in experiences:
                eid = exp["frontmatter"]["experience_id"]
                frontmatter_yaml = yaml.dump(exp["frontmatter"], allow_unicode=True, default_flow_style=False)
                exp_content = f"---\n{frontmatter_yaml}---\n\n{exp['body']}"

                info = tarfile.TarInfo(name=f"{eid}.md")
                info.size = len(exp_content.encode("utf-8"))
                tar.addfile(info, io.BytesIO(exp_content.encode("utf-8")))

            # Add index file
            index = _load_index(exp_dir)
            index_content = yaml.dump(index, allow_unicode=True, default_flow_style=False)
            info = tarfile.TarInfo(name=".experience-index.yaml")
            info.size = len(index_content.encode("utf-8"))
            tar.addfile(info, io.BytesIO(index_content.encode("utf-8")))

        print(f"  Exported {len(experiences)} experiences to: {tar_path}")
        print(f"  Upload {tar_path.name} to GitHub Release or submit PR to stdd-experiences repo")
    else:
        result = json.dumps(experiences, ensure_ascii=False, indent=2) if args.format == "json" else yaml.dump(experiences, allow_unicode=True, default_flow_style=False)

        if args.output and not publish:
            Path(args.output).write_text(result, encoding="utf-8")
            print(f" 已导出 {len(experiences)} 条经验到: {args.output}")
        elif not publish:
            print(result)


def _read_community_config(project_root: Path) -> dict:
    from ..utils import read_config
    config = read_config(project_root)
    return config.get("community", {})


def _download_with_fallback(pack_name: str, pack_version: str, config: dict) -> bytes | None:
    """Download pack from registries with priority ordering and timeout fallback.

    Supports two registry types:
      - github (default):  {url}/experience-{pack}-latest.tar.gz
      - gitee:             {url}/{version}/experience-{pack}-{version}.tar.gz
    """
    registries = sorted(config.get("registries", []), key=lambda r: r.get("priority", 99))
    timeout = config.get("fallback_timeout", 5)

    for i, registry in enumerate(registries):
        registry_type = registry.get("type", "github")

        if registry_type == "gitee":
            # Gitee: /releases/download/{tag}/{file} — no /latest/ redirect
            pack_filename = f"experience-{pack_name}-{pack_version}.tar.gz"
            url = f"{registry['url'].rstrip('/')}/{pack_version}/{pack_filename}"
        else:
            # GitHub (default): /releases/latest/download/{file}
            pack_filename = f"experience-{pack_name}-latest.tar.gz"
            url = f"{registry['url'].rstrip('/')}/{pack_filename}"

        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            if i > 0:
                print(f"  [FALLBACK] Switched to {registry['name']} mirror")
            return resp.content
        except requests.Timeout:
            if i < len(registries) - 1:
                source_name = registry['name']
                next_name = registries[i + 1]['name']
                print(f"  [FALLBACK] {source_name} timed out, switched to {next_name} mirror")
        except requests.RequestException as e:
            if i < len(registries) - 1:
                print(f"  [FALLBACK] {registry['name']} unreachable ({e}), switching to {registries[i + 1]['name']} mirror")

    return None


def _cmd_pull(args: argparse.Namespace, exp_dir: Path) -> None:
    project_root = Path.cwd()
    config = _read_community_config(project_root)

    if not config.get("registries"):
        print("  No community registries configured in experience.yaml")
        sys.exit(1)

    pack_name = args.pack_name

    # Look up pack version from config
    pack_version = None
    for pack in config.get("packs", []):
        if pack.get("name") == pack_name:
            pack_version = pack.get("version", "latest")
            break
    if pack_version is None:
        pack_version = "latest"

    print(f"  Pulling experience pack: {pack_name} (version: {pack_version}) ...")

    data = _download_with_fallback(pack_name, pack_version, config)
    if data is None:
        print(f"  Error: all registries unreachable")
        sys.exit(1)

    existing_ids = set()
    for f in exp_dir.glob("EXP-*.md"):
        existing_ids.add(f.stem)

    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)

    try:
        with tarfile.open(tmp_path, "r:gz") as tar:
            members = tar.getmembers()
            exp_members = [m for m in members if m.name.startswith("EXP-") and m.name.endswith(".md")]
            index_member = None
            for m in members:
                if m.name.endswith(".experience-index.yaml"):
                    index_member = m
                    break

            if not exp_members and index_member is None:
                print(f"  Error: pack '{pack_name}' not found in registry")
                sys.exit(1)

            new_count = 0
            skip_count = 0
            update_count = 0

            for member in exp_members:
                eid = Path(member.name).stem
                dest = exp_dir / f"{eid}.md"

                if dest.exists():
                    print(f"  [SKIP] {eid} already exists locally")
                    skip_count += 1
                    continue

                fobj = tar.extractfile(member)
                if fobj:
                    dest.write_bytes(fobj.read())
                    new_count += 1
                    print(f"  [NEW] {eid} imported")

            # Merge index: add new IDs, update vote metadata for existing IDs
            if index_member:
                fobj = tar.extractfile(index_member)
                if fobj:
                    remote_index = yaml.safe_load(fobj.read()) or {}
                    local_index = _load_index(exp_dir)

                    for cat, ids in remote_index.get("by_category", {}).items():
                        for eid in ids:
                            if eid in existing_ids:
                                # Update vote metadata for existing experience
                                exp_file = exp_dir / f"{eid}.md"
                                local_data = _load_experience(exp_file)
                                if local_data:
                                    # Find the remote experience data for vote sync
                                    for rm in exp_members:
                                        if Path(rm.name).stem == eid:
                                            rf = tar.extractfile(rm)
                                            if rf:
                                                remote_data = yaml.safe_load(rf.read().decode("utf-8").split("---", 2)[1]) or {}
                                                for vk in ("community_votes_useful", "community_votes_unuseful", "adoption_count"):
                                                    if vk in remote_data:
                                                        local_data[vk] = remote_data[vk]
                                                content = exp_file.read_text(encoding="utf-8")
                                                parts = content.split("---", 2)
                                                body = parts[2] if len(parts) >= 3 else ""
                                                new_content = f"---\n{yaml.dump(local_data, allow_unicode=True, default_flow_style=False)}---\n{body}"
                                                exp_file.write_text(new_content, encoding="utf-8")
                                                update_count += 1
                                                break
                            else:
                                local_index.setdefault("by_category", {}).setdefault(cat, []).append(eid)

                    _save_index(exp_dir, local_index)

            total = new_count + update_count
            print(f"  Done: {total} experiences ({new_count} new, {update_count} updated, {skip_count} skipped)")

    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


def _cmd_verify(args: argparse.Namespace, exp_dir: Path) -> None:
    """Manually verify a discovered experience."""
    exp_file = exp_dir / f"{args.experience_id}.md"
    data = _load_experience(exp_file)
    if data is None:
        print(f"Experience '{args.experience_id}' not found.")
        sys.exit(1)

    current_state = data.get("lifecycle_state", "discovered")
    valid, err = _check_transition(current_state, "verified")
    if not valid:
        print(err)
        sys.exit(1)

    # Update frontmatter
    data["lifecycle_state"] = "verified"
    if "occurrences" in data:
        data["occurrences"] = max(data["occurrences"], 2)
    if "confidence" in data:
        data["confidence"] = max(data["confidence"], 0.7)

    content = exp_file.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    body = parts[2] if len(parts) >= 3 else ""
    new_content = f"---\n{yaml.dump(data, allow_unicode=True, default_flow_style=False)}---\n{body}"
    exp_file.write_text(new_content, encoding="utf-8")

    # Update index
    index = _load_index(exp_dir)
    _index_remove_entry(index, args.experience_id, current_state)
    _index_add_entry(index, args.experience_id, data)
    _save_index(exp_dir, index)

    print(f"{args.experience_id} verified (discovered → verified)")


def _cmd_deposit(args: argparse.Namespace, exp_dir: Path) -> None:
    """Manually deposit a verified experience (requires occurrences>=3, confidence>=0.8)."""
    exp_file = exp_dir / f"{args.experience_id}.md"
    data = _load_experience(exp_file)
    if data is None:
        print(f"Experience '{args.experience_id}' not found.")
        sys.exit(1)

    current_state = data.get("lifecycle_state", "discovered")
    valid, err = _check_transition(current_state, "deposited")
    if not valid:
        print(err)
        sys.exit(1)

    if data.get("occurrences", 1) < 3:
        print(f"Cannot deposit: occurrences ({data.get('occurrences', 1)}) < 3")
        sys.exit(1)
    if data.get("confidence", 0.5) < 0.8:
        print(f"Cannot deposit: confidence ({data.get('confidence', 0.5)}) < 0.8")
        sys.exit(1)

    data["lifecycle_state"] = "deposited"

    content = exp_file.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    body = parts[2] if len(parts) >= 3 else ""
    new_content = f"---\n{yaml.dump(data, allow_unicode=True, default_flow_style=False)}---\n{body}"
    exp_file.write_text(new_content, encoding="utf-8")

    index = _load_index(exp_dir)
    _index_remove_entry(index, args.experience_id, current_state)
    _index_add_entry(index, args.experience_id, data)
    _save_index(exp_dir, index)

    print(f"{args.experience_id} deposited (verified → deposited)")


def _cmd_retire(args: argparse.Namespace, exp_dir: Path) -> None:
    """Retire an experience from any lifecycle state."""
    exp_file = exp_dir / f"{args.experience_id}.md"
    data = _load_experience(exp_file)
    if data is None:
        print(f"Experience '{args.experience_id}' not found.")
        sys.exit(1)

    current_state = data.get("lifecycle_state", "discovered")
    valid, err = _check_transition(current_state, "retired")
    if not valid:
        print(err)
        sys.exit(1)

    reason = getattr(args, "reason", "")
    data["lifecycle_state"] = "retired"
    data["retire_reason"] = reason
    data["retired_date"] = datetime.now().strftime("%Y-%m-%d")

    content = exp_file.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    body = parts[2] if len(parts) >= 3 else ""
    new_content = f"---\n{yaml.dump(data, allow_unicode=True, default_flow_style=False)}---\n{body}"
    exp_file.write_text(new_content, encoding="utf-8")

    index = _load_index(exp_dir)
    _index_remove_entry(index, args.experience_id, current_state)
    _index_add_entry(index, args.experience_id, data)
    _save_index(exp_dir, index)

    print(f"{args.experience_id} retired ({current_state} → retired)")


def _index_remove_entry(index: dict, eid: str, old_state: str) -> None:
    """Remove an entry from all index buckets based on old state. Best-effort cleanup."""
    for bucket in ("by_category", "by_language", "by_lifecycle", "by_severity"):
        for key in list(index.get(bucket, {}).keys()):
            entry_list = index[bucket].get(key, [])
            if eid in entry_list:
                entry_list.remove(eid)
                if not entry_list:
                    del index[bucket][key]


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
    elif subcommand == "verify":
        _cmd_verify(args, exp_dir)
    elif subcommand == "deposit":
        _cmd_deposit(args, exp_dir)
    elif subcommand == "retire":
        _cmd_retire(args, exp_dir)
    elif subcommand == "curate":
        from .curate import cmd_curate
        cmd_curate(args)
    else:
        print(f" 未知子命令: {subcommand}")
        print(" 可用: list, add, stats, export, pull, verify, deposit, retire, curate")
        sys.exit(1)
