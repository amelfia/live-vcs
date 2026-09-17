from typing import Any
from load_json import load_json

VCSData = dict[str, Any]
BranchDict = dict[str, Any]


def forked_from_hash(data: VCSData) -> dict[str, list[str]]:
    fork_dict: dict[str, list[str]] = {}
    for branch in data["snapshots"]:
        if "branched_from" in branch and branch["children"]:
            key = branch["branched_from"]["hash"]
            if key not in fork_dict:
                fork_dict[key] = []
            fork_dict[key].append(branch["branch"])
    return fork_dict


def display_graph(json_file_path: str) -> str:
    data = load_json(json_file_path)
    return render_graph(data)


def render_graph(data: VCSData) -> str:
    fork_dict = forked_from_hash(data)
    branches_by_name: dict[str, BranchDict] = {
        b["branch"]: b for b in data["snapshots"]
    }
    out: list[str] = []

    def render(branch: BranchDict, prefix: str) -> None:
        commits = list(reversed(branch["children"]))

        for index, commit in enumerate(commits):
            tip = (
                f" ({branch['branch']})"
                if branch["branch"] != "main" and index == 0
                else ""
            )
            line = f"* {commit['hash'][:7]} {commit['annotation']}{tip}"
            out.append(prefix + line)

            for child_name in fork_dict.get(commit["hash"], []):
                child = branches_by_name[child_name]
                out.append(f"{prefix}|")
                render(child, prefix + "    ")

            if index < len(commits) - 1:
                out.append(f"{prefix}|")

    if "main" in branches_by_name:
        render(branches_by_name["main"], "")
        out.append("main")
    return "\n".join(out) + "\n"
