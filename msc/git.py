from pathlib import Path
import subprocess
import os
from .session import get_session

class Git:

    def __init__(self, filepath:str):
        self.file =f"{str(Path(filepath).name)}"
        self.path = Path(filepath).parent
        self.session = get_session()

        print(self.file)
        print(self.path)


    def bin(self) -> str:
        """Return the path to the git executable."""
        git_bin = getattr(self.session, "git_bin", None)
        if git_bin:
            return git_bin
        raise ValueError("No git instance found")

    def run_git_command(self, arguments: list[str], check: bool = True, path = None, strip = True) -> str:
        git_exe = self.bin()
        if not path:
            path = self.path
        result = subprocess.run(
            [git_exe, *arguments],
            capture_output=True,
            cwd=path,
            text=True,
            check=check
        )
        if strip:
            return result.stdout.strip()
        else:
            return result.stdout

    def verify_git_bin(self) -> tuple[bool, str]:
        try:
            output = self.run_git_command(["ls-remote", "https://github.com/example/test"])
            return True, output
        except (subprocess.CalledProcessError, ValueError, FileNotFoundError) as e:
            return False, str(e)
        
    def verify_repository(self) -> tuple[bool, str]:
        session = get_session()
        url = session.repository_url

        if url is None:
            return False, "No url provided"

        try:
            output = self.run_git_command(arguments=["ls-remote",url])
            return True, output
        except (subprocess.CalledProcessError, ValueError, FileNotFoundError) as e:
            return False, str(e)
          
    def push(self) -> tuple[bool,str]:
        try:
            self.run_git_command(["push", "origin", "HEAD"])
        except Exception as e:
            return False, f"push failed because {e}"
        return True, "success"

    def commit(self, message) -> tuple[bool,str]:
        try:
            self.run_git_command(["add", str(self.file)])
            self.run_git_command(["commit", "-m", message])
        except Exception as e:
            return False, f"commit failed because {e}"
        return True, "success"

    def fetch(self):
        try:
            self.run_git_command(["fetch", "origin"])
        except Exception as e:
            return False, f"fetch failed because {e}"
        return True, "success"

    def pull(self) -> tuple[bool,str]:
        try:
            self.fetch()
            self.run_git_command(["pull", "origin", "HEAD"])
        except Exception as e:
            return False, f"pull failed because {e}"
        return True, "success"

    def clone(self, directory: str) -> tuple[bool,str]:
        try:
            self.run_git_command(["clone", str(self.session.repository_url)], path = directory)
        except Exception as e:
            return False, f"clone failed because {e}"
        return True, "success"
    
    def checkout(self, hash) -> tuple[bool,str]:
        try:
            self.run_git_command(["checkout", hash, "--", self.file])
        except Exception as e:
            return False, f"checkout failed because {e}"
        return True, "success"
    
    def get_detailed_git_history(self):
        # Format: hash, author, date, message
        git_format = "%h%x09%an%x09%ad%x09%s"

        history = []

        try:
            result = self.run_git_command(["log", f"--pretty=format:{git_format}", "--date=short", "--", self.file])
            for line in result:
                if not line.strip(): continue
                parts = line.split('\t')
                
                if len(parts) == 4:
                    commit_hash = parts[0]
                    
                    size_result = self.run_git_command([self.bin(), "ls-tree", "-r", "-l", commit_hash, self.file], strip=False)
                    
                    size_str = "Unknown"
                    if size_result:
                        size_parts = size_result.split()
                        if len(size_parts) >= 4:
                            bytes_val = int(size_parts[3])
                            size_str = f"{bytes_val / (1024*1024):.2f} MB"

                    history.append({
                        "hash": commit_hash,
                        "author": parts[1],
                        "date": parts[2],
                        "message": parts[3],
                        "size": size_str
                    })
            
            return True, history
        except Exception as e:
            return False, f"getting history failed because {e}"
        
    def get_current_commit(self) -> tuple[bool,str]:

        try:
            # 1. Get the current file's blob hash
            current_blob = self.run_git_command(["hash-object", self.file])

            # 2. Get all commits that touched this file (newest to oldest)
            commits = self.run_git_command(["log", "--format=%", "--"], strip = False).splitlines()

            # 3. Find the first commit where the file's blob matches the current blob
            for commit_hash in commits:
                commit_blob = self.run_git_command(["rev-parse", f"{commit_hash}:{self.file}"])
                
                if commit_blob == current_blob:
                    return True, commit_hash # Found the exact match!

            return False, "didnt find hash"

        except Exception as e:
            print(f"Error finding current file version: {e}")
            return False, "Unknown"
