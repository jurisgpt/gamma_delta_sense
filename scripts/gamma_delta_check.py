#!/usr/bin/env python3
"""
Simple Gamma/Delta Check - builds on your existing validator
"""
import os
from pathlib import Path

def check_fact_rule_pairs(kb_path="../kb"):
    """Check for matching fact/rule pairs."""
    facts_dir = Path(kb_path) / "facts" 
    rules_dir = Path(kb_path) / "rules"
    
    if not facts_dir.exists() or not rules_dir.exists():
        print("❌ Missing facts or rules directory")
        return
    
    fact_files = {f.stem.replace('fact', ''): f for f in facts_dir.glob('fact*.txt')}
    rule_files = {f.stem.replace('rule', ''): f for f in rules_dir.glob('rule*.txt')}
    
    all_ids = set(fact_files.keys()) | set(rule_files.keys())
    
    print(f"📊 Found {len(all_ids)} knowledge units")
    
    for id in sorted(all_ids):
        has_fact = id in fact_files
        has_rule = id in rule_files
        status = "✅" if has_fact and has_rule else "⚠️"
        print(f"{status} Unit {id}: fact={has_fact}, rule={has_rule}")

if __name__ == "__main__":
    check_fact_rule_pairs()
