#!/bin/bash
# Debug and fix the sensing module import issues

echo "🔍 Debugging sensing module imports..."

# Check what's in the sensing directory
echo "📁 Contents of sensing/ directory:"
ls -la sensing/

echo ""
echo "📄 Checking if delta_analyzer.py exists and has content:"
if [ -f "sensing/delta_analyzer.py" ]; then
    echo "✅ File exists"
    echo "📊 File size: $(wc -c < sensing/delta_analyzer.py) bytes"
    echo "📝 First few lines:"
    head -5 sensing/delta_analyzer.py
else
    echo "❌ File does not exist"
fi

echo ""
echo "🐍 Testing Python syntax of delta_analyzer.py:"
python -m py_compile sensing/delta_analyzer.py 2>&1 || echo "❌ Syntax error found"

echo ""
echo "🔍 Checking for DeltaAnalyzer class in the file:"
if grep -q "class DeltaAnalyzer" sensing/delta_analyzer.py 2>/dev/null; then
    echo "✅ DeltaAnalyzer class found"
else
    echo "❌ DeltaAnalyzer class not found"
fi

echo ""
echo "🔧 Testing individual file imports:"
python -c "import sensing.delta_analyzer; print('✅ Module import works')" 2>&1 || echo "❌ Module import failed"
python -c "from sensing.delta_analyzer import DeltaAnalyzer; print('✅ Class import works')" 2>&1 || echo "❌ Class import failed"
