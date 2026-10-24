#!/usr/bin/env python3
"""Respectfully export the Marxists Internet Archive glossary to JSONL, JSON, and CSV.

The crawler discovers real term-page links from the A-Z glossary indexes, sleeps
one second between successful page requests, and can resume from its JSONL
checkpoint after an interruption.
"""

from __future__ import annotations

import csv
import html as html_lib
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen

from lxml import html


BASE = "https://www.marxists.org/glossary/"
TERMS_PREFIX = BASE + "terms/"
INDEX_URLS = [urljoin(BASE, f"{letter}.htm") for letter in "abcdefghijklmnopqrstuvwxyz"]
OUTPUT = Path("output/mia_glossary")
JSONL_PATH = OUTPUT / "glossary_terms.jsonl"
JSON_PATH = OUTPUT / "glossary_terms.json"
CSV_PATH = OUTPUT / "glossary_terms.csv"
STATE_PATH = OUTPUT / "crawl_state.json"
ERROR_PATH = OUTPUT / "crawl_errors.jsonl"
REQUEST_DELAY_SECONDS = 1.0
USER_AGENT = "CodexGlossaryResearch/1.0 (respectful educational export; +https://www.marxists.org/)"


def normalise_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def canonical_url(value: str) -> str:
    """Normalize only what is needed for deduplication, retaining anchors."""
    parsed = urlparse(value)
    return parsed._replace(fragment=unquote(parsed.fragment)).geturl()


