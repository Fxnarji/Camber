try:
    from ..constants import get_preferences
except:
    # we are in watcher, no prefs needed
    pass

from pathlib import Path
import subprocess
import os

class Git():

    @staticmethod
    def bin():
        prefs = get_preferences()
        return prefs.git_path

    def get_git_repo(path):
        path = Path(path).resolve()
        for parent in [path] + list(path.parents):
            if (parent / ".git").is_dir():
                return parent
        raise ValueError("Not a git repository!")
    
    @classmethod
    def checkout(self, hash, file_path):
        repo_dir = self.get_git_repo(file_path)
        rel_path = os.path.relpath(file_path, repo_dir)
        subprocess.run(
            [f"{self.bin()}", "checkout", hash, "--", rel_path],
            cwd=repo_dir,
            check=True
                    )
        return None

    @classmethod
    def get_current_commit_hash(cls, file_path):
        repo_dir = cls.get_git_repo(file_path)
        rel_path = os.path.relpath(file_path, repo_dir)

        try:
            # 1. Get the current file's blob hash
            current_blob = subprocess.run(
                [cls.bin(), "hash-object", rel_path],
                cwd=repo_dir, capture_output=True, text=True, check=True
            ).stdout.strip()

            # 2. Get all commits that touched this file (newest to oldest)
            log_cmd = [cls.bin(), "log", "--format=%h", "--", rel_path]
            commits = subprocess.run(log_cmd, cwd=repo_dir, capture_output=True, text=True, check=True).stdout.splitlines()

            # 3. Find the first commit where the file's blob matches the current blob
            for commit_hash in commits:
                # Ask Git: "What was the blob hash for this file in THIS specific commit?"
                tree_cmd = [cls.bin(), "rev-parse", f"{commit_hash}:{rel_path}"]
                commit_blob = subprocess.run(tree_cmd, cwd=repo_dir, capture_output=True, text=True).stdout.strip()
                
                if commit_blob == current_blob:
                    return commit_hash # Found the exact match!

            return "Modified/Uncommitted"

        except Exception as e:
            print(f"Error finding current file version: {e}")
            return "Unknown"


    @classmethod
    def commit(self, msg, filepath):
        # Get the directory of the current blend file
        repo_dir = os.path.dirname(filepath)
        
        try:
            subprocess.run([f"{self.bin()}", "add", bpy.data.filepath], cwd=repo_dir, check=True, capture_output=True)
            
            subprocess.run([f"{self.bin()}", "commit", "-m", msg], cwd=repo_dir, check=True, capture_output=True)
            
            result = subprocess.run([f"{self.bin()}", "push"], cwd=repo_dir, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Push failed: {result.stderr}")
                return False, f"Commit saved, but Push failed: {result.stderr}"

            return True, "Successfully committed and pushed!"

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            print(f"Git Error: {error_msg}")
            return False, error_msg
        except FileNotFoundError:
            print(self.bin)
            return False, "Git executable not found. Is Git installed?"
        
    @classmethod
    def get_git_history(self, file_path):
        """
        Returns a list of dictionaries containing commit history for a specific file.
        """
        if not file_path or not os.path.exists(file_path):
            return []

        repo_dir = self.get_git_repo(file_path)

        rel_path = os.path.relpath(file_path, repo_dir)

        # We use a custom format to make parsing easy: 
        # %h = short hash, %an = author name, %ad = date, %s = subject (message)
        git_format = "%h%x09%an%x09%ad%x09%s"
        
        cmd = [
            f"{self.bin()}", "log", 
            f"--pretty=format:{git_format}", 
            "--date=short", 
            "--", rel_path
        ]

        try:
            result = subprocess.run(
                cmd, 
                cwd=repo_dir, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            history = []
            for line in result.stdout.splitlines():
                if not line.strip():
                    continue
                
                # Split by the tab character we inserted (%x09)
                parts = line.split('\t')
                if len(parts) == 4:
                    history.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "message": parts[3]
                    })
            
            return history

        except subprocess.CalledProcessError as e:
            print(f"Git Log Error: {e.stderr}")
            return []
        except FileNotFoundError:
            print("Git executable not found.")
            return []