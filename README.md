
# Immunology Knowledge Base Development & Monitoring System

<!-- Replace with actual image -->
![Immunology Knowledge Base](https://via.placeholder.com/800x200/0066CC/FFFFFF?text=Immunology+Knowledge+Base)

A domain-specific system for developing, monitoring, and analyzing changes in immunology knowledge bases. Focuses on tracking relationships between immunological concepts like BTN3A1 activation and gamma delta T cell responses.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation Status](https://gamma-delta-sense.readthedocs.io/en/latest/)

## Features

- **Real-time change detection** - Monitor knowledge base modifications
- **Semantic difference analysis** - Detect meaningful content changes
- **Knowledge validation** - Ensure structural and logical integrity
- **Relationship mapping** - Track connections between immunological concepts
- **Continuous monitoring** - Daemon mode for background operation

## Project Structure

```bash
immunology-knowledge-system/
├── kb/                       # Knowledge base
│   ├── facts/                # Factual information
│   └── rules/                # Rule definitions
├── raw_docs/                 # Source documents
├── semi_structured/          # Processed data
├── scripts/                  # Operational scripts
│   ├── sense_changes.py      # CLI for change detection
│   ├── validate_kb.py        # Validation tool
│   └── monitor_daemon.py     # Monitoring daemon
├── sensing/                  # Analysis modules
├── tests/                    # Test suites
└── ui/                       # User interface
```

## Knowledge Format Examples

### Structured Fact (YAML)

```yaml
# kb/facts/structured/fact-001.yaml
concept: BTN3A1_activation
properties:
  antibody_binding: true
  t_cell_activation: Vγ9Vδ2
context: 
  pathway: Butyrophilin-mediated immune response
sources:
  - pmid: 12345678
  - doi: 10.1016/j.immuni.2023.01.001
confidence: 0.95
last_updated: 2023-05-15
```

### Structured Rule (YAML)

```yaml
# kb/rules/structured/rule-001.yaml
rule_id: BTN3A1_activation_rule
antecedent: BTN3A1_antibody_binding
consequent: Vγ9Vδ2_T_cell_activation
confidence: 0.92
evidence:
  - source: PMID:23456789
  - source: DOI:10.1084/jem.20220765
conditions:
  - requires_phosphoantigen_presentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip package manager
- libyaml (for PyYAML)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/immunology-knowledge-system.git
cd immunology-knowledge-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Configure the system
cp config/sense_config.example.yaml sense_config.yaml
# Edit sense_config.yaml with your paths and settings
```

## Usage

### Command Line Interface

```bash
# Run change detection
python scripts/sense_changes.py gamma

# Perform difference analysis between versions
python scripts/sense_changes.py delta --version v1.2 v1.3

# Validate knowledge base
python scripts/sense_changes.py validate

# Start monitoring daemon
python scripts/monitor_daemon.py start

# Show system status
python scripts/sense_changes.py status
```

### Key Commands

| Command    | Description                  | Options                      |
|------------|------------------------------|------------------------------|
| `gamma`    | Detect file-level changes    | `--threshold`, `--full-scan` |
| `delta`    | Analyze semantic differences | `--versions`, `--deep`       |
| `validate` | Run KB validation            | `--fix` (attempt repairs)    |
| `status`   | Show monitoring status       | `--verbose`                  |

## Configuration

Edit `sense_config.yaml` to customize system behavior:

```yaml
paths:
  kb: ./kb
  raw: ./raw_docs

detection:
  interval: 60          # Seconds between scans
  threshold: 0.85       # Change significance threshold

analysis:
  semantic_similarity: 0.75

monitoring:
  realtime: true
  watched_extensions: [".yaml", ".yml"]

logging:
  level: info
  file: system.log
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

Please ensure your code follows PEP8 guidelines and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Documentation

Full documentation is available at [https://immuno-kb.readthedocs.io](https://immuno-kb.readthedocs.io)

## Project Status

**Status:** Active Development  
**Primary Focus:** Immunology domain knowledge base centered on BTN3A1-mediated immune responses and gamma delta T cell activation  
**Contact:** 

---

*This system is designed for researchers working with immunological knowledge bases and requires domain expertise in immunology and T cell biology.*
