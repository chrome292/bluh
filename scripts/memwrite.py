#!/usr/bin/env python3
"""Safe writes to memory/: compare-and-swap, permission tiers, provenance log.

    memwrite.py hash  <path>                                  print the file's current hash
    memwrite.py write <path> --expect <hash> --by <who> --why <reason>  < new_content
    memwrite.py append <path> --by <who> --why <reason>       < text_to_append

`write` refuses if the file changed since you read it (the hash no longer matches
--expect). When that happens, re-read the file, redo your edit, and try again.
Pass --expect new for a file that doesn't exist yet.
Every successful change is recorded in memory/CHANGELOG.md, and git history is
the version store, so any change can be rolled back.
"""
import argparse
import datetime
import fcntl
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEM = ROOT / "memory"
READ_ONLY = ("org/",)  # human-curated tiers agents may not write
LOG = MEM / "CHANGELOG.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16] if path.exists() else "new"


def resolve(rel: str) -> Path:
    p = (ROOT / rel).resolve()
    if MEM not in p.parents:
        sys.exit(f"refused: {rel} is outside memory/")
    sub = p.relative_to(MEM).as_posix()
    if sub.startswith(READ_ONLY) or p == LOG:
        sys.exit(f"refused: {sub} is read-only to agents; propose the change in memory/proposals/ instead")
    return p


def log(path: Path, before: str, after: str, by: str, why: str) -> None:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with LOG.open("a") as f:
        f.write(f"- {ts} {path.relative_to(MEM).as_posix()} {before}->{after} by={by}: {why}\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("op", choices=["hash", "write", "append"])
    ap.add_argument("path")
    ap.add_argument("--expect")
    ap.add_argument("--by", default="unknown")
    ap.add_argument("--why", default="")
    a = ap.parse_args()

    if a.op == "hash":
        print(digest(ROOT / a.path))
        return

    path = resolve(a.path)
    if not a.why:
        sys.exit("refused: --why is required so the change can be audited")
    data = sys.stdin.read()

    # One lock for all of memory/: the check and the write happen as a single step.
    with open(MEM / ".memwrite.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        before = digest(path)
        if a.op == "write":
            if a.expect is None:
                sys.exit("refused: write needs --expect <hash> (from `memwrite.py hash`)")
            if a.expect != before:
                sys.exit(f"conflict: {a.path} changed since you read it ({a.expect} != {before}); re-read and retry")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
        else:
            with path.open("a") as f:
                f.write(data if data.endswith("\n") else data + "\n")
        after = digest(path)
        log(path, before, after, a.by, a.why)
    print(after)


if __name__ == "__main__":
    main()
