#!/usr/bin/env python3
"""
Sanity Check & Get Well Soon Script
==================================
Shows you exactly where you are and what exists.
"""

import os
from pathlib import Path

def sanity_check():
    print("🏥 SANITY CHECK & GET WELL SOON 🏥")
    print("=" * 50)
    
    # Where am I?
    current_dir = Path.cwd()
    print(f"📍 Current Directory: {current_dir}")
    
    # What's in this directory?
    print(f"\n📁 Contents of {current_dir.name}/:")
    for item in sorted(current_dir.iterdir()):
        if item.is_dir():
            print(f"  📂 {item.name}/")
        else:
            print(f"  📄 {item.name}")
    
    # Check for key directories
    print(f"\n🔍 Key Directory Check:")
    kb_dir = current_dir / "kb"
    scripts_dir = current_dir / "scripts" 
    
    if kb_dir.exists():
        print(f"  ✅ kb/ directory exists")
        facts_dir = kb_dir / "facts"
        rules_dir = kb_dir / "rules"
        
        if facts_dir.exists():
            fact_files = list(facts_dir.glob("*.txt"))
            print(f"     📊 facts/: {len(fact_files)} .txt files")
        else:
            print(f"     ❌ facts/ directory missing")
            
        if rules_dir.exists():
            rule_files = list(rules_dir.glob("*.txt"))
            print(f"     📊 rules/: {len(rule_files)} .txt files")
        else:
            print(f"     ❌ rules/ directory missing")
    else:
        print(f"  ❌ kb/ directory not found")
    
    if scripts_dir.exists():
        print(f"  ✅ scripts/ directory exists")
        gamma_script = scripts_dir / "gamma_delta_check.py"
        if gamma_script.exists():
            print(f"     ✅ gamma_delta_check.py exists")
        else:
            print(f"     ❌ gamma_delta_check.py missing")
    else:
        print(f"  ❌ scripts/ directory not found")
    
    # Quick gamma/delta check if everything exists
    if kb_dir.exists() and (kb_dir / "facts").exists() and (kb_dir / "rules").exists():
        print(f"\n🎯 Quick Gamma/Delta Check:")
        
        facts_dir = kb_dir / "facts"
        rules_dir = kb_dir / "rules"
        
        fact_files = {f.stem.replace('fact', ''): f for f in facts_dir.glob('fact*.txt')}
        rule_files = {f.stem.replace('rule', ''): f for f in rules_dir.glob('rule*.txt')}
        
        all_ids = set(fact_files.keys()) | set(rule_files.keys())
        
        if all_ids:
            print(f"   📊 Found {len(all_ids)} knowledge units")
            for id in sorted(all_ids):
                has_fact = id in fact_files
                has_rule = id in rule_files
                status = "✅" if has_fact and has_rule else "⚠️"
                print(f"   {status} Unit {id}: fact={has_fact}, rule={has_rule}")
        else:
            print(f"   📝 No fact*.txt or rule*.txt files found")
    
    print(f"\n💊 RECOMMENDATIONS:")
    if current_dir.name != "gamma_delta_sense":
        print(f"   🏃 Navigate to main directory: cd gamma_delta_sense")
    print(f"   🧪 Run gamma/delta check: python scripts/gamma_delta_check.py") 
    print(f"   🔧 Run this sanity check anytime: python sanity_check.py")
    
    print(f"\n🎉 You'll feel better soon! Keep it simple.")

if __name__ == "__main__":
    sanity_check()

