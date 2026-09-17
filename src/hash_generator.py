import os
import gzip
import hashlib

def hash_generator(ableton_als_file_path: str) -> str | None:
    try:
        path = os.path.abspath(ableton_als_file_path)
        if not os.path.isfile(path):
            return None

        with gzip.open(path, "rb") as f:
            xml_text = f.read()

        return hashlib.md5(xml_text).hexdigest()
    except Exception:
        return None
