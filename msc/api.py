try:
    import bpy
    from ..constants import get_preferences
except ImportError:
    # We are in the watcher; these won't be used anyway
    bpy = None
    get_preferences = None

import requests
from requests.auth import HTTPBasicAuth
import json
import os

from .git import Git

class Secrets():
    @property
    def prefs(self):
        p = get_preferences()
        if not p:
            raise Exception("Addon preferences not found. Is the addon registered?")
        return p

    @property
    def root(self):
        return self.prefs.server_url

    @property
    def repo(self):
        return self.prefs.repository_name

    @property
    def username(self):
        return self.prefs.username

    @property
    def token(self):
        return self.prefs.forgejo_token
    
    @property
    def owner(self):
        return self.prefs.owner

class API():
    def __init__(self, manual_secrets=None):
        # If we are in the watcher, we pass secrets manually
        # If in Blender, it uses the Secrets() class which hits prefs
        self.sec = manual_secrets if manual_secrets else Secrets()

    @property
    def LFS_HEADER(self):
        return {
            "Accept": "application/vnd.git-lfs+json",
            "Content-Type": "application/vnd.git-lfs+json"
        }
    
    @property
    def AUTH(self):
        return HTTPBasicAuth(self.sec.username, self.sec.token)

    def add_file():
        pass

    def commit():
        pass

    def is_file_locked(self, file_path):
            """
            Returns the lock object if the file is locked, otherwise None.
            file_path: relative path from repo root (e.g. 'assets/hero.blend')
            """
            # The URL we verified earlier
            url = f"{self.sec.root}/{self.sec.owner}/{self.sec.repo}.git/info/lfs/locks"
            
            try:
                response = requests.get(
                    url, 
                    headers=self.LFS_HEADER, 
                    auth=self.AUTH
                )
                
                if response.status_code == 200:
                    locks = response.json().get('locks', [])
                    
                    # Search for the file path in the list of locks
                    for lock in locks:
                        if lock.get('path') == file_path:
                            print(f"🚩 File is locked by {lock['owner']['name']}")
                            return lock # Return the whole dict so you have the ID/Owner
                    
                    print("✅ File is free to be locked.")
                    return None
                else:
                    print(f"Error checking locks: {response.status_code}")
                    return None
                    
            except Exception as e:
                print(f"Connection failed: {e}")
                return None

    def lock(self, absolute_file_path):
            """API call to lock a file on Forgejo."""
            rel_path = self.convert_abs_to_relpath(absolute_file_path)

            url = f"{self.sec.root}/{self.sec.owner}/{self.sec.repo}.git/info/lfs/locks"
            payload = {"path": rel_path}
            
            response = requests.post(
                url, 
                headers=self.LFS_HEADER, 
                auth=self.AUTH, 
                data=json.dumps(payload)
            )
            
            if response.status_code == 201:
                print(f"Locked {absolute_file_path}")
                return response.json() # Returns the lock ID
            else:
                print(f"Lock failed: {response.text} for {absolute_file_path}")
                return None

    def unlock(self, lock_id):
            """API call to release a lock using its ID."""
            # Endpoint: .../info/lfs/locks/{id}/unlock
            url = f"{self.sec.root}/{self.sec.owner}/{self.sec.repo}.git/info/lfs/locks/{lock_id}/unlock"
            
            response = requests.post(
                url, 
                headers=self.LFS_HEADER, 
                auth=self.AUTH,
                json={}
            )
            
            if response.status_code in [200, 204]:
                return True
            else:
                return False

    def find_lock_id_by_path(self, absolute_file_path):
        rel_path = self.convert_abs_to_relpath(absolute_file_path)
        url = f"{self.sec.root}/{self.sec.owner}/{self.sec.repo}.git/info/lfs/locks/"
        response = requests.get(url, headers=self.LFS_HEADER, auth=self.AUTH)
        
        if response.status_code == 200:
            locks = response.json().get('locks', [])
            for l in locks:
                # Now the comparison is apples-to-apples
                if l.get('path') == rel_path:
                    return l.get('id')
        return None
    
    def convert_abs_to_relpath(self, absolute_file_path):
        repo_dir = Git.get_git_repo(absolute_file_path)
        
        rel_path = os.path.relpath(absolute_file_path, repo_dir)
        
        rel_path = rel_path.replace(os.sep, '/')
        return rel_path