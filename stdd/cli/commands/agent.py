"""STDD agent verify CLI — Agent CP-based verification pipeline (V2.7)."""

import sys
import yaml
from pathlib import Path


def cmd_agent_verify(args):
    """Execute Agent verification checkpoints."""
    project_root = Path.cwd()
    spec_file = project_root / "canonical" / "specs" / "agent" / f"{args.task}.yaml"

    if not spec_file.exists():
        print(f"  canonical/specs/agent/{args.task}.yaml not found")
        sys.exit(1)

    data = yaml.safe_load(spec_file.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    meta = data.get("meta", {})

    print(f"\n  Agent Verify: {meta.get('task_id', args.task)}")
    print(f"  System: {meta.get('system', 'unknown')}")
    print(f"  Checkpoints: {len(steps)}")
    print()

    if args.dry_run:
        _dry_run(steps)
        return

    passed = 0
    failed = 0

    for step in steps:
        if args.cp and step["id"] != args.cp:
            continue

        print(f"  [{step['id']}] {step['description']}")
        if args.dry_run:
            continue

        # Execute and collect results
        import subprocess
        action = step.get("action", "")
        result = subprocess.run(action, shell=True, capture_output=True, text=True)

        # Check assertions
        step_failed = False
        for assertion in step.get("assertions", []):
            atype = assertion.get("type", "")
            expected = assertion.get("expected", "")
            actual = ""

            if atype == "exit_code":
                actual = str(result.returncode)
                ok = (result.returncode == expected)
            elif atype == "stdout_contains":
                actual = result.stdout[:200]
                ok = (expected in result.stdout)
            elif atype == "stderr_contains":
                actual = result.stderr[:200]
                ok = (expected in result.stderr)
            else:
                ok = False

            status = "PASS" if ok else "FAIL"
            if not ok:
                step_failed = True
                failed += 1
            else:
                passed += 1

            print(f"    {status}: {atype} (expected: {expected}, got: {str(actual)[:80]})")

        if not step.get("assertions"):
            passed += 1
            print("    PASS: action completed")
            continue

    print(f"\n  Results: {passed} passed, {failed} failed")
    if failed > 0:
        print(f"  Report: agent-verification-report.md")
        sys.exit(1)


def _dry_run(steps: list):
    """Preview mode — show what would be done."""
    for step in steps:
        print(f"  [{step['id']}] {step['description']}")
        print(f"    Action: {step.get('action', 'N/A')}")
        for assertion in step.get("assertions", []):
            print(f"    Assert: {assertion['type']} == {assertion.get('expected', '?')}")
        print()


def _dispatch(args):
    """Route to appropriate agent subcommand."""
    if args.action == "verify":
        cmd_agent_verify(args)
    else:
        print(f"  Unknown agent action: {args.action}")
        sys.exit(1)
