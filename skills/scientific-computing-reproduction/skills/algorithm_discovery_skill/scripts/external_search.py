from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml


ARXIV_API = "https://export.arxiv.org/api/query"
GITHUB_REPO_SEARCH_API = "https://api.github.com/search/repositories"


def build_search_queries(task: dict) -> list[str]:
    domain = task.get("domain", {})
    metrics = task.get("metrics", {}).get("primary", {})
    parts = [
        domain.get("algorithm_family", ""),
        domain.get("problem_type", ""),
        domain.get("field", "").replace("_", " "),
    ]
    base = " ".join(part for part in parts if part).strip()
    metric = metrics.get("name", "")
    if not base:
        base = task.get("query", "computational mathematics optimization algorithm")
    queries = [
        f"{base} algorithm",
        f"{base} implementation code",
        f"{base} {metric} benchmark".strip(),
    ]
    return list(dict.fromkeys(query for query in queries if query))


def _get_json(url: str, timeout: int) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "computational-math-skills/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _get_text(url: str, timeout: int) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "computational-math-skills/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def search_arxiv(query: str, max_results: int = 5, timeout: int = 30) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
    )
    xml_text = _get_text(f"{ARXIV_API}?{params}", timeout)
    root = ET.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    results = []
    for entry in root.findall("atom:entry", ns):
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ns) or "").split())
        published = entry.findtext("atom:published", default="", namespaces=ns) or ""
        url = entry.findtext("atom:id", default="", namespaces=ns) or ""
        authors = [node.findtext("atom:name", default="", namespaces=ns) for node in entry.findall("atom:author", ns)]
        results.append(
            {
                "source": "arxiv",
                "title": title,
                "summary": summary,
                "url": url,
                "published": published,
                "authors": [author for author in authors if author],
                "query": query,
            }
        )
    return results


def search_github(query: str, max_results: int = 5, timeout: int = 30) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "q": f"{query} in:name,description,readme language:Python",
            "sort": "stars",
            "order": "desc",
            "per_page": max_results,
        }
    )
    data = _get_json(f"{GITHUB_REPO_SEARCH_API}?{params}", timeout)
    results = []
    for item in data.get("items", []):
        results.append(
            {
                "source": "github",
                "title": item.get("full_name") or item.get("name", ""),
                "summary": item.get("description") or "",
                "url": item.get("html_url", ""),
                "stars": item.get("stargazers_count", 0),
                "language": item.get("language"),
                "updated_at": item.get("updated_at"),
                "query": query,
            }
        )
    return results


def normalize_candidates(raw_candidates: list[dict]) -> list[dict]:
    seen = set()
    candidates = []
    for raw in raw_candidates:
        url = raw.get("url", "")
        title = " ".join(raw.get("title", "").split())
        key = (raw.get("source"), url or title.lower())
        if key in seen:
            continue
        seen.add(key)
        candidates.append(
            {
                "source": raw.get("source", "unknown"),
                "title": title,
                "summary": " ".join(raw.get("summary", "").split())[:1200],
                "url": url,
                "metadata": {key: value for key, value in raw.items() if key not in {"source", "title", "summary", "url"}},
            }
        )
    return candidates


def discover_external_algorithms(task_file: Path | str, out: Path | str, sources: list[str] | None = None, max_results: int = 5, timeout: int = 30) -> dict:
    task_file = Path(task_file)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    task = yaml.safe_load(task_file.read_text())
    queries = build_search_queries(task)
    sources = sources or ["arxiv", "github"]
    raw: list[dict] = []
    failures = []
    last_arxiv_request = 0.0
    for query in queries:
        if "arxiv" in sources:
            try:
                elapsed = time.monotonic() - last_arxiv_request
                if last_arxiv_request and elapsed < 3.2:
                    time.sleep(3.2 - elapsed)
                raw.extend(search_arxiv(query, max_results=max_results, timeout=timeout))
                last_arxiv_request = time.monotonic()
            except Exception as exc:
                last_arxiv_request = time.monotonic()
                failures.append({"source": "arxiv", "query": query, "error": str(exc)})
        if "github" in sources:
            try:
                raw.extend(search_github(query, max_results=max_results, timeout=timeout))
            except Exception as exc:
                failures.append({"source": "github", "query": query, "error": str(exc)})
    result = {
        "queries": queries,
        "sources": sources,
        "candidates": normalize_candidates(raw),
        "failures": failures,
    }
    (out / "algorithm_candidates.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--sources", default="arxiv,github")
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    result = discover_external_algorithms(
        args.task,
        args.out,
        sources=[item.strip() for item in args.sources.split(",") if item.strip()],
        max_results=args.max_results,
        timeout=args.timeout,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
