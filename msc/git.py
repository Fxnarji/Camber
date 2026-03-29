try:
    from ..constants import get_preferences
except:
    # we are in watcher, no prefs needed
    pass

from contextlib import contextmanager
from pathlib import Path
import subprocess
import tempfile
import stat
import os
import json


class Git():

    @staticmethod
    def bin():
        prefs = get_preferences()
        return prefs.git_path

    @staticmethod
    def get_git_repo(path):
        path = Path(path).resolve()
        for parent in [path] + list(path.parents):
            if (parent / ".git").is_dir():
                return parent
        raise ValueError("Not a git repository!")

    @staticmethod
    @contextmanager
    def _credential_env():
        """Context manager that yields (env, git_args) for authenticated remote
        operations. Sets GIT_ASKPASS to a temp script that returns the PAT, and
        also yields '-c credential.helper=' args to disable any system credential
        manager that would otherwise intercept the request before ASKPASS is called.
        Falls back to (base_env, []) gracefully if credentials are unavailable."""
        base_env = {**os.environ, 'GIT_TERMINAL_PROMPT': '0'}

        try:
            prefs = get_preferences()
            username = prefs.username
            token = prefs.personal_access_token
            if not username or not token:
                yield base_env, []
                return
        except Exception:
            yield base_env, []
            return

        # Write a platform-appropriate GIT_ASKPASS helper.
        # Credentials are passed via env vars to avoid any shell-escaping issues.
        if os.name == 'nt':
            # Windows: .cmd file, git always asks for password only
            script = '@echo %_CAMBER_PAT%\r\n'
            suffix = '.cmd'
        else:
            # Unix: shell script that handles both username and password prompts
            script = (
                '#!/bin/sh\n'
                'case "$1" in\n'
                '  *[Uu]sername*) echo "$_CAMBER_USER" ;;\n'
                '  *) echo "$_CAMBER_PAT" ;;\n'
                'esac\n'
            )
            suffix = '.sh'

        fd, askpass_path = tempfile.mkstemp(suffix=suffix, prefix='camber_askpass_')
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(script)
            if os.name != 'nt':
                os.chmod(askpass_path, stat.S_IRWXU)

            env = {
                **base_env,
                'GIT_ASKPASS': askpass_path,
                '_CAMBER_USER': username,
                '_CAMBER_PAT': token,
            }
            # credential.helper= (empty) disables any system credential manager
            # so git falls through to GIT_ASKPASS instead of the keychain/manager
            git_args = ['-c', 'credential.helper=']
            yield env, git_args
        finally:
            try:
                os.unlink(askpass_path)
            except OSError:
                pass

    @classmethod
    def checkout(cls, hash, file_path):
        repo_dir = cls.get_git_repo(file_path)
        rel_path = os.path.relpath(file_path, repo_dir)
        subprocess.run(
<<<<<<< Updated upstream
            [f"{cls.bin()}", "checkout", hash, "--", rel_path],
=======
            [self.bin(), "checkout", hash, "--", rel_path],
>>>>>>> Stashed changes
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
                tree_cmd = [cls.bin(), "rev-parse", f"{commit_hash}:{rel_path}"]
                commit_blob = subprocess.run(tree_cmd, cwd=repo_dir, capture_output=True, text=True).stdout.strip()
                if commit_blob == current_blob:
                    return commit_hash

            return "Modified/Uncommitted"

        except Exception as e:
            print(f"Error finding current file version: {e}")
            return "Unknown"

    @classmethod
<<<<<<< Updated upstream
    def commit(cls, msg, filepath):
        repo_dir = cls.get_git_repo(filepath)
=======
    def commit(self, msg, filepath):
>>>>>>> Stashed changes
        filename = os.path.basename(filepath)
        git_bin = cls.bin()

        try:
<<<<<<< Updated upstream
            subprocess.run([git_bin, "add", filename], cwd=repo_dir, check=True, capture_output=True)
            
=======
            # 1. Stage the file
            subprocess.run([git_bin, "add", filename], cwd=repo_dir, check=True, capture_output=True, text=True)

            # 2. Check: is there actually anything staged to commit?
            # --quiet returns 0 if no changes, 1 if there are changes.
>>>>>>> Stashed changes
            change_check = subprocess.run([git_bin, "diff", "--cached", "--quiet"], cwd=repo_dir)
            if change_check.returncode == 0:
<<<<<<< Updated upstream
                return False, "No changes to commit"

            subprocess.run([git_bin, "commit", "-m", msg], cwd=repo_dir, check=True, capture_output=True)
            return True, "Committed locally"

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            return False, error_msg
        except FileNotFoundError:
            return False, "Git executable not found"
=======
                print("No changes detected. Nothing to commit.")
                return True

            # 3. Commit
            subprocess.run([git_bin, "commit", "-m", msg], cwd=repo_dir, check=True, capture_output=True, text=True)

            # 4. Push with injected credentials
            with self._credential_env() as (env, cred_args):
                subprocess.run(
                    [git_bin, *cred_args, "push"],
                    cwd=repo_dir, check=True, capture_output=True, text=True,
                    env=env
                )

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            print(f"Git Error: {error_msg}")
            return False, error_msg
        except FileNotFoundError:
            print(git_bin)
            return False, "Git executable not found. Is Git installed?"
>>>>>>> Stashed changes

    @classmethod
    def get_detailed_git_history(cls, file_path):
        if not file_path or not os.path.exists(file_path):
            return []

        repo_dir = cls.get_git_repo(file_path)
        rel_path = os.path.relpath(file_path, repo_dir).replace("\\", "/")
        git_bin = cls.bin()

        # Format: hash, author, date, message
        git_format = "%h%x09%an%x09%ad%x09%s"
        cmd = [git_bin, "log", f"--pretty=format:{git_format}", "--date=short", "--", rel_path]

        try:
            result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True, check=True)
            history = []

            for line in result.stdout.splitlines():
                if not line.strip(): continue
                parts = line.split('\t')

                if len(parts) == 4:
                    commit_hash = parts[0]

                    # Get the size of the file at THIS specific commit
                    # ls-tree -l shows the object size in bytes
                    size_cmd = [git_bin, "ls-tree", "-r", "-l", commit_hash, rel_path]
                    size_result = subprocess.run(size_cmd, cwd=repo_dir, capture_output=True, text=True)

                    # ls-tree output looks like: 100644 blob <hash> <size>    <path>
                    size_str = "Unknown"
                    if size_result.stdout:
                        size_parts = size_result.stdout.split()
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

            return history

        except Exception as e:
            print(f"Error fetching history with sizes: {e}")
            return []

    @classmethod
    def get_git_history(cls, file_path):
        """
        Returns a list of dictionaries containing commit history for a specific file.
        """
        if not file_path or not os.path.exists(file_path):
            return []

