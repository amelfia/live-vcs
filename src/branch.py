from typing import Any

BranchDict = dict[str, Any]
VCSData = dict[str, Any]


def get_branch(data: VCSData, branch_name: str) -> BranchDict | None:
    for branch in data["snapshots"]:
        if branch["branch"] == branch_name:
            return branch
    return None


def parent_hash_of_branch(branch: BranchDict) -> str | None:
    children: list[dict[str, str]] = branch.get("children", [])
    if children:
        return children[-1]["hash"]
    return None

def find_branch_by_commit_hash(data: dict, commit_hash: str) -> str | None:
    for branch in data["snapshots"]:
        for commit in branch["children"]:
            if commit["hash"].startswith(commit_hash):
                return branch["branch"]
    return None


def create_branch(data: VCSData, branch_name: str, from_branch: str, from_hash: str | None) -> VCSData:
    data["snapshots"].append(
        {
            "branch": branch_name,
            "branched_from": {"branch": from_branch, "hash": from_hash},
            "children": [],
        }
    )
    return data


def switch_branch(data: VCSData, branch_name: str) -> VCSData:
    if get_branch(data, branch_name) is None:
        raise ValueError(f"Branch {branch_name} doesn't exist")
    data["pointer"] = branch_name
    return data


def current_branch(data: VCSData) -> BranchDict:
    branch = get_branch(data, data["pointer"])
    if branch is None:
        raise ValueError(f"Pointer references a missing branch '{data['pointer']}'")
    return branch
