import sys
import os
import select

from constants import PROMPT
from display_graph import display_graph
from load_json import load_json
from input_lock import input_lock, watcher_pending
from snapshot import snapshot_dir_for_json
from handlers import branch_handler, switch_handler, load_handler

def _line_ready(timeout: float = 0.2) -> bool:
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    return bool(ready)

def command_prompt_loop(json_file_path: str) -> None:
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
            stripped_input = input().strip().split(maxsplit=1)
            command = stripped_input[0].lower() if stripped_input else ""
            args = stripped_input[1].strip() if len(stripped_input) > 1 else None

        if command == "graph":
            print(display_graph(json_file_path))
        elif command == "branch":
            branch_handler(json_file_path, args)
        elif command == "switch":
            switch_handler(json_file_path, args)
        elif command == "load":
            load_handler(json_file_path, snapshot_dir)
        elif command == "quit":
            print("\nExiting Ableton VCS. Goodbye!")
            break
        elif command == "":
            pass
        else:
            print(f"Unknown command: '{command}'")

        print(PROMPT.format(branch=load_json(json_file_path)["pointer"]), end="", flush=True)
