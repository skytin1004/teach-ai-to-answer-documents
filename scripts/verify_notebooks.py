"""Validate repository links, notebooks, and public-repo hygiene.

Use --execute to run notebooks in the current Python environment.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = ROOT / "articles"
NOTEBOOK_DIR = ROOT / "notebooks"
SKIPPED_DIR_NAMES = {
    ".git",
    "drafts",
    ".ipynb_checkpoints",
    "translated_images",
    "translations",
    "__pycache__",
}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
]


def is_skipped_path(path: Path) -> bool:
    relative_parts = path.relative_to(ROOT).parts
    return any(
        part in SKIPPED_DIR_NAMES or part.startswith(".venv")
        for part in relative_parts
    )


def iter_markdown_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*.md")
        if not is_skipped_path(path)
    )


def iter_secret_scan_files() -> list[Path]:
    allowed_suffixes = {
        ".env",
        ".example",
        ".gitattributes",
        ".gitignore",
        ".ipynb",
        ".jsonl",
        ".md",
        ".py",
        ".txt",
        ".yaml",
        ".yml",
    }
    return sorted(
        path for path in ROOT.rglob("*")
        if path.is_file()
        and not is_skipped_path(path)
        and (path.suffix in allowed_suffixes or path.name in {".env.example"})
    )


def check_local_links() -> None:
    missing: list[tuple[Path, str, Path]] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")

    for file_path in iter_markdown_files():
        text = file_path.read_text(encoding="utf-8")
        for match in link_pattern.finditer(text):
            raw_link = match.group(1)
            if raw_link.startswith(("http://", "https://", "mailto:")):
                continue
            if raw_link.startswith(("./translations", "./translated_images")):
                continue

            target = (file_path.parent / raw_link).resolve()
            if not target.exists():
                missing.append((file_path, raw_link, target))

    if missing:
        print("Missing local links:")
        for file_path, raw_link, target in missing:
            print(f"- {file_path.relative_to(ROOT)}: {raw_link} -> {target}")
        raise SystemExit(1)

    print("Local markdown links passed")


def validate_notebooks() -> list[Path]:
    notebooks = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    for notebook_path in notebooks:
        notebook = nbformat.read(notebook_path, as_version=4)
        nbformat.validate(notebook)
        print(f"{notebook_path.relative_to(ROOT)} validation passed")
    return notebooks


def check_notebook_cleanliness(notebooks: list[Path]) -> None:
    dirty_notebooks: list[str] = []
    for notebook_path in notebooks:
        notebook = nbformat.read(notebook_path, as_version=4)
        output_count = sum(
            len(cell.get("outputs", []))
            for cell in notebook.cells
            if cell.cell_type == "code"
        )
        executed_count = sum(
            1
            for cell in notebook.cells
            if cell.cell_type == "code" and cell.get("execution_count") is not None
        )
        if output_count or executed_count:
            dirty_notebooks.append(
                f"{notebook_path.relative_to(ROOT)} "
                f"(outputs={output_count}, executed_cells={executed_count})"
            )

    if dirty_notebooks:
        print("Notebooks contain saved outputs or execution counts:")
        for notebook in dirty_notebooks:
            print(f"- {notebook}")
        raise SystemExit(1)

    print("Notebook output cleanliness passed")


def check_high_risk_secret_patterns() -> None:
    findings: list[tuple[Path, int, str]] = []
    for path in iter_secret_scan_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                findings.append((path, line_number, line.strip()))

    if findings:
        print("High-risk secret patterns found:")
        for path, line_number, line in findings:
            print(f"- {path.relative_to(ROOT)}:{line_number}: {line}")
        raise SystemExit(1)

    print("High-risk secret pattern scan passed")


def execute_notebooks(notebooks: list[Path]) -> None:
    previous_cwd = Path.cwd()
    os.chdir(ROOT)
    try:
        for notebook_path in notebooks:
            notebook = nbformat.read(notebook_path, as_version=4)
            client = NotebookClient(notebook, timeout=180, kernel_name="python3")
            client.execute()
            print(f"{notebook_path.relative_to(ROOT)} execution passed")
    finally:
        os.chdir(previous_cwd)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute notebooks after validating links and notebook JSON.",
    )
    args = parser.parse_args()

    check_local_links()
    notebooks = validate_notebooks()
    check_notebook_cleanliness(notebooks)
    check_high_risk_secret_patterns()
    if args.execute:
        execute_notebooks(notebooks)


if __name__ == "__main__":
    main()
