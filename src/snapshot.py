import shutil
import os
import re
import glob


def snapshot_dir_for_json(json_file_path: str) -> str:
    json_dir = os.path.dirname(os.path.abspath(json_file_path))
    return os.path.join(json_dir, "snapshots")


def als_root_finder(json_file_path: str) -> str | None:
    json_dir = os.path.dirname(os.path.abspath(json_file_path))
    als_files = glob.glob(os.path.join(json_dir, "*.als"))
    if len(als_files) == 1:
        return als_files[0]
    return None


def snapshot(als_file_path: str, file_hash: str, snapshots_dir_path: str, timestamp: str) -> str | None:
    try:
        os.makedirs(snapshots_dir_path, exist_ok=True)

        project_name = os.path.basename(als_file_path)
        name, exten = os.path.splitext(project_name)

        corrected_timestamp = timestamp.replace(":", "-").replace(".", "-")
        new_project_name = f"{name}[{corrected_timestamp}][{file_hash[:7]}]{exten}"
        destination_path = os.path.join(snapshots_dir_path, new_project_name)

        shutil.copy2(als_file_path, destination_path)
        return destination_path
    except Exception as e:
        print(f"Error creating snapshot: '{e}'")
        return None


def find_snapshot(snapshots_dir_path: str, commit_hash: str) -> str | None:
    if not os.path.isdir(snapshots_dir_path):
        return None
    for item in os.listdir(snapshots_dir_path):
        groups = re.findall(r"\[([^\[\]]+)\]", item)
        if groups and groups[-1].startswith(commit_hash):
            return os.path.join(snapshots_dir_path, item)
    return None
