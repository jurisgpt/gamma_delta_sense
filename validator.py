import os
import yaml

def load_yaml(filepath):
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f), None
    except Exception as e:
        return None, str(e)

def validate_kb_files(base_path):
    results = []
    for kb_type in ['rules', 'facts']:
        dir_path = os.path.join(base_path, 'kb', kb_type)
        if not os.path.isdir(dir_path):
            results.append({"file": f"<missing {kb_type} dir>", "status": "ERROR", "details": "Directory not found"})
            continue

        for fname in os.listdir(dir_path):
            if fname.endswith(".yaml"):
                full_path = os.path.join(dir_path, fname)
                data, err = load_yaml(full_path)
                results.append({
                    "file": fname,
                    "status": "OK" if err is None else "FAIL",
                    "details": "Valid" if err is None else err
                })
    return results

if __name__ == "__main__":
    kb_base = os.path.expanduser("~/github/gamma_delta_sense")
    report = validate_kb_files(kb_base)
    for r in report:
        print(f"{r['file']:25} | {r['status']:5} | {r['details']}")


