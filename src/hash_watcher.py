import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileMovedEvent
from write_commit_to_json import write_commit_to_json
from input_lock import watcher_pending

class ALS_HANDLER(FileSystemEventHandler):
    def __init__(self, json_file_path: str, dir_path: str) -> None:
        self.json_file_path = json_file_path
        self.dir_path = os.path.abspath(dir_path)

    def handle_als_change(self, src_path: str) -> None:
        parent_dir = os.path.dirname(os.path.abspath(src_path))
        if src_path.endswith(".als") and parent_dir == self.dir_path:
            watcher_pending.set()
            try:
                write_commit_to_json(src_path, self.json_file_path)
            finally:
                watcher_pending.clear()

    def on_modified(self, event: FileModifiedEvent) -> None:
        if not event.is_directory:
            self.handle_als_change(event.src_path)

    def on_moved(self, event: FileMovedEvent) -> None:
        if not event.is_directory:
            self.handle_als_change(event.dest_path)

def start_watcher(dir_path: str, json_file_path: str) -> None:
    observer = Observer()
    handler = ALS_HANDLER(json_file_path, dir_path)
    observer.schedule(handler, path=dir_path, recursive=False)
    observer.start()
    while True:
        time.sleep(1)
