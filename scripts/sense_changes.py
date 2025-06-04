#!/usr/bin/env python3
"""
Gamma Delta Sense CLI Tool
=========================

Command-line interface for your sensing system.
Save this as scripts/sense_changes.py
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add the parent directory to path so we can import sensing modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from sensing.gamma_detector import GammaDetector
    from sensing.delta_analyzer import DeltaAnalyzer
except ImportError as e:
    print(f"❌ Error importing sensing modules: {e}")
    print("Make sure you're running this from the gamma_delta_sense directory")
    sys.exit(1)


def cmd_gamma(args):
    """Run gamma (change) detection."""
    print("🔍 Running Gamma Detection...")
    print("-" * 40)
    
    detector = GammaDetector(kb_path=args.kb_path)
    results = detector.scan_for_changes()
    
    # Display results
    metrics = results["gamma_metrics"]
    print(f"📊 Scan Results ({results['scan_timestamp'][:19]})")
    print(f"  Total Files: {metrics['total_files']}")
    print(f"  Total Changes: {metrics['total_changes']}")
    print(f"  Change Rate: {metrics['change_rate']:.2%}")
    print()
    
    if results["new_files"]:
        print(f"✨ New Files ({len(results['new_files'])}):")
        for file in results["new_files"]:
            print(f"  + {file}")
        print()
    
    if results["deleted_files"]:
        print(f"🗑️  Deleted Files ({len(results['deleted_files'])}):")
        for file in results["deleted_files"]:
            print(f"  - {file}")
        print()
    
    if results["modified_files"]:
        print(f"📝 Modified Files ({len(results['modified_files'])}):")
        for mod in results["modified_files"]:
            size_change = mod["size_change"]
            size_indicator = f"(+{size_change})" if size_change > 0 else f"({size_change})" if size_change < 0 else "(same size)"
            print(f"  ~ {mod['file']} {size_indicator}")
        print()
    
    # Show trends if available
    trends = detector.get_change_trends()
    if trends.get("status") != "insufficient_data":
        print(f"📈 Change Trends (last {trends['window_size']} scans):")
        print(f"  Average Rate: {trends['average_change_rate']:.2%}")
        print(f"  Trend: {trends['trend_direction']}")
        print(f"  Total Changes: {trends['total_changes_in_window']}")
    
    # Save detailed results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Detailed results saved to: {args.output}")


def cmd_delta(args):
    """Run delta (difference) analysis."""
    print("📊 Running Delta Analysis...")
    print("-" * 40)
    
    analyzer = DeltaAnalyzer(kb_path=args.kb_path)
    results = analyzer.analyze_fact_rule_pairs()
    
    # Display summary
    summary = results["summary"]
    print(f"📋 Analysis Summary ({results['analysis_timestamp'][:19]})")
    print(f"  Total Pairs: {summary['total_pairs_found']}")
    print(f"  Complete Pairs: {summary['complete_pairs']}")
    print(f"  Incomplete Pairs: {summary['incomplete_pairs']}")
    print(f"  Average Similarity: {summary['average_similarity']:.2%}")
    print()
    
    # Show incomplete pairs
    incomplete_pairs = []
    low_similarity_pairs = []
    
    for pair_id, analysis in results["pair_analyses"].items():
        if not (analysis["fact_exists"] and analysis["rule_exists"]):
            incomplete_pairs.append((pair_id, analysis))
        elif analysis["consistency_score"] < 0.5:
            low_similarity_pairs.append((pair_id, analysis))
    
    if incomplete_pairs:
        print(f"⚠️  Incomplete Pairs ({len(incomplete_pairs)}):")
        for pair_id, analysis in incomplete_pairs:
            missing = []
            if not analysis["fact_exists"]:
                missing.append("fact")
            if not analysis["rule_exists"]:
                missing.append("rule")
            print(f"  {pair_id}: Missing {', '.join(missing)}")
        print()
    
    if low_similarity_pairs:
        print(f"🔍 Low Similarity Pairs ({len(low_similarity_pairs)}):")
        for pair_id, analysis in low_similarity_pairs:
            score = analysis["consistency_score"]
            print(f"  {pair_id}: {score:.1%} similarity")
        print()
    
    # Show recommendations
    if results["recommendations"]:
        print("💡 Recommendations:")
        for rec in results["recommendations"]:
            print(f"  - {rec}")
        print()
    
    # Detailed analysis for specific pair
    if args.detail and args.detail in results["pair_analyses"]:
        print(f"🔬 Detailed Analysis for Pair {args.detail}:")
        analysis = results["pair_analyses"][args.detail]
        
        if "content_analysis" in analysis:
            ca = analysis["content_analysis"]
            print(f"  Similarity Score: {ca['similarity_score']:.2%}")
            print(f"  Word Overlap: {ca['word_overlap_count']} words")
            print(f"  Unique to Fact: {ca['unique_words_in_fact']} words")
            print(f"  Unique to Rule: {ca['unique_words_in_rule']} words")
        
        if analysis["issues"]:
            print(f"  Issues: {', '.join(analysis['issues'])}")
    
    # Save detailed results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Detailed results saved to: {args.output}")


def cmd_status(args):
    """Show overall system status."""
    print("📊 Gamma Delta Sense System Status")
    print("=" * 40)
    
    kb_path = Path(args.kb_path)
    facts_path = kb_path / "facts"
    rules_path = kb_path / "rules"
    
    # Basic directory status
    print("📁 Directory Status:")
    print(f"  Knowledge Base: {kb_path} ({'✅' if kb_path.exists() else '❌'})")
    print(f"  Facts: {facts_path} ({'✅' if facts_path.exists() else '❌'})")
    print(f"  Rules: {rules_path} ({'✅' if rules_path.exists() else '❌'})")
    print()
    
    # File counts
    if facts_path.exists() and rules_path.exists():
        fact_files = list(facts_path.glob("*.txt"))
        rule_files = list(rules_path.glob("*.txt"))
        
        print("📈 File Statistics:")
        print(f"  Fact Files: {len(fact_files)}")
        print(f"  Rule Files: {len(rule_files)}")
        print(f"  Total Files: {len(fact_files) + len(rule_files)}")
        print()
        
        # Quick analysis
        print("🔍 Quick Analysis:")
        
        # Gamma detection
        try:
            detector = GammaDetector(kb_path=args.kb_path)
            gamma_results = detector.scan_for_changes()
            metrics = gamma_results["gamma_metrics"]
            print(f"  Change Rate: {metrics['change_rate']:.2%}")
            print(f"  Recent Changes: {metrics['total_changes']}")
        except Exception as e:
            print(f"  Gamma Detection: Error ({e})")
        
        # Delta analysis
        try:
            analyzer = DeltaAnalyzer(kb_path=args.kb_path)
            delta_results = analyzer.analyze_fact_rule_pairs()
            summary = delta_results["summary"]
            print(f"  Complete Pairs: {summary['complete_pairs']}/{summary['total_pairs_found']}")
            print(f"  Average Similarity: {summary['average_similarity']:.2%}")
        except Exception as e:
            print(f"  Delta Analysis: Error ({e})")


def cmd_validate(args):
    """Run comprehensive validation (combines gamma + delta)."""
    print("✅ Running Comprehensive Validation")
    print("=" * 40)
    
    # Run gamma detection
    print("1️⃣ Gamma Detection (Change Analysis)")
    detector = GammaDetector(kb_path=args.kb_path)
    gamma_results = detector.scan_for_changes()
    gamma_metrics = gamma_results["gamma_metrics"]
    
    print(f"   Changes detected: {gamma_metrics['total_changes']}")
    print(f"   Change rate: {gamma_metrics['change_rate']:.2%}")
    
    # Run delta analysis
    print("\n2️⃣ Delta Analysis (Content Consistency)")
    analyzer = DeltaAnalyzer(kb_path=args.kb_path)
    delta_results = analyzer.analyze_fact_rule_pairs()
    delta_summary = delta_results["summary"]
    
    print(f"   Complete pairs: {delta_summary['complete_pairs']}")
    print(f"   Incomplete pairs: {delta_summary['incomplete_pairs']}")
    print(f"   Average similarity: {delta_summary['average_similarity']:.2%}")
    
    # Overall assessment
    print("\n🎯 Overall Assessment:")
    
    issues = []
    if gamma_metrics['change_rate'] > 0.2:
        issues.append("High change rate detected")
    
    if delta_summary['incomplete_pairs'] > 0:
        issues.append(f"{delta_summary['incomplete_pairs']} incomplete pairs")
    
    if delta_summary['average_similarity'] < 0.5:
        issues.append("Low average content similarity")
    
    if issues:
        print("   ⚠️  Issues found:")
        for issue in issues:
            print(f"      - {issue}")
        exit_code = 1
    else:
        print("   ✅ All checks passed!")
        exit_code = 0
    
    # Save comprehensive report
    if args.output:
        report = {
            "validation_timestamp": datetime.now().isoformat(),
            "gamma_results": gamma_results,
            "delta_results": delta_results,
            "issues": issues,
            "status": "failed" if issues else "passed"
        }
        
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Comprehensive report saved to: {args.output}")
    
    return exit_code


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Gamma Delta Sensing System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/sense_changes.py gamma                    # Detect changes
  python scripts/sense_changes.py delta                    # Analyze differences  
  python scripts/sense_changes.py status                   # Show system status
  python scripts/sense_changes.py validate                 # Full validation
  python scripts/sense_changes.py delta --detail 1         # Detailed analysis for pair 1
  python scripts/sense_changes.py gamma --output report.json  # Save results to file
        """
    )
    
    parser.add_argument(
        "--kb-path", 
        default="kb",
        help="Path to knowledge base directory (default: kb)"
    )
    
    parser.add_argument(
        "--output", 
        help="Save detailed results to JSON file"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Gamma command
    gamma_parser = subparsers.add_parser('gamma', help='Run gamma (change) detection')
    
    # Delta command  
    delta_parser = subparsers.add_parser('delta', help='Run delta (difference) analysis')
    delta_parser.add_argument('--detail', help='Show detailed analysis for specific pair ID')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Run comprehensive validation')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'gamma':
            cmd_gamma(args)
        elif args.command == 'delta':
            cmd_delta(args)
        elif args.command == 'status':
            cmd_status(args)
        elif args.command == 'validate':
            exit_code = cmd_validate(args)
            sys.exit(exit_code)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if hasattr(args, 'debug') and args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

