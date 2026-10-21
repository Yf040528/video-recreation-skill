import json
from pathlib import Path

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate_basic(document: dict, kind: str):
    """Dependency-free structural gate. Server may add jsonschema Draft 2020-12 validation."""
    required = {
        "svml": ["svml_version","job_id","intent","output","masters","shots"],
        "task": ["task_id","job_id","semantic_function","presence_map","output_contract"],
        "generation_request": ["request_id","capability","task_id","inputs","requirements"],
        "qa_result": ["task_id","status","checks"]
    }[kind]
    missing=[k for k in required if k not in document]
    if missing: raise ValueError(f"{kind} missing required fields: {missing}")
    return document
