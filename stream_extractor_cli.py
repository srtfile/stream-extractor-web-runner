#!/usr/bin/env python3
"""Command line runner for GitHub Actions.

Reads URLs, calls extractor_core.extract_stream(), and writes JSON + Markdown outputs.
Use only for media pages you own or are allowed to process.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from extractor_core import extract_stream

URL_RE = re.compile(r"https?://[^\s<>'\"`]+", re.I)


def collect_urls(args: argparse.Namespace) -> list[str]:
    chunks: list[str] = []
    if args.url:
        chunks.extend(args.url)
    if args.urls_file:
        chunks.append(Path(args.urls_file).read_text(encoding="utf-8", errors="replace"))
    if args.stdin:
        chunks.append(sys.stdin.read())

    raw = "\n".join(chunks)
    urls = URL_RE.findall(raw)
    # De-duplicate while preserving order
    return list(dict.fromkeys(u.strip() for u in urls if u.strip()))


def sanitize_result(result: dict[str, Any]) -> dict[str, Any]:
    """Keep workflow output readable and JSON-safe."""
    clean = dict(result)
    for key in ("headers", "chain"):
        if key in clean and not clean[key]:
            clean.pop(key, None)
    return clean


def result_to_markdown(results: list[dict[str, Any]]) -> str:
    ok = sum(1 for r in results if r.get("ok"))
    lines = [
        "## Stream extraction result",
        "",
        f"Processed: **{len(results)}** URL(s)",
        f"Success: **{ok}**",
        f"Failed: **{len(results) - ok}**",
        "",
        "> Use these results only for media you own or have permission to access.",
        "",
    ]

    for idx, item in enumerate(results, 1):
        lines.append(f"### {idx}. {item.get('host', 'unknown')}")
        lines.append("")
        lines.append(f"Input: `{item.get('input_url', '')}`")
        if item.get("ok"):
            lines.append(f"Type: `{item.get('type', 'unknown')}`")
            lines.append("")
            lines.append("```text")
            lines.append(str(item.get("url", "")))
            lines.append("```")
            extra = item.get("extra") or []
            if isinstance(extra, list) and len(extra) > 1:
                lines.append(f"Additional streams found: **{len(extra) - 1}**")
        else:
            lines.append(f"Error: `{item.get('error', 'unknown error')}`")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run stream URL extraction from CLI/GitHub Actions.")
    parser.add_argument("--url", action="append", help="URL to process. Can be repeated.")
    parser.add_argument("--urls-file", help="Text file containing URLs.")
    parser.add_argument("--stdin", action="store_true", help="Read URLs from stdin.")
    parser.add_argument("--output-dir", default="results", help="Directory for output files.")
    parser.add_argument("--json-name", default="results.json", help="JSON output filename.")
    parser.add_argument("--markdown-name", default="results.md", help="Markdown output filename.")
    args = parser.parse_args()

    urls = collect_urls(args)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not urls:
        results = [{"ok": False, "error": "No valid http(s) URLs found."}]
    else:
        results = []
        for url in urls:
            started = time.time()
            try:
                data = sanitize_result(extract_stream(url))
                data["ok"] = True
                data["elapsed_seconds"] = round(time.time() - started, 2)
                results.append(data)
            except Exception as exc:  # keep Action running so all URLs report back
                results.append({
                    "ok": False,
                    "input_url": url,
                    "host": "unknown",
                    "error": str(exc),
                    "elapsed_seconds": round(time.time() - started, 2),
                })

    json_path = out_dir / args.json_name
    md_path = out_dir / args.markdown_name
    json_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(result_to_markdown(results), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(result_to_markdown(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
