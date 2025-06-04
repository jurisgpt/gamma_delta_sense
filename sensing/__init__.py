#!/usr/bin/env python3
"""
Core Sensing System Files for Gamma Delta Sense
===============================================

These are the essential files for your sensing/ directory.
Save each section as the indicated filename.
"""

# =============================================================================
# FILE: sensing/__init__.py
# =============================================================================
"""
Gamma Delta Sensing System

Provides change detection (gamma) and difference analysis (delta) 
for knowledge base files.
"""

from .gamma_detector import GammaDetector
from .delta_analyzer import DeltaAnalyzer
from .file_monitor import FileMonitor
from .indexer import KnowledgeIndexer

__version__ = "1.0.0"
__all__ = ["GammaDetector", "DeltaAnalyzer", "FileMonitor", "KnowledgeIndexer"]

# =============================================================================
# FILE: sensing/gamma_detector.py  
# =============================================================================
"""
Gamma Detection: Rate of Change Analysis

Monitors and detects changes in your knowledge base files.
Designed specifically for your kb/facts and kb/rules structure.
"""

import os
import time
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FileState:
    """Represents the state of a file for change detection."""
    path: str
    size: int
    modified_time: float
    content_hash: str
    last_checked: float = 0.0
    
    @classmethod
    def from_file(cls, file_path: Path) -> 'FileState':
        """Create FileState from actual file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = file_path.stat()
        content_hash = cls._calculate_hash(file_path)
        
        return cls(
            path=str(file_path),
            size=stat.st_size,
            modified_time=stat.st_mtime,
            content_hash=content_hash,
            last_checked=time.time()
        )
    
    @staticmethod
    def _calculate_hash(file_path: Path) -> str:
        """Calculate SHA-256 hash of file content."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""
    
    def has_changed(self, current_state: 'FileState') -> bool:
        """Check if file has changed compared to current state."""
        return (
            self.content_hash != current_state.content_hash or
            self.size != current_state.size or
            self.modified_time != current_state.modified_time
        )


class GammaDetector:
    """
    Gamma (Change Rate) Detection System
    
    Monitors your kb/facts and kb/rules directories for changes
    and calculates change rates over time.
    """
    
    def __init__(self, kb_path: str = "kb"):
        self.kb_path = Path(kb_path)
        self.facts_path = self.kb_path / "facts"
        self.rules_path = self.kb_path / "rules"
        
        # State tracking
        self.baseline_states: Dict[str, FileState] = {}
        self.change_history: List[Dict] = []
        self.state_file = ".gamma_detector_state.json"
        
        # Load previous state if exists
        self._load_state()
    
    def scan_for_changes(self) -> Dict[str, any]:
        """
        Scan knowledge base for changes since last check.
        
        Returns:
            Dictionary with change detection results
        """
        scan_time = time.time()
        results = {
            "scan_timestamp": datetime.now().isoformat(),
            "changes_detected": {},
            "new_files": [],
            "deleted_files": [],
            "modified_files": [],
            "gamma_metrics": {}
        }
        
        # Scan both facts and rules directories
        current_files = {}
        
        for directory, dir_name in [(self.facts_path, "facts"), (self.rules_path, "rules")]:
            if directory.exists():
                for file_path in directory.glob("*.txt"):
                    file_key = str(file_path.relative_to(self.kb_path))
                    try:
                        current_files[file_key] = FileState.from_file(file_path)
                    except Exception as e:
                        print(f"Warning: Could not read {file_path}: {e}")
        
        # Compare with baseline
        baseline_keys = set(self.baseline_states.keys())
        current_keys = set(current_files.keys())
        
        # Detect new files
        new_files = current_keys - baseline_keys
        results["new_files"] = list(new_files)
        
        # Detect deleted files
        deleted_files = baseline_keys - current_keys
        results["deleted_files"] = list(deleted_files)
        
        # Detect modified files
        modified_files = []
        for file_key in baseline_keys & current_keys:
            baseline_state = self.baseline_states[file_key]
            current_state = current_files[file_key]
            
            if baseline_state.has_changed(current_state):
                modified_files.append({
                    "file": file_key,
                    "old_hash": baseline_state.content_hash[:8],
                    "new_hash": current_state.content_hash[:8],
                    "size_change": current_state.size - baseline_state.size
                })
        
        results["modified_files"] = modified_files
        
        # Calculate gamma metrics (change rates)
        total_files = len(current_files)
        total_changes = len(new_files) + len(deleted_files) + len(modified_files)
        
        results["gamma_metrics"] = {
            "total_files": total_files,
            "total_changes": total_changes,
            "change_rate": total_changes / total_files if total_files > 0 else 0,
            "files_added": len(new_files),
            "files_deleted": len(deleted_files),
            "files_modified": len(modified_files)
        }
        
        # Update baseline and save state
        self.baseline_states = current_files
        self.change_history.append(results)
        self._save_state()
        
        return results
    
    def get_change_trends(self, window_size: int = 10) -> Dict[str, any]:
        """
        Analyze change trends over recent scans.
        
        Args:
            window_size: Number of recent scans to analyze
            
        Returns:
            Trend analysis results
        """
        if len(self.change_history) < 2:
            return {"status": "insufficient_data", "scans_available": len(self.change_history)}
        
        recent_scans = self.change_history[-window_size:]
        
        change_rates = [scan["gamma_metrics"]["change_rate"] for scan in recent_scans]
        total_changes = [scan["gamma_metrics"]["total_changes"] for scan in recent_scans]
        
        trends = {
            "window_size": len(recent_scans),
            "average_change_rate": sum(change_rates) / len(change_rates),
            "max_change_rate": max(change_rates),
            "min_change_rate": min(change_rates),
            "total_changes_in_window": sum(total_changes),
            "trend_direction": self._calculate_trend(change_rates)
        }
        
        return trends
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate if trend is increasing, decreasing, or stable."""
        if len(values) < 3:
            return "unknown"
        
        # Simple linear trend calculation
        recent_avg = sum(values[-3:]) / 3
        earlier_avg = sum(values[:-3]) / len(values[:-3]) if len(values) > 3 else values[0]
        
        if recent_avg > earlier_avg * 1.1:
            return "increasing"
        elif recent_avg < earlier_avg * 0.9:
            return "decreasing"
        else:
            return "stable"
    
    def _load_state(self):
        """Load previous detection state."""
        if Path(self.state_file).exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self.baseline_states = {
                        k: FileState(**v) for k, v in data.get("baseline_states", {}).items()
                    }
                    self.change_history = data.get("change_history", [])
            except Exception as e:
                print(f"Warning: Could not load state file: {e}")
    
    def _save_state(self):
        """Save detection state."""
        try:
            data = {
                "baseline_states": {k: asdict(v) for k, v in self.baseline_states.items()},
                "change_history": self.change_history[-50:]  # Keep last 50 scans
            }
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save state file: {e}")


# =============================================================================
# FILE: sensing/delta_analyzer.py
# =============================================================================
"""
Delta Analysis: Content Difference Analysis

