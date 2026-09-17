import threading

input_lock: threading.Lock = threading.Lock()
watcher_pending: threading.Event = threading.Event()


def safe_input(prompt: str) -> str:
    with input_lock:
        return input(prompt)