<<<<<<< Updated upstream
        repo_dir = cls.get_git_repo(file_path)

        rel_path = os.path.relpath(file_path, repo_dir)

        git_format = "%h%x09%an%x09%ad%x09%s"
        
        cmd = [
            cls.bin(), "log", 
            f"--pretty=format:{git_format}", 
            "--date=short", 
            "--", rel_path
        ]
=======
        repo_dir = self.get_git_repo(file_path)
        rel_path = os.path.relpath(file_path, repo_dir)

        # %h = short hash, %an = author name, %ad = date, %s = subject (message)
        git_format = "%h%x09%an%x09%ad%x09%s"
        cmd = [self.bin(), "log", f"--pretty=format:{git_format}", "--date=short", "--", rel_path]
>>>>>>> Stashed changes

        try:
            result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True, check=True)

            history = []
            for line in result.stdout.splitlines():
                if not line.strip():
                    continue
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

    @classmethod
    def fetch(cls, file_path):
        """Updates the local database with objects and refs from the remote."""
        repo_dir = cls.get_git_repo(file_path)
        try:
            with cls._credential_env() as (env, cred_args):
                result = subprocess.run(
                    [cls.bin(), *cred_args, "fetch"],
                    cwd=repo_dir,
                    capture_output=True,
                    text=True,
                    check=True,
                    env=env
                )
            # Git fetch outputs status to stderr even on success
            fetch_summary = result.stderr.strip()
            return True, fetch_summary
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            print(f"Git Fetch Error: {error_msg}")
            return False, error_msg

    @classmethod
    def pull(cls, file_path):
        """
        Incorporate changes from a remote repository into the current branch.
        """
        repo_dir = cls.get_git_repo(file_path)
        try:
            with cls._credential_env() as (env, cred_args):
                result = subprocess.run(
                    [cls.bin(), *cred_args, "pull"],
                    cwd=repo_dir, check=True, capture_output=True, text=True,
                    env=env
                )
            print(result.stderr.strip())
            return True, "Success"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            print(f"Git Pull Error: {error_msg}")
            return False, error_msg