Analyzes differences between fact/rule pairs and content similarity.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
import difflib


@dataclass
class ContentAnalysis:
    """Results of content analysis between files."""
    similarity_score: float
    word_overlap: Set[str]
    unique_to_first: Set[str]
    unique_to_second: Set[str]
    line_differences: List[str]


@dataclass
class PairAnalysis:
    """Analysis results for a fact/rule pair."""
    fact_id: int
    fact_exists: bool
    rule_exists: bool
    content_analysis: Optional[ContentAnalysis] = None
    consistency_score: float = 0.0
    issues: List[str] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []


class DeltaAnalyzer:
    """
    Delta (Difference) Analysis System
    
    Analyzes content differences between your fact/rule pairs
    and identifies inconsistencies or missing relationships.
    """
    
    def __init__(self, kb_path: str = "kb"):
        self.kb_path = Path(kb_path)
        self.facts_path = self.kb_path / "facts"
        self.rules_path = self.kb_path / "rules"
    
    def analyze_fact_rule_pairs(self) -> Dict[str, any]:
        """
        Analyze all fact/rule pairs for content consistency.
        
        Returns:
            Comprehensive analysis results
        """
        results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "pair_analyses": {},
            "summary": {
                "total_pairs_found": 0,
                "complete_pairs": 0,
                "incomplete_pairs": 0,
                "average_similarity": 0.0
            },
            "recommendations": []
        }
        
        # Find all fact and rule files
        fact_files = self._get_numbered_files(self.facts_path, "fact")
        rule_files = self._get_numbered_files(self.rules_path, "rule")
        
        # Get all unique IDs
        all_ids = set(fact_files.keys()) | set(rule_files.keys())
        
        pair_analyses = []
        similarity_scores = []
        
        for file_id in sorted(all_ids):
            fact_path = fact_files.get(file_id)
            rule_path = rule_files.get(file_id)
            
            analysis = PairAnalysis(
                fact_id=file_id,
                fact_exists=fact_path is not None,
                rule_exists=rule_path is not None
            )
            
            # Check for missing files
            if not analysis.fact_exists:
                analysis.issues.append(f"Missing fact{file_id}.txt")
            if not analysis.rule_exists:
                analysis.issues.append(f"Missing rule{file_id}.txt")
            
            # Analyze content if both files exist
            if analysis.fact_exists and analysis.rule_exists:
                try:
                    fact_content = self._read_file(fact_path)
                    rule_content = self._read_file(rule_path)
                    
                    analysis.content_analysis = self._analyze_content_similarity(
                        fact_content, rule_content
                    )
                    analysis.consistency_score = analysis.content_analysis.similarity_score
                    similarity_scores.append(analysis.consistency_score)
                    
                    # Check for potential issues
                    if analysis.consistency_score < 0.3:
                        analysis.issues.append("Low content similarity between fact and rule")
                    
                except Exception as e:
                    analysis.issues.append(f"Error reading files: {e}")
            
            pair_analyses.append(analysis)
            results["pair_analyses"][file_id] = self._analysis_to_dict(analysis)
        
        # Calculate summary statistics
        complete_pairs = sum(1 for a in pair_analyses if a.fact_exists and a.rule_exists)
        incomplete_pairs = len(pair_analyses) - complete_pairs
        
        results["summary"] = {
            "total_pairs_found": len(pair_analyses),
            "complete_pairs": complete_pairs,
            "incomplete_pairs": incomplete_pairs,
            "average_similarity": sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
        }
        
        # Generate recommendations
        if incomplete_pairs > 0:
            results["recommendations"].append(f"Create missing files for {incomplete_pairs} incomplete pairs")
        
        low_similarity_pairs = [a for a in pair_analyses if a.consistency_score < 0.5]
        if low_similarity_pairs:
            results["recommendations"].append(
                f"Review {len(low_similarity_pairs)} pairs with low content similarity"
            )
        
        return results
    
    def _get_numbered_files(self, directory: Path, prefix: str) -> Dict[int, Path]:
        """Get numbered files (e.g., fact1.txt, rule2.txt) from directory."""
        files = {}
        if directory.exists():
            pattern = re.compile(rf"{prefix}(\d+)\.txt$")
            for file_path in directory.glob(f"{prefix}*.txt"):
                match = pattern.match(file_path.name)
                if match:
                    file_id = int(match.group(1))
                    files[file_id] = file_path
        return files
    
    def _read_file(self, file_path: Path) -> str:
        """Read file content with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception:
            return ""
    
    def _analyze_content_similarity(self, content1: str, content2: str) -> ContentAnalysis:
        """Analyze similarity between two pieces of content."""
        # Tokenize content
        words1 = set(re.findall(r'\w+', content1.lower()))
        words2 = set(re.findall(r'\w+', content2.lower()))
        
        # Calculate word overlap
        overlap = words1 & words2
        union = words1 | words2
        
        # Calculate similarity score
        similarity = len(overlap) / len(union) if union else 0.0
        
        # Generate line differences
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()
        diff = list(difflib.unified_diff(lines1, lines2, lineterm=""))
        
        return ContentAnalysis(
            similarity_score=similarity,
            word_overlap=overlap,
            unique_to_first=words1 - words2,
            unique_to_second=words2 - words1,
            line_differences=diff
        )
    
    def _analysis_to_dict(self, analysis: PairAnalysis) -> Dict:
        """Convert PairAnalysis to dictionary for serialization."""
        result = {
            "fact_id": analysis.fact_id,
            "fact_exists": analysis.fact_exists,
            "rule_exists": analysis.rule_exists,
            "consistency_score": analysis.consistency_score,
            "issues": analysis.issues
        }
        
        if analysis.content_analysis:
            result["content_analysis"] = {
                "similarity_score": analysis.content_analysis.similarity_score,
                "word_overlap_count": len(analysis.content_analysis.word_overlap),
                "unique_words_in_fact": len(analysis.content_analysis.unique_to_first),
                "unique_words_in_rule": len(analysis.content_analysis.unique_to_second)
            }
        
        return result


# =============================================================================
# FILE: sensing/config.yaml
# =============================================================================
"""
# Sensing System Configuration
# Save this as sensing/config.yaml

