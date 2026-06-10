#!/usr/bin/env python3
"""Extract URLs from a GitHub issue event payload."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s<>'\"`]+", re.I)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: issue_to_urls.py EVENT_JSON OUT_FILE", file=sys.stderr)
        return 2
    event_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    event = json.loads(event_path.read_text(encoding="utf-8"))
    issue = event.get("issue", {})
    text = "\n".join([str(issue.get("title", "")), str(issue.get("body", ""))])
    urls = list(dict.fromkeys(URL_RE.findall(text)))
    out_path.write_text("\n".join(urls) + ("\n" if urls else ""), encoding="utf-8")
    print(f"Found {len(urls)} URL(s)")
    return 0 if urls else 1


if __name__ == "__main__":
    raise SystemExit(main())
