"""stdd experience curate — Official maintainer tool for curating community experiences (V2.5)."""

import argparse
import sys
import tarfile
import tempfile
from pathlib import Path
from datetime import datetime

import yaml
import requests


def _read_community_config(project_root: Path) -> dict:
    from ..utils import read_config
    config = read_config(project_root)
    return config.get("community", {})


def _get_curation_dir(project_root: Path) -> Path:
    d = project_root / ".stdd" / "curation"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _pattern_similarity(a: str, b: str) -> float:
    """Jaccard similarity on word tokens between two pattern strings."""
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union) if union else 0.0


def cmd_curate_pull(args: argparse.Namespace, project_root: Path) -> None:
    """Download all .tar.gz packs from all registries into inbox."""
    config = _read_community_config(project_root)
    curation_dir = _get_curation_dir(project_root)
    inbox = curation_dir / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    registries = sorted(config.get("registries", []), key=lambda r: r.get("priority", 99))
    packs = config.get("packs", [])
    timeout = config.get("fallback_timeout", 5)

    total = 0
    sources = set()

    for pack_info in packs:
        pack_name = pack_info.get("name", "")
        version = pack_info.get("version", "latest")
        filename = f"experience-{pack_name}-{version}.tar.gz"

        for registry in registries:
            url = f"{registry['url'].rstrip('/')}/{filename}"
            try:
                resp = requests.get(url, timeout=timeout)
                resp.raise_for_status()
                dest = inbox / filename
                dest.write_bytes(resp.content)
                total += 1
                sources.add(registry["name"])
                break  # Got it from this registry, don't try others
            except requests.RequestException:
                continue  # Try next registry

    print(f"  Downloaded: {total} packs from {len(sources)} sources")
    print(f"  Inbox: {inbox}")