sensing:
  gamma_detection:
    enabled: true
    scan_interval_seconds: 60
    change_threshold: 0.1
    max_history_entries: 100
    
  delta_analysis:
    enabled: true
    similarity_threshold: 0.5
    content_comparison_enabled: true
    word_analysis_enabled: true
    
  file_monitoring:
    watch_directories:
      - "kb/facts"
      - "kb/rules"
    file_extensions:
      - ".txt"
      - ".yaml"
    ignore_patterns:
      - "*.tmp"
      - "*.bak"
      - ".*"
    
  parallel_processing:
    max_workers: 4
    batch_size: 50
    timeout_seconds: 30

logging:
  level: "INFO"
  format: "%(asctime)s - [Γ∆] - %(levelname)s - %(message)s"
  file: "gamma_delta.log"
"""


# =============================================================================
# Usage Example
# =============================================================================
if __name__ == "__main__":
    print("🎯 Gamma Delta Sensing System")
    print("=" * 40)
    
    # Test gamma detection
    print("🔍 Testing Gamma Detection...")
    gamma = GammaDetector()
    changes = gamma.scan_for_changes()
    
    print(f"  Files scanned: {changes['gamma_metrics']['total_files']}")
    print(f"  Changes detected: {changes['gamma_metrics']['total_changes']}")
    print(f"  Change rate: {changes['gamma_metrics']['change_rate']:.2%}")
    
    # Test delta analysis  
    print("\n📊 Testing Delta Analysis...")
    delta = DeltaAnalyzer()
    analysis = delta.analyze_fact_rule_pairs()
    
    print(f"  Total pairs: {analysis['summary']['total_pairs_found']}")
    print(f"  Complete pairs: {analysis['summary']['complete_pairs']}")
    print(f"  Average similarity: {analysis['summary']['average_similarity']:.2%}")
    
    if analysis['recommendations']:
        print("\n💡 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"  - {rec}")

