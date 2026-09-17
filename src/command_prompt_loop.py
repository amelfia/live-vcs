import sys
import os
import select

from constants import PROMPT
from display_graph import display_graph
from load_json import load_json
from input_lock import input_lock, watcher_pending
from project_loader import project_loader
from snapshot import snapshot_dir_for_json, als_root_finder
from handlers import branch_handler, switch_handler, load_handler


def _line_ready(timeout=0.2):
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    return bool(ready)

def command_prompt_loop(json_file_path):
    snapshot_dir = snapshot_dir_for_json(json_file_path)

    print(PROMPT.format(branch=load_json(json_file_path)["pointer"]), end="", flush=True)
    while True:
        if watcher_pending.is_set():
            watcher_pending.wait(timeout=0.2)
            continue

        if not _line_ready():
            continue

        with input_lock:
            if watcher_pending.is_set():
                continue

            striped_input = input().strip().split(maxsplit=1)
            command = striped_input[0].lower() if striped_input else ""
            args = striped_input[1].strip() if len(striped_input) > 1 else None

        if command == "graph":
            print(display_graph(json_file_path))

        elif command == "branch":
            branch_handler(json_file_path, args)

        elif command == "switch":
            switch_handler(json_file_path, args)

        elif command == "load":
            load_handler(json_file_path, snapshot_dir)

        elif command == "quit":
            break

        else:
            print("Command not valid")

        print(PROMPT.format(branch=load_json(json_file_path)["pointer"]), end="", flush=True)
