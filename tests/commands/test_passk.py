"""TC-PASSK-001~002: pass@k verification tests (V2.8)."""

import pytest
from pathlib import Path


class TestPassK:
    """TC-PASSK-001, TC-PASSK-002"""

    def test_passk_all_pass(self, tmp_path, monkeypatch, capsys):
        """k=3 all passes."""
        from stdd.cli.commands.ci import run_pass_k
        # Mock a command that always succeeds
        result = run_pass_k("python -c \"exit(0)\"", k=3)
        assert result["pass_count"] == 3
        assert result["total"] == 3
        assert result["pass_at_1"] == 1.0
        assert result["pass_at_k"] == 1.0

    def test_passk_mixed_results(self, tmp_path, monkeypatch, capsys):
        """pass@1 low, pass@3 high → ambiguity detected."""
        # Use a command that fails randomly based on a counter
        # Simulate by creating a temp script
        script = tmp_path / "flaky.py"
        script.write_text("""import sys, os
counter_file = os.path.join(os.path.dirname(__file__), 'counter.txt')
count = 0
try:
    with open(counter_file) as f:
        count = int(f.read().strip())
except:
    pass
count += 1
with open(counter_file, 'w') as f:
    f.write(str(count))
# Fail on first run, succeed on subsequent
if count == 1:
    sys.exit(1)
else:
    sys.exit(0)
""", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import run_pass_k
        result = run_pass_k(f"python {script}", k=3)
        assert result["pass_at_1"] == 0.0  # First run fails
        assert result["pass_at_k"] > 0.5  # At least one succeeds
        assert result["total"] == 3

    def test_passk_default_k1(self, tmp_path, monkeypatch):
        """Default k=1 maintains V2.7 behavior."""
        from stdd.cli.commands.ci import run_pass_k
        result = run_pass_k("python -c \"exit(0)\"", k=1)
        assert result["pass_count"] == 1
        assert result["total"] == 1