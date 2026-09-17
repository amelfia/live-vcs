import os
import platform
import subprocess

def project_loader(als_file_path: str) -> bool:
    path = os.path.abspath(als_file_path)
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return False
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.run(["open", path], check=True)
        elif system == "Windows":
            subprocess.run(["start", path], shell=True, check=True)
        else:
            subprocess.run(["xdg-open", path], check=True)
        return True
    except Exception as e:
        print(f"Failed to open project: {e}")
        return False
