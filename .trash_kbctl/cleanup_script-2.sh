#!/bin/bash
# Cleanup and Proper Setup Script for Gamma Delta Sense System

echo "🧹 Cleaning up spurious files and directories..."

# Remove the spurious single-word files/directories from root
rm -rf "#" "Background" "CLI" "configuration" "for" "monitoring" "operations" "service" "System-wide"

# Clean up the sensing directory
cd sensing
rm -rf "#" "analysis" "change" "configuration" "Content" "detection" "difference" "file" "indexing" "monitoring" "of" "Parallel" "Rate" "Real-time" "Sensing"
cd ..

echo "✅ Cleanup completed!"

# Verify the core files are present
echo "📋 Checking core sensing files..."

CORE_FILES=(
    "sensing/__init__.py"
    "sensing/gamma_detector.py"
    "sensing/delta_analyzer.py" 
    "sensing/file_monitor.py"
    "sensing/indexer.py"
    "sensing/config.yaml"
    "scripts/sense_changes.py"
    "scripts/monitor_daemon.py"
    "sense_config.yaml"
)

for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ Missing: $file"
    fi
done

echo ""
echo "🎯 Your clean structure should now be:"
echo "gamma_delta_sense/"
echo "├── kb/"
echo "│   ├── facts/"
echo "│   ├── rules/"
echo "│   ├── facts.yaml"
echo "│   └── rules.yaml"
echo "├── sensing/"
echo "│   ├── __init__.py"
echo "│   ├── gamma_detector.py"
echo "│   ├── delta_analyzer.py"
echo "│   ├── file_monitor.py"
echo "│   ├── indexer.py"
echo "│   └── config.yaml"
echo "├── scripts/"
echo "│   ├── validate_kb.py"
echo "│   ├── sense_changes.py"
echo "│   └── monitor_daemon.py"
echo "├── raw_docs/"
echo "├── semi_structured/"
echo "├── tests/"
echo "├── ui/"
echo "├── validator.py"
echo "├── sense_config.yaml"
echo "└── README.md"

echo ""
echo "🚀 Run 'tree -L 2' to verify the cleanup worked!"
