import bpy
from pathlib import Path
import subprocess

class Git():
    def __init__(self):
        pass

    def get_git_repo(path):
        path = Path(path).resolve()
        for parent in [path] + list(path.parents):
            if (parent / ".git").is_dir():
                return parent
        return None
    
    @classmethod
    def push():
        pass

    @classmethod
    def commit(self, msg):
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"{msg}"], check=True)

        return