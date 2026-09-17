from typing import Any
import os
import shutil
from load_json import load_json, save_json
from snapshot import find_snapshot, als_root_finder
from project_loader import project_loader
from input_lock import safe_input
from branch import (
    create_branch,
    get_branch,
    parent_hash_of_branch,
    switch_branch,
    current_branch,
    find_branch_by_commit_hash,
)

VCSData = dict[str, Any]


def branch_handler(json_file_path: str, branch_name: str | None = None) -> None:
    if branch_name is None:
        branch_name = safe_input("Enter the name of the branch: ").strip()
    data: VCSData = load_json(json_file_path)
    if get_branch(data, branch_name) is not None:
        print(f"Branch '{branch_name}' exists, use '<switch> <{branch_name}>'")
        return
    current = current_branch(data)
    parent_hash = parent_hash_of_branch(current)
    create_branch(data, branch_name, current["branch"], parent_hash)
    switch_branch(data, branch_name)
    save_json(data, json_file_path)
    print(f"Created and switched to '{branch_name}'")


def switch_handler(json_file_path: str, branch_name: str | None = None) -> None:
    if branch_name is None:
        branch_name = safe_input("Switch to branch: ").strip()
    data: VCSData = load_json(json_file_path)
    try:
        switch_branch(data, branch_name)
        save_json(data, json_file_path)
        print(f"Switched to '{branch_name}'")
    except ValueError as e:
        print(e)


def load_handler(json_file_path: str, snapshot_dir: str) -> None:
    hash_input = safe_input("Please enter the commit's hash to restore: ").strip()
    snapshot_file_path = find_snapshot(snapshot_dir, hash_input)
    if snapshot_file_path is None:
        print(f"No snapshots found with matching hash: '{hash_input}'")
        return

    root_als = als_root_finder(json_file_path)
    if root_als is None:
        print("Could not find a root .als file in folder")
        return

    data: VCSData = load_json(json_file_path)
    owner_branch = find_branch_by_commit_hash(data, hash_input)
    if owner_branch:
        switch_branch(data, owner_branch)
        save_json(data, json_file_path)
        print(f"Switched active branch to '{owner_branch}'")

    shutil.copy2(snapshot_file_path, root_als)
    print(f"Restored root project to [{hash_input[:7]}]")
    project_loader(root_als)