<<<<<<< Updated upstream

    @classmethod
    def push(cls, file_path):
        repo_dir = cls.get_git_repo(file_path)
        try:
            result = subprocess.run(
                [cls.bin(), "push"],
                cwd=repo_dir, capture_output=True, text=True, check=True
            )
            return True, result.stderr.strip() or "Push successful"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            return False, error_msg

    @classmethod
    def get_current_user(cls):
        """Get the current Git user name and email."""
        git_bin = cls.bin()
        try:
            name = subprocess.run(
                [git_bin, "config", "--get", "user.name"],
                capture_output=True, text=True, check=True
            ).stdout.strip()
            email = subprocess.run(
                [git_bin, "config", "--get", "user.email"],
                capture_output=True, text=True, check=True
            ).stdout.strip()
            return {"name": name, "email": email}
        except subprocess.CalledProcessError:
            return {"name": None, "email": None}

    @classmethod
    def lfs_list_locks(cls, file_path):
        """List all LFS locks in the repository. Returns list of lock dicts."""
        repo_dir = cls.get_git_repo(file_path)
        git_bin = cls.bin()
        try:
            result = subprocess.run(
                [git_bin, "lfs", "locks", "--json"],
                cwd=repo_dir, capture_output=True, text=True, check=True
            )
            if result.stdout:
                data = json.loads(result.stdout)
                return data
            return []
        except subprocess.CalledProcessError:
            return []
        except json.JSONDecodeError:
            return []

    @classmethod
    def lfs_get_lock(cls, file_path):
        """Get lock info for a specific file. Returns {id, owner, path} or None."""
        locks = cls.lfs_list_locks(file_path)
        repo_dir = cls.get_git_repo(file_path)
        rel_path = os.path.relpath(file_path, repo_dir).replace("\\", "/")
        for lock in locks:
            if lock.get("path") == rel_path:
                return {
                    "id": lock.get("id"),
                    "owner": lock.get("owner", {}).get("name"),
                    "path": lock.get("path")
                }
        return None

    @classmethod
    def lfs_lock(cls, file_path):
        """Lock a file using git lfs lock."""
        repo_dir = cls.get_git_repo(file_path)
        git_bin = cls.bin()
        try:
            subprocess.run(
                [git_bin, "lfs", "lock", file_path],
                cwd=repo_dir, capture_output=True, text=True, check=True
            )
            return True, "File locked"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else e.stdout.strip() if e.stdout else str(e)
            return False, error_msg

    @classmethod
    def lfs_unlock(cls, lock_id):
        """Unlock a file using git lfs unlock by lock ID."""
        git_bin = cls.bin()
        try:
            subprocess.run(
                [git_bin, "lfs", "unlock", str(lock_id)],
                capture_output=True, text=True, check=True
            )
            return True, "File unlocked"
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else e.stdout.strip() if e.stdout else str(e)
            return False, error_msg
=======
>>>>>>> Stashed changes