def fetch(url: str, attempts: int = 4) -> str:
    """Fetch UTF-8/Latin-1 HTML with retries; throttle is handled by the caller."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
            with urlopen(request, timeout=45) as response:
                data = response.read()
                charset = response.headers.get_content_charset() or "utf-8"
            try:
                return data.decode(charset, errors="replace")
            except LookupError:
                return data.decode("latin-1", errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Could not fetch {url}: {last_error}")


def is_term_url(url: str) -> bool:
    bare, _ = urldefrag(url)
    return bare.startswith(TERMS_PREFIX) and bare.lower().endswith((".htm", ".html"))


def discover_term_links(index_html: str, index_url: str) -> Iterable[str]:
    tree = html.fromstring(index_html)
    for href in tree.xpath("//a[@href]/@href"):
        absolute = canonical_url(urljoin(index_url, href))
        if is_term_url(absolute):
            yield absolute


def marker_nodes(tree, requested_anchors: set[str]):
    """Find entry anchor elements requested by the master alphabetical indexes."""
    result = []
    for node in tree.xpath("//*[@id or @name]"):
        marker = unquote(node.get("id") or node.get("name") or "")
        if marker in requested_anchors:
            result.append((marker, node))
    return result


def heading_for(marker):
    tag = marker.tag.lower() if isinstance(marker.tag, str) else ""
    if re.fullmatch(r"h[1-6]", tag):
        return marker
    parent = marker.getparent()
    if parent is not None and isinstance(parent.tag, str) and re.fullmatch(r"h[1-6]", parent.tag.lower()):
        return parent
    for candidate in marker.itersiblings():
        if not isinstance(candidate.tag, str):
            continue
        tag = candidate.tag.lower()
        if tag in {"script", "style"}:
            continue
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "b", "strong"}:
            return candidate
    return marker


def fragment_between(start, end) -> tuple[str, str]:
    """Return complete sibling blocks between entry starts, excluding navigation."""
    blocks = []
    node = start
    while node is not None and node is not end:
        if isinstance(node.tag, str) and node.tag.lower() not in {"script", "style", "nav", "footer"}:
            classes = node.get("class", "")
            if "footer" not in classes.lower() and "nav" not in classes.lower():
                blocks.append(html.tostring(node, encoding="unicode", method="html"))
        node = node.getnext()
    if not blocks:
        text = normalise_whitespace(" ".join(start.itertext()))
        return "", text
    fragment = "\n".join(blocks)
    parsed = html.fragment_fromstring(f"<section>{fragment}</section>", create_parent=False)
    text = normalise_whitespace(" ".join(parsed.itertext()))
    return fragment, text


def clean_term(heading) -> str:
    term = normalise_whitespace(" ".join(heading.itertext()))
    term = re.sub(r"\s*(?:\[\d+\]|\d+)$", "", term).strip()
    return term


def extract_entries(page_html: str, page_url: str, anchors: set[str]) -> list[dict]:
    tree = html.fromstring(page_html)
    for bad in tree.xpath("//script|//style"):
        bad.drop_tree()
    starts = []
    seen = set()
    for anchor, marker in marker_nodes(tree, anchors):
        if anchor in seen:
            continue
        seen.add(anchor)
        heading = heading_for(marker)
        starts.append((anchor, marker, heading))
    starts.sort(key=lambda item: item[1].sourceline or 0)
    entries = []
    for i, (anchor, marker, heading) in enumerate(starts):
        next_marker = starts[i + 1][1] if i + 1 < len(starts) else None
        start_block = heading
        while start_block.getparent() is not None and start_block.getparent().tag is not None:
            parent = start_block.getparent()
            if parent.tag.lower() in {"body", "main", "article"}:
                break
            # Prefer a meaningful direct child of the content container.
            start_block = parent
        definition_html, whole_text = fragment_between(start_block, next_marker)
        term = clean_term(heading)
        if not term:
            term = anchor.replace("-", " ").title()
        definition_text = whole_text
        # Remove the heading only when it is the first textual occurrence.
        if definition_text.casefold().startswith(term.casefold()):
            definition_text = definition_text[len(term):].lstrip(" :–—-\t")
        entries.append(
            {
                "term": term,
                "definition_html": definition_html,
                "definition_text": definition_text,
                "source_url": f"{page_url}#{anchor}",
                "anchor_id": anchor,
                "page_url": page_url,
            }
        )
    return entries


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_existing() -> tuple[dict[str, dict], set[str]]:
    entries = {}
    pages = set()
    if JSONL_PATH.exists():
        for line in JSONL_PATH.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            entry = json.loads(line)
            entries[entry["source_url"]] = entry
            pages.add(entry["page_url"])
    return entries, pages


def record_error(url: str, error: Exception) -> None:
    with ERROR_PATH.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"url": url, "error": str(error)}, ensure_ascii=False) + "\n")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    existing, complete_pages = load_existing()
    page_to_anchors: dict[str, set[str]] = defaultdict(set)

    print(f"Discovering links from {len(INDEX_URLS)} alphabetical indexes…", flush=True)
    for position, index_url in enumerate(INDEX_URLS, 1):
        try:
            page = fetch(index_url)
            for link in discover_term_links(page, index_url):
                term_page, anchor = urldefrag(link)
                if anchor:
                    page_to_anchors[canonical_url(term_page)].add(unquote(anchor))
            print(f"  {position:02d}/26 {index_url}", flush=True)
        except Exception as exc:
            record_error(index_url, exc)
            print(f"  ERROR {index_url}: {exc}", file=sys.stderr, flush=True)
        time.sleep(REQUEST_DELAY_SECONDS)

    state = {
        "index_urls": INDEX_URLS,
        "term_pages_discovered": len(page_to_anchors),
        "term_anchor_links_discovered": sum(map(len, page_to_anchors.values())),
        "request_delay_seconds": REQUEST_DELAY_SECONDS,
        "completed_pages_before_run": len(complete_pages),
    }
    write_json(STATE_PATH, state)
    print(f"Crawling {len(page_to_anchors)} term pages ({len(complete_pages)} already checkpointed)…", flush=True)

    with JSONL_PATH.open("a", encoding="utf-8") as stream:
        for position, (page_url, anchors) in enumerate(sorted(page_to_anchors.items()), 1):
            if page_url in complete_pages:
                continue
            try:
                source = fetch(page_url)
                page_entries = extract_entries(source, page_url, anchors)
                if not page_entries:
                    raise RuntimeError("No requested entry anchors found on page")
                for entry in page_entries:
                    if entry["source_url"] not in existing:
                        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
                        existing[entry["source_url"]] = entry
                stream.flush()
                complete_pages.add(page_url)
                print(f"  {position:03d}/{len(page_to_anchors):03d} {page_url} ({len(page_entries)} entries)", flush=True)
            except Exception as exc:
                record_error(page_url, exc)
                print(f"  ERROR {page_url}: {exc}", file=sys.stderr, flush=True)
            time.sleep(REQUEST_DELAY_SECONDS)

    entries = sorted(existing.values(), key=lambda entry: (entry["term"].casefold(), entry["source_url"]))
    write_json(JSON_PATH, entries)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as stream:
        columns = ["term", "definition_text", "definition_html", "source_url", "anchor_id", "page_url"]
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(entries)
    state.update({
        "completed_pages": len(complete_pages),
        "entries_exported": len(entries),
        "jsonl_path": str(JSONL_PATH),
        "json_path": str(JSON_PATH),
        "csv_path": str(CSV_PATH),
        "errors_path": str(ERROR_PATH),
    })
    write_json(STATE_PATH, state)
    print(json.dumps({"status": "complete", **state}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
