from datetime import datetime
from typing import Any
from hash_generator import hash_generator
from load_json import load_json, save_json, commit_structure
from snapshot import snapshot, snapshot_dir_for_json
from input_lock import safe_input
from branch import current_branch

def commit_duplicate(branch: dict[str, Any], file_hash: str) -> bool:
    children: list[dict[str, str]] = branch.get("children", [])
    return bool(children and children[-1]["hash"] == file_hash)

def write_commit_to_json(als_file_path: str, json_file_path: str) -> None:
    file_hash = hash_generator(als_file_path)
    if file_hash is None:
        print(f"Failed to hash: {als_file_path}")
        return

    data = load_json(json_file_path)
    current = current_branch(data)

    if commit_duplicate(current, file_hash):
        return

    if not current["children"] and "branched_from" in current and current["branched_from"]["hash"] == file_hash:
        return

    timestamp = datetime.now().isoformat()
    print(f"\n [Change detected] File saved: {als_file_path}")
    annotation = safe_input("Describe the changes you made: ").strip()

    snapshot(als_file_path, file_hash, snapshot_dir_for_json(json_file_path), timestamp)

    current["children"].append(commit_structure(file_hash, annotation, timestamp))
    save_json(data, json_file_path)
