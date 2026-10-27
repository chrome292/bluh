#!/usr/bin/env python3
"""Turn recent Claude Code sessions for this project into compact digests for /dream.

    collect_transcripts.py [--days 7] [--out .dream/inbox]

Reads ~/.claude/projects/<this-project>/*.jsonl and writes one markdown digest per
session: what the user asked, every tool call, and every tool error. Errors and
repeated corrections are where the patterns worth remembering show up.
"""
import argparse
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def project_dir() -> Path:
    slug = str(ROOT).replace("/", "-")
    return Path.home() / ".claude" / "projects" / slug


def clip(s: str, n: int) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def digest(path: Path) -> str | None:
    lines, n_err = [], 0
    for raw in path.open():
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if d.get("isSidechain") or d.get("type") not in ("user", "assistant"):
            continue
        content = d.get("message", {}).get("content")
        if isinstance(content, str):
            if d["type"] == "user" and not content.startswith("<"):
                lines.append(f"USER: {clip(content, 400)}")
            continue
        for block in content or []:
            kind = block.get("type")
            if kind == "text" and d["type"] == "user":
                lines.append(f"USER: {clip(block['text'], 400)}")
            elif kind == "tool_use":
                lines.append(f"TOOL {block['name']}: {clip(json.dumps(block.get('input', {})), 200)}")
            elif kind == "tool_result" and block.get("is_error"):
                n_err += 1
                body = block.get("content")
                if isinstance(body, list):
                    body = " ".join(x.get("text", "") for x in body if isinstance(x, dict))
                lines.append(f"ERROR: {clip(str(body), 300)}")
    if not lines:
        return None
    return f"# Session {path.stem}\n\n{len(lines)} events, {n_err} tool errors\n\n" + "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out", default=str(ROOT / ".dream" / "inbox"))
    a = ap.parse_args()

    src = project_dir()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cutoff = datetime.datetime.now().timestamp() - a.days * 86400
    written = 0
    for f in sorted(src.glob("*.jsonl")) if src.exists() else []:
        if f.stat().st_mtime < cutoff:
            continue
        text = digest(f)
        if text:
            (out / f"{f.stem}.md").write_text(text)
            written += 1
    print(f"{written} session digests from {src} -> {out}")


if __name__ == "__main__":
    main()
