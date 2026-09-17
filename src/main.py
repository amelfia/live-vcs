import os
import threading
from hash_watcher import start_watcher
from command_prompt_loop import command_prompt_loop

def main() -> None:
    project_dir = input("Please enter the path to your Ableton project folder: ").strip()
    project_dir = os.path.abspath(project_dir)
    json_commits = os.path.join(project_dir, "snapshot_hashes.json")

    print("Ableton VCS")
    print("=====:)======")

    watcher_thread = threading.Thread(
        target=start_watcher, args=(project_dir, json_commits), daemon=True
    )
    watcher_thread.start()
    command_prompt_loop(json_commits)

if __name__ == "__main__":
    main()
