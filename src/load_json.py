import os
import json
from typing import Any

SnapshotData = dict[str, Any]
CommitDict = dict[str, str]


def load_json(json_file_path: str) -> SnapshotData:
    abs_json_path = os.path.abspath(json_file_path)
    if os.path.isfile(abs_json_path) and os.path.getsize(abs_json_path) > 0:
        with open(abs_json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"pointer": "main", "snapshots": [{"branch": "main", "children": []}]}


def save_json(data: SnapshotData, json_file_path: str) -> None:
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def commit_structure(file_hash: str, annotation: str, timestamp: str) -> CommitDict:
    return {"hash": file_hash, "timestamp": timestamp, "annotation": annotation}
