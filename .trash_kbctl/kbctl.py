#!/usr/bin/env python3
"""
kbctl.py — Knowledge Base Control CLI Engine

Performs indexing, policy enforcement, and validation of knowledge base content.
Engineered to NASA-grade reliability and readability.
"""

import os
import argparse
import yaml
from pathlib import Path
from typing import List, Dict

# Load file_rules.yaml for policy enforcement
def load_rules(rules_path: Path) -> Dict:
    if not rules_path.exists():
        raise FileNotFoundError(f"Missing file_rules.yaml at {rules_path}")
    with open(rules_path, "r") as f:
        return yaml.safe_load(f)

# Index files in a given directory
def index_directory(base_path: Path, subdirs: List[str]) -> Dict[str, List[str]]:
    index = {}
    for sub in subdirs:
        path = base_path / sub
        if not path.exists():
            raise FileNotFoundError(f"Directory '{sub}' not found in KB")
        files = sorted([f.name for f in path.glob("*.txt")])
        index[sub] = files
    return index

# Validate indexed files based on rules
def validate_index(index: Dict[str, List[str]], rules: Dict):
    all_ids = set()
    violations = []

    for rule in rules.get("expected_dirs", []):
        files = index.get(rule, [])
        ids = set(f.replace(".txt", "") for f in files)
        all_ids = all_ids.union(ids)

    for _id in sorted(all_ids):
        for rule in rules.get("expected_dirs", []):
            expected_file = f"{_id}.txt"
            if expected_file not in index.get(rule, []):
                violations.append(f"[MISSING] {expected_file} in {rule}")

    return violations

# CLI entry point
def main():
    parser = argparse.ArgumentParser(description="NASA-grade KB Index + Validator")
    parser.add_argument("command", choices=["index", "validate"], help="Command to run")
    parser.add_argument("--kb", default="kb", help="Base knowledge base path")
    parser.add_argument("--rules", default="kb/file_rules.yaml", help="Validation rules YAML file")
    args = parser.parse_args()

    kb_path = Path(args.kb)
    rules_path = Path(args.rules)

    # Load file rules
    rules = load_rules(rules_path)
    subdirs = rules.get("expected_dirs", [])

    # Index
    index = index_directory(kb_path, subdirs)

    if args.command == "index":
        print("📦 KB File Index:")
        for dir_name, files in index.items():
            for f in files:
                print(f"[{dir_name}] {f}")
    elif args.command == "validate":
        violations = validate_index(index, rules)
        if violations:
            print("❌ Validation Errors:")
            for v in violations:
                print(" -", v)
            exit(1)
        else:
            print("✅ All files validated successfully.")

if __name__ == "__main__":
    main()


