#!/usr/bin/env python3
"""Claude Code hooks enforcing AGENTS.md mechanically. One module, three events:

    guard.py pre-edit    PreToolUse  Edit|Write|NotebookEdit  deny edits to generated or vendored paths
    guard.py post-edit   PostToolUse Edit|Write               reseal + regenerate the ledger; check ESTATE pins
    guard.py pre-bash    PreToolUse  Bash                     gate `git commit` on the fast gates and the message rule

Reads the hook payload from stdin. Paths outside this repository are ignored.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Generated or pinned paths: never hand-edited (AGENTS.md § Generated surfaces, § Vendored packages).
PROTECTED = (
    ("vendor/*", "vendored byte for byte from larsbx/finite-math-kernels: change it upstream, re-vendor, "
                 "re-pin with vendor/vendoring/check_vendored_sync.py pin NAME COMMIT, then tools/estate_pins.py --write"),
    ("data/*", "a census output: rerun the script named in its ledger `replay` (without --check), "
               "then update the record's digest and reseal"),
    ("tla/*", "generated from research/ledger.json: edit the ledger, then tools/seal_ledger.py and the generator"),
    ("docs/ledger-index.md", "generated from research/ledger.json: edit the ledger, then tools/seal_ledger.py and the generator"),
    ("paper/*/tables/*", "generated from data/: run the paper's make_tables.py"),
    ("tools/audit_estate_layout.py", "a vendored copy of the estate audit is forbidden (SPEC_estate §5); CI downloads it by pin"),
)
GENERATED_BLOCK = ("# BEGIN generated claims", "# END generated claims")
# Model identifiers never go into a commit (session policy); attribution trailers are fine.
MODEL_ID = re.compile(r"\bclaude-(?:opus|sonnet|haiku|fable)-\d[\w.-]*", re.IGNORECASE)


def relative(path: str | None) -> str | None:
    if not path:
        return None
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return None


def deny(reason: str) -> int:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    return 0


def run(*cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env={**os.environ, "PYTHONPATH": "vendor"})


def touches_generated_block(tool: dict) -> bool:
    """Whether an edit of claim_governance.toml changes the generated [[claim]] block."""
    text = (ROOT / "claim_governance.toml").read_text(encoding="utf-8")
    start, end = text.find(GENERATED_BLOCK[0]), text.find(GENERATED_BLOCK[1])
    if "content" in tool:   # Write: compare the block before and after
        new = tool["content"]
        return new[new.find(GENERATED_BLOCK[0]):new.find(GENERATED_BLOCK[1])] != text[start:end]
    old = tool.get("old_string", "")
    at = text.find(old) if old else -1
    return at != -1 and at + len(old) > start and at < end


def pre_edit(payload: dict) -> int:
    tool = payload.get("tool_input", {})
    rel = relative(tool.get("file_path") or tool.get("notebook_path"))
    if rel is None:
        return 0
    for pattern, why in PROTECTED:
        if fnmatch(rel, pattern):
            return deny(f"{rel} is not hand-edited: {why}.")
    if rel == "claim_governance.toml" and touches_generated_block(tool):
        return deny("the [[claim]] block of claim_governance.toml is generated: edit research/ledger.json, "
                    "then tools/seal_ledger.py and the generator. The hand-written head above the markers is editable.")
    return 0


def post_edit(payload: dict) -> int:
    rel = relative(payload.get("tool_input", {}).get("file_path"))
    if rel == "research/ledger.json":
        steps = [("reseal", run(sys.executable, "tools/seal_ledger.py")),
                 ("regenerate", run(sys.executable, "-m", "proof_records.generate_ledgers", "research/ledger.json",
                                    "--claims", "claim_governance.toml"))]
        failed = [(name, r) for name, r in steps if r.returncode]
        if failed:
            name, r = failed[0]
            print(json.dumps({"decision": "block",
                              "reason": f"ledger {name} failed after editing research/ledger.json:\n{r.stdout}{r.stderr}"}))
        else:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext":
                              "research/ledger.json was resealed and its surfaces regenerated "
                              "(docs/ledger-index.md, tla/, the claim block of claim_governance.toml)."}}))
    elif rel in ("vendored.toml", "ESTATE.toml"):
        r = run(sys.executable, "tools/estate_pins.py")
        if r.returncode:
            print(json.dumps({"decision": "block", "reason": r.stdout + r.stderr}))
    return 0


def pre_bash(payload: dict) -> int:
    command = payload.get("tool_input", {}).get("command", "")
    if not re.search(r"\bgit\b[^;&|]*\bcommit\b", command):
        return 0
    if (found := MODEL_ID.search(command)):
        return deny(f"the commit names a model identifier ({found.group(0)}); keep model identifiers out of commits.")
    r = subprocess.run(["scripts/verify_all.sh", "fast"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        return deny("fast gates failed; fix them before committing (scripts/verify_all.sh fast):\n" + r.stdout)
    return 0


if __name__ == "__main__":
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    handlers = {"pre-edit": pre_edit, "post-edit": post_edit, "pre-bash": pre_bash}
    if event not in handlers:
        print(f"usage: guard.py {{{'|'.join(handlers)}}}", file=sys.stderr)
        raise SystemExit(1)   # non-blocking error: a misconfigured hook must not wedge the session
    raise SystemExit(handlers[event](json.load(sys.stdin)))
