#!/usr/bin/env python3
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


if __name__ == "__main__":
    # Test the gamma detector
    detector = GammaDetector()
    results = detector.scan_for_changes()
    print(f"Scanned {results['gamma_metrics']['total_files']} files")
    print(f"Detected {results['gamma_metrics']['total_changes']} changes")

