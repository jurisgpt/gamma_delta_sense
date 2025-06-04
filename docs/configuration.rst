Configuration
============

The Gamma Delta Sense system is configured using the ``sense_config.yaml`` file in the root directory.

Example Configuration
--------------------

.. code-block:: yaml

    # Gamma Delta Sense System Configuration
    system:
      name: "Gamma Delta Sense"
      version: "1.0.0"
      description: "Change detection and difference analysis for knowledge base"

    paths:
      knowledge_base: "kb"
      facts_directory: "kb/facts"
      rules_directory: "kb/rules"
      raw_docs: "raw_docs"
      semi_structured: "semi_structured"

    sensing:
      gamma_detection:
        enabled: true
        threshold: 0.1
        scan_interval: 60
        
      delta_analysis:
        enabled: true
        similarity_threshold: 0.5
        
      monitoring:
        real_time: false
        file_extensions: [".txt", ".yaml"]

    validation:
      require_paired_files: true
      content_validation: true
      cross_reference_check: true

    performance:
      max_workers: 4
      timeout_seconds: 30
      
    logging:
      level: "INFO"
      file: "gamma_delta.log"

Configuration Options
--------------------

### System
- ``name``: System name
- ``version``: System version
- ``description``: System description

### Paths
- ``knowledge_base``: Root directory for knowledge base
- ``facts_directory``: Directory for fact files
- ``rules_directory``: Directory for rule files
- ``raw_docs``: Directory for raw documents
- ``semi_structured``: Directory for semi-structured data

### Sensing
#### Gamma Detection
- ``enabled``: Enable/disable change detection
- ``threshold``: Threshold for detecting changes (0-1)
- ``scan_interval``: Time between scans (seconds)

#### Delta Analysis
- ``enabled``: Enable/disable difference analysis
- ``similarity_threshold``: Threshold for considering items similar (0-1)

#### Monitoring
- ``real_time``: Enable real-time monitoring
- ``file_extensions``: File extensions to monitor

### Validation
- ``require_paired_files``: Require paired YAML/TXT files
- ``content_validation``: Enable content validation
- ``cross_reference_check``: Check cross-references between files

### Performance
- ``max_workers``: Maximum number of worker threads
- ``timeout_seconds``: Operation timeout in seconds

### Logging
- ``level``: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- ``file``: Log file path
