from typing import Any
from load_json import load_json

VCSData = dict[str, Any]
BranchDict = dict[str, Any]


def forked_from_hash(data: VCSData) -> dict[str, list[str]]:
    fork_dict: dict[str, list[str]] = {}
    for branch in data["snapshots"]:
        if "branched_from" in branch and branch["children"]:
            key = branch["branched_from"]["hash"]
            if key:
                fork_dict.setdefault(key, []).append(branch["branch"])
    return fork_dict


def display_graph(json_file_path: str) -> str:
    data = load_json(json_file_path)
    return render_graph(data)


def render_graph(data: VCSData) -> str:
    branches_by_name: dict[str, BranchDict] = {b["branch"]: b for b in data["snapshots"]}

    fork_dict = forked_from_hash(data)
    out: list[str] = []

    def render_branch(branch: BranchDict, is_main: bool) -> None:
        commits = list(reversed(branch.get("children", [])))
        prefix = "" if is_main else "| "

        for index, commit in enumerate(commits):
            tag = f" ({branch['branch']})"if index == 0 and not is_main else ""
            out.append(f"{prefix}* {commit['hash'][:7]} {commit['annotation']}{tag}")


            for child_name in fork_dict.get(commit["hash"], []):
                child = branches_by_name[child_name]
                out.append("|\\")
                render_branch(child, is_main=False)
                out.append("|/")

            if index < len(commits) - 1:
                out.append(f"{prefix}|")

    if "main" in branches_by_name:
        render_branch(branches_by_name["main"], is_main=True)

    return "\n".join(out) + "\n"