def cmd_curate_deduplicate(args: argparse.Namespace, project_root: Path) -> None:
    """Detect and merge duplicate experiences in inbox."""
    curation_dir = _get_curation_dir(project_root)
    inbox = curation_dir / "inbox"
    if not inbox.exists():
        print("  Inbox is empty. Run 'curate pull' first.")
        return

    # Extract all experiences from inbox tarballs
    all_exps = {}  # eid -> (data, body)
    for tar_file in sorted(inbox.glob("*.tar.gz")):
        with tarfile.open(tar_file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.name.startswith("EXP-") and member.name.endswith(".md"):
                    eid = Path(member.name).stem
                    if eid in all_exps:
                        continue
                    fobj = tar.extractfile(member)
                    if fobj:
                        content = fobj.read().decode("utf-8")
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            data = yaml.safe_load(parts[1]) or {}
                            all_exps[eid] = (data, parts[2].strip())

    eids = list(all_exps.keys())
    merges = []
    flagged = []

    for i in range(len(eids)):
        for j in range(i + 1, len(eids)):
            pattern_a = all_exps[eids[i]][0].get("pattern", "")
            pattern_b = all_exps[eids[j]][0].get("pattern", "")
            sim = _pattern_similarity(pattern_a, pattern_b)

            if sim > 0.8:
                merges.append((eids[i], eids[j], sim))
            elif sim > 0.6:
                flagged.append((eids[i], eids[j], sim))

    # Auto-merge high-similarity pairs
    merged_count = 0
    merged_ids = set()
    for eid_a, eid_b, sim in merges:
        if eid_a in merged_ids or eid_b in merged_ids:
            continue
        data_a, body_a = all_exps[eid_a]
        data_b, body_b = all_exps[eid_b]

        # Keep the more complete entry
        completeness_a = sum(1 for k in ("root_cause", "fix_template") if data_a.get(k))
        completeness_b = sum(1 for k in ("root_cause", "fix_template") if data_b.get(k))

        if completeness_a >= completeness_b:
            keeper, dropper = eid_a, eid_b
            keeper_data, keeper_body = data_a, body_a
            dropper_data = data_b
        else:
            keeper, dropper = eid_b, eid_a
            keeper_data, keeper_body = data_b, body_b
            dropper_data = data_a

        # Merge: tags union, occurrences sum, confidence max
        keeper_data["tags"] = list(set(keeper_data.get("tags", []) + dropper_data.get("tags", [])))
        keeper_data["occurrences"] = keeper_data.get("occurrences", 1) + dropper_data.get("occurrences", 1)
        keeper_data["confidence"] = max(keeper_data.get("confidence", 0.5), dropper_data.get("confidence", 0.5))

        merged_ids.add(keeper)
        merged_ids.add(dropper)
        merged_count += 1

    if merges:
        print(f"  发现 {len(merges)} 组疑似重复，合并后: {len(all_exps)} → {len(all_exps) - merged_count} 条")
    if flagged:
        print(f"  {len(flagged)} 组相似度在 60-80%，标记为'待人工确认':")
        for eid_a, eid_b, sim in flagged:
            data_a = all_exps[eid_a][0]
            data_b = all_exps[eid_b][0]
            print(f"    - {eid_a} ↔ {eid_b} (相似度: {sim:.0%})")
            print(f"      A: {data_a.get('pattern', '')[:80]}")
            print(f"      B: {data_b.get('pattern', '')[:80]}")
    if not merges and not flagged:
        print("  未发现重复经验。")


def cmd_curate_review(args: argparse.Namespace, project_root: Path) -> None:
    """Interactive review of experiences in inbox."""
    curation_dir = _get_curation_dir(project_root)
    inbox = curation_dir / "inbox"
    if not inbox.exists():
        print("  Inbox is empty. Run 'curate pull' first.")
        return

    # Collect all experiences
    all_exps = {}
    for tar_file in sorted(inbox.glob("*.tar.gz")):
        with tarfile.open(tar_file, "r:gz") as tar:
            for member in tar.getmembers():
                if member.name.startswith("EXP-") and member.name.endswith(".md"):
                    eid = Path(member.name).stem
                    if eid in all_exps:
                        continue
                    fobj = tar.extractfile(member)
                    if fobj:
                        content = fobj.read().decode("utf-8")
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            data = yaml.safe_load(parts[1]) or {}
                            all_exps[eid] = (data, parts[2].strip())

    approved = []
    rejected = []

    for eid, (data, body) in all_exps.items():
        occurrences = data.get("occurrences", 1)
        confidence = data.get("confidence", 0.5)
        root_cause = data.get("root_cause", "")
        fix_template = data.get("fix_template", "")

        # Auto-suggestions
        flags = []
        if occurrences < 2 and confidence < 0.5:
            flags.append("[LOW QUALITY]")
        if not root_cause or not fix_template:
            flags.append("[INCOMPLETE]")

        flag_str = " ".join(flags) if flags else ""
        print(f"\n  ─────────────────────────────")
        print(f"  {eid} {flag_str}")
        print(f"  Category: {data.get('category', '?')} | Severity: {data.get('severity', '?')}")
        print(f"  Occurrences: {occurrences} | Confidence: {confidence}")
        print(f"  Pattern: {data.get('pattern', '')[:100]}")
        if root_cause:
            print(f"  Root Cause: {root_cause[:100]}")
        if fix_template:
            print(f"  Fix: {fix_template[:100]}")
        print(f"  [a]pprove  [e]dit  [m]erge  [r]eject  [s]kip")

        # Interactive choice (V2.9.5)
        try:
            choice = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = "s"

        if choice == "a":
            data["curated"] = True
            data["pack_version"] = "v1.0.0"
            data["lifecycle_state"] = "merged"
            approved.append(eid)
            print("  -> Approved (merged)")
        elif choice == "r":
            try:
                reason = input("  Reject reason: ").strip()
            except (EOFError, KeyboardInterrupt):
                reason = "manual rejection"
            data["reject_reason"] = reason
            data["lifecycle_state"] = "retired"
            rejected.append(eid)
            print(f"  -> Rejected: {reason}")
        elif choice == "e":
            print(f"  Edit mode for {eid}")
            try:
                new_pat = input("  New pattern (Enter=keep): ").strip()
                if new_pat:
                    data["pattern"] = new_pat
                new_root = input("  New root_cause (Enter=keep): ").strip()
                if new_root:
                    data["root_cause"] = new_root
                new_fix = input("  New fix_template (Enter=keep): ").strip()
                if new_fix:
                    data["fix_template"] = new_fix
                data["curated"] = True
                data["pack_version"] = "v1.0.0"
                data["lifecycle_state"] = "merged"
                approved.append(eid)
                print("  -> Approved (edited)")
            except (EOFError, KeyboardInterrupt):
                print("  -> Skipped (edit cancelled)")
        else:
            print("  -> Skipped")

    print(f"\n  Review complete: {len(approved)} approved, {len(rejected)} rejected")


def cmd_curate_pack(args: argparse.Namespace, project_root: Path) -> None:
    """Package approved experiences into official release tar.gz."""
    curation_dir = _get_curation_dir(project_root)
    inbox = curation_dir / "inbox"

    language = getattr(args, "language", "python")
    version = getattr(args, "version", "v1.0.0")
    curated_by = getattr(args, "curated_by", "STDD maintainer")
    today = datetime.now().strftime("%Y-%m-%d")

    # Collect curated experiences
    curated = []
    if inbox.exists():
        for tar_file in sorted(inbox.glob("*.tar.gz")):
            with tarfile.open(tar_file, "r:gz") as tar:
                for member in tar.getmembers():
                    if member.name.startswith("EXP-") and member.name.endswith(".md"):
                        fobj = tar.extractfile(member)
                        if fobj:
                            content = fobj.read().decode("utf-8")
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                data = yaml.safe_load(parts[1]) or {}
                                if data.get("curated"):
                                    curated.append((Path(member.name).stem, data, parts[2].strip()))

    if not curated:
        print("  No approved experiences found. Run 'curate review' first.")
        return

    pack_name = f"experience-{language}-{version}"
    tar_path = project_root / ".stdd" / "curation" / f"{pack_name}.tar.gz"

    index = {"last_id": 0, "total": len(curated), "by_category": {}, "by_language": {}, "by_lifecycle": {}, "by_severity": {}}

    with tarfile.open(tar_path, "w:gz") as tar:
        for eid, data, body in curated:
            data["pack_version"] = version
            data["curated"] = True
            data["curated_by"] = curated_by
            data["curated_date"] = today

            frontmatter = yaml.dump(data, allow_unicode=True, default_flow_style=False)
            content = f"---\n{frontmatter}---\n\n{body}"

            info = tarfile.TarInfo(name=f"{eid}.md")
            info.size = len(content.encode("utf-8"))
            import io
            tar.addfile(info, io.BytesIO(content.encode("utf-8")))

            # Build index entry
            cat = data.get("category", "unknown")
            lang = data.get("language", "unknown")
            lc = data.get("lifecycle_state", "verified")
            sev = data.get("severity", "medium")
            index.setdefault("by_category", {}).setdefault(cat, []).append(eid)
            index.setdefault("by_language", {}).setdefault(lang, []).append(eid)
            index.setdefault("by_lifecycle", {}).setdefault(lc, []).append(eid)
            index.setdefault("by_severity", {}).setdefault(sev, []).append(eid)

        # Add index
        index_yaml = yaml.dump(index, allow_unicode=True, default_flow_style=False)
        info = tarfile.TarInfo(name=".experience-index.yaml")
        info.size = len(index_yaml.encode("utf-8"))
        import io
        tar.addfile(info, io.BytesIO(index_yaml.encode("utf-8")))

    print(f"  Pack created: {tar_path}")
    print(f"  {len(curated)} curated experiences for {language}")
    print(f"  Upload to GitHub + Gitee Release: {pack_name}.tar.gz")


def cmd_curate(args: argparse.Namespace) -> None:
    """CLI entry: stdd experience curate <subcommand>."""
    project_root = Path.cwd()
    subcommand = getattr(args, "curate_subcommand", "pull")

    if subcommand == "pull":
        cmd_curate_pull(args, project_root)
    elif subcommand == "deduplicate":
        cmd_curate_deduplicate(args, project_root)
    elif subcommand == "review":
        cmd_curate_review(args, project_root)
    elif subcommand == "pack":
        cmd_curate_pack(args, project_root)
    else:
        print(f"  Unknown curate subcommand: {subcommand}")
        print("  Available: pull, deduplicate, review, pack")
        sys.exit(1)
