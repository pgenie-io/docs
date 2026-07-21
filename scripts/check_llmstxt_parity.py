#!/usr/bin/env python3
"""Fail if mkdocs.yml's nav and llmstxt-md sections cover different .md files."""

import sys
from pathlib import Path

import yaml

MKDOCS_YML = Path(__file__).resolve().parent.parent / "mkdocs.yml"


class _IgnoreUnknownTagsLoader(yaml.SafeLoader):
    pass


_IgnoreUnknownTagsLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:", lambda loader, suffix, node: suffix
)


def collect_nav_files(nav):
    files = set()
    for entry in nav:
        if isinstance(entry, str):
            files.add(entry)
        elif isinstance(entry, dict):
            for value in entry.values():
                if isinstance(value, str):
                    files.add(value)
                elif isinstance(value, list):
                    files |= collect_nav_files(value)
    return files


def collect_section_files(sections):
    files = set()
    for entries in sections.values():
        for entry in entries or []:
            if isinstance(entry, str):
                files.add(entry)
            elif isinstance(entry, dict):
                files |= set(entry.keys())
    return files


def find_llmstxt_md_config(plugins):
    for plugin in plugins:
        if isinstance(plugin, dict) and "llmstxt-md" in plugin:
            return plugin["llmstxt-md"] or {}
    return None


def main():
    config = yaml.load(MKDOCS_YML.read_text(), Loader=_IgnoreUnknownTagsLoader)
    nav_files = collect_nav_files(config["nav"])

    llmstxt_md_config = find_llmstxt_md_config(config.get("plugins", []))
    if llmstxt_md_config is None:
        print("mkdocs.yml has no llmstxt-md plugin configured", file=sys.stderr)
        return 1
    section_files = collect_section_files(llmstxt_md_config.get("sections", {}))

    missing_from_sections = nav_files - section_files
    missing_from_nav = section_files - nav_files

    if missing_from_sections or missing_from_nav:
        if missing_from_sections:
            print(
                "Pages in nav but missing from llmstxt-md sections:",
                file=sys.stderr,
            )
            for f in sorted(missing_from_sections):
                print(f"  - {f}", file=sys.stderr)
        if missing_from_nav:
            print(
                "Pages in llmstxt-md sections but missing from nav:",
                file=sys.stderr,
            )
            for f in sorted(missing_from_nav):
                print(f"  - {f}", file=sys.stderr)
        return 1

    print(f"nav and llmstxt-md sections match ({len(nav_files)} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
