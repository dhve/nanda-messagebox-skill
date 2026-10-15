#!/usr/bin/env python3
"""Lightweight checks for demo/index.html before it is published.

Usage (from the repository root):
  python3 demo/tools/check_page.py            draft check: missing assets are reported as PENDING
  python3 demo/tools/check_page.py --publish  publish gate: any missing asset or failure exits 1

Uses only the Python standard library. If Pillow or ffprobe are installed, image sizes and
video details are checked too. No browser is used.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

DEMO = Path(__file__).resolve().parent.parent
PAGE = DEMO / "index.html"

TOP_LINKS = [
    ("SKILL.MD", "https://my.nandaindex.org/"),
    ("NANDA Index", "https://nandaindex.org/"),
    ("Agent Box", "https://agentboxnanda.org/"),
]
PROMPTS = [
    "Set me up at my.nandaindex.org using [my email].",
    "My code is [six-digit code].",
    "Find [Muse’s agent address] on NANDA and say hello.",
    "Check my Agent Box.",
    "Reply: Hello back!",
    "Check for replies in my Agent Box.",
]
PUBLIC_ANCHORS = ["prompts", "why", "help"]  # hash links from the earlier published page
OLD_IDENTITIES = ["Wajo Demo", "Muse Demo", "you+muse", "you+wajo", "October 14, 2026", "screenshots/0"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.problems, self.ids, self.hrefs = [], [], [], []
        self.assets, self.imgs, self.videos, self.tracks, self.navs = [], [], [], [], 0
        self.header_links, self.prompts, self.text = [], [], []
        self._in_header = self._in_prompt = self._in_script = self._in_style = 0
        self._link = None
        self._prompt = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "nav":
            self.navs += 1
        if tag == "header":
            self._in_header += 1
        if tag in ("script",):
            self._in_script += 1
        if tag == "style":
            self._in_style += 1
        if tag == "a":
            self.hrefs.append(a.get("href", ""))
            if self._in_header:
                self._link = [a.get("href", ""), ""]
        if tag == "p" and "prompt" in (a.get("class") or "").split():
            self._in_prompt, self._prompt = 1, []
        for key in ("src", "poster"):
            if a.get(key):
                self.assets.append((tag, a[key]))
        if tag == "a" and a.get("href") and not re.match(r"^(https?:|#|mailto:)", a["href"]):
            self.assets.append(("a", a["href"]))
        if tag == "img":
            self.imgs.append(a)
        if tag == "video":
            self.videos.append(a)
        if tag == "track":
            self.tracks.append(a)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.problems.append(f"unexpected </{tag}> (open: {'/'.join(self.stack[-3:])})")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
            return
        self.stack.pop()
        if tag == "header":
            self._in_header -= 1
        if tag == "script":
            self._in_script -= 1
        if tag == "style":
            self._in_style -= 1
        if tag == "a" and self._link is not None:
            self.header_links.append((self._link[1].strip(), self._link[0]))
            self._link = None
        if tag == "p" and self._in_prompt:
            self.prompts.append("".join(self._prompt).strip())
            self._in_prompt = 0

    def handle_data(self, data):
        if self._link is not None:
            self._link[1] += data
        if self._in_prompt:
            self._prompt.append(data)
        if not self._in_script and not self._in_style:
            self.text.append(data)


def ffprobe(path: Path) -> dict | None:
    if not shutil.which("ffprobe"):
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:stream=codec_type,codec_name,width,height,pix_fmt",
                          "-of", "json", str(path)], capture_output=True, text=True)
    return json.loads(out.stdout) if out.returncode == 0 else None


def moov_first(path: Path) -> bool:
    data = path.read_bytes()[:1 << 20]
    m, d = data.find(b"moov"), data.find(b"mdat")
    return m != -1 and (d == -1 or m < d)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--publish", action="store_true", help="fail on any pending asset")
    args = ap.parse_args()
    results: list[tuple[str, str, str]] = []
    add = lambda status, name, detail="": results.append((status, name, detail))

    html = PAGE.read_text(encoding="utf-8")
    p = Page()
    p.feed(html)
    p.close()
    add("FAIL" if p.problems or p.stack else "PASS", "markup nesting",
        "; ".join(p.problems[:5]) or (f"unclosed: {p.stack}" if p.stack else "balanced"))
    dupes = sorted({i for i in p.ids if p.ids.count(i) > 1})
    add("FAIL" if dupes else "PASS", "unique ids", ", ".join(dupes) or f"{len(p.ids)} ids")
    missing_anchor = [h for h in p.hrefs if h.startswith("#") and h[1:] not in p.ids]
    add("FAIL" if missing_anchor else "PASS", "in-page links", ", ".join(missing_anchor) or "all targets exist")
    lost = [a for a in PUBLIC_ANCHORS if a not in p.ids]
    add("FAIL" if lost else "PASS", "earlier public anchors", ", ".join("#" + a for a in lost) or "#prompts, #why, #help kept")
    add("PASS" if p.header_links == TOP_LINKS and p.navs == 1 else "FAIL", "top links",
        f"{p.header_links}, {p.navs} nav element(s)")
    add("PASS" if p.prompts == PROMPTS else "FAIL", "prompts exact and in order",
        "6 of 6 match" if p.prompts == PROMPTS else f"found {p.prompts}")
    v = p.videos[0] if p.videos else {}
    video_ok = (len(p.videos) == 1 and "controls" in v and "autoplay" not in v and v.get("poster")
                and v.get("preload") in ("metadata", "none")
                and any(t.get("kind") == "captions" and t.get("srclang") and t.get("src") for t in p.tracks))
    add("PASS" if video_ok else "FAIL", "video element", "controls, poster, captions track, no autoplay"
        if video_ok else f"video={v} tracks={p.tracks}")
    add("PASS" if "aspect-ratio:16/9" in html.replace(" ", "") else "FAIL", "16:9 player", "aspect-ratio rule")
    no_alt = [i.get("src") for i in p.imgs if not (i.get("alt") or "").strip() and i.get("id") != "dialog-image"]
    add("FAIL" if no_alt else "PASS", "image alt text", ", ".join(no_alt) or f"{len(p.imgs) - 1} screenshots")

    body_text = " ".join(" ".join(p.text).split())
    body_text = body_text.split("Theme adapted from projnanda")[0]
    dashes = [c for c in ("—", "–") if c in body_text]
    add("FAIL" if dashes else "PASS", "no em or en dashes in page text", "found" if dashes else "none")
    stale = [s for s in OLD_IDENTITIES if s in html]
    add("FAIL" if stale else "PASS", "no old demo identities", ", ".join(stale) or "none")
    add("FAIL" if "gmail" in body_text.lower() else "PASS", "no provider-specific email wording",
        "mentions Gmail" if "gmail" in body_text.lower() else "says personal email address")
    story = all(w in body_text for w in ("Alice uses Muse", "Bob uses Wajo", "nandaindex.org", "Agent Box"))
    add("PASS" if story else "FAIL", "intro and step 3 wording", "Alice/Muse, Bob/Wajo, manual search link")

    pending = []
    seen = set()
    for tag, ref in p.assets:
        ref = ref.split("#")[0]
        if not ref or ref.startswith(("http:", "https:", "data:")) or ref in seen:
            continue
        seen.add(ref)
        path = (DEMO / ref).resolve()
        if not path.exists():
            pending.append(ref)
            continue
        if path.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            try:
                from PIL import Image
                with Image.open(path) as im:
                    w, h = im.size
                poster = ref.endswith("-poster.jpg")
                ok = (w, h) == (1920, 1080) if poster else w >= 1200
                add("PASS" if ok else "WARN", f"image {ref}", f"{w}x{h}, {path.stat().st_size // 1024} KB"
                    + ("" if ok else (", expected 1920x1080" if poster else ", narrower than 1200 px")))
            except ImportError:
                add("PASS", f"image {ref}", f"present, {path.stat().st_size // 1024} KB")
        elif path.suffix.lower() == ".mp4":
            size_mb = path.stat().st_size / 1e6
            info = ffprobe(path)
            detail = f"{size_mb:.1f} MB"
            status = "FAIL" if size_mb >= 100 else ("WARN" if size_mb > 50 else "PASS")
            if info:
                dur = float(info["format"].get("duration", 0))
                vs = [s for s in info["streams"] if s["codec_type"] == "video"]
                au = [s for s in info["streams"] if s["codec_type"] == "audio"]
                detail += f", {dur:.1f} s"
                if dur > 180 or not vs or vs[0].get("codec_name") != "h264" or not au:
                    status = "FAIL"
                if vs:
                    detail += f", {vs[0].get('width')}x{vs[0].get('height')} {vs[0].get('codec_name')} {vs[0].get('pix_fmt')}"
            if not moov_first(path):
                status, detail = ("FAIL" if status == "FAIL" else "WARN"), detail + ", not faststart"
            add(status, f"video {ref}", detail)
        elif path.suffix.lower() == ".vtt":
            text = path.read_text(encoding="utf-8", errors="replace")
            cues = text.count("-->")
            bad = "nanda" in text.lower()
            ok = text.lstrip("﻿").startswith("WEBVTT") and cues > 0 and not bad
            add("PASS" if ok else "FAIL", f"captions {ref}",
                f"{cues} cues" + (", contains the word nanda" if bad else ""))
        else:
            add("PASS", f"asset {ref}", "present")
    if pending:
        add("FAIL" if args.publish else "PENDING", "assets still missing", ", ".join(pending))

    width = max(len(n) for _, n, _ in results)
    for status, name, detail in results:
        print(f"{status:<8} {name:<{width}}  {detail}")
    counts = {s: sum(1 for r in results if r[0] == s) for s in ("PASS", "WARN", "PENDING", "FAIL")}
    print("summary:", ", ".join(f"{k} {v}" for k, v in counts.items() if v))
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
