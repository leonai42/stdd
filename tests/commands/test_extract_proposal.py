"""Tests for stdd extract-proposal CLI."""
import json, yaml, argparse
from pathlib import Path
from stdd.cli.commands.extract_proposal import cmd_extract_proposal

class TestExtractProposal:
    def test_extracts_json(self, tmp_path, capsys):
        d = tmp_path / "changes" / "2026-06-06-test"
        d.mkdir(parents=True)
        (d / "proposal.md").write_text("# Test\n## Why\nA problem.\n## What Changes\n- C1\n- C2\n## Capabilities\n### New\n- **a**: A\n### Modified\n- **b**: B\n## Success Criteria\n- [ ] S1\n- [ ] S2\n", encoding="utf-8")
        (d / ".stdd.yaml").write_text("status: active\n", encoding="utf-8")
        ns = argparse.Namespace(name="2026-06-06-test", format="json", verbose=0, dry_run=False)
        cmd_extract_proposal(ns)
        data = json.loads(capsys.readouterr().out)
        assert data["title"] == "Test"
        assert len(data["what_changes"]) == 2
        assert len(data["success_criteria"]) == 2
