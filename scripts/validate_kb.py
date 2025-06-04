import os
import yaml

# Define required fields
REQUIRED_RULE_FIELDS = ["rule_id", "if", "then", "metadata"]
REQUIRED_FACT_FIELDS = ["concept", "property", "context"]

def validate_rule(file_path):
    errors = []
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return {"file": file_path, "type": "rule", "status": "invalid", "errors": [f"YAML load error: {str(e)}"]}

    if not isinstance(data, dict):
        return {"file": file_path, "type": "rule", "status": "invalid", "errors": ["Top-level YAML must be a dictionary."]}

    for field in REQUIRED_RULE_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "metadata" in data:
        meta = data["metadata"]
        if not isinstance(meta.get("year", 0), int):
            errors.append("metadata.year must be an integer")
        if not isinstance(meta.get("confidence", 1.0), float):
            errors.append("metadata.confidence must be a float")

    return {
        "file": file_path,
        "type": "rule",
        "status": "valid" if not errors else "invalid",
        "errors": errors
    }

def validate_fact(file_path):
    errors = []
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return {"file": file_path, "type": "fact", "status": "invalid", "errors": [f"YAML load error: {str(e)}"]}

    if not isinstance(data, list):
        return {"file": file_path, "type": "fact", "status": "invalid", "errors": ["File must contain a list of facts."]}

    for i, entry in enumerate(data):
        for field in REQUIRED_FACT_FIELDS:
            if field not in entry:
                errors.append(f"Fact {i+1} missing field: {field}")

    return {
        "file": file_path,
        "type": "fact",
        "status": "valid" if not errors else "invalid",
        "errors": errors
    }

def validate_kb(base_dir="./gamma_delta_sense/kb"):
    results = []

    rule_dir = os.path.join(base_dir, "rules")
    fact_dir = os.path.join(base_dir, "facts")

    for root, _, files in os.walk(rule_dir):
        for f in files:
            if f.endswith(".yaml"):
                results.append(validate_rule(os.path.join(root, f)))

    for root, _, files in os.walk(fact_dir):
        for f in files:
            if f.endswith(".yaml"):
                results.append(validate_fact(os.path.join(root, f)))

    return results

# Run and print results
if __name__ == "__main__":
    results = validate_kb()
    for r in results:
        print(f"{r['status'].upper()} - {r['file']}")
        if r['errors']:
            for err in r['errors']:
                print(f"  ✗ {err}")
        print()


