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
    def GENERIC_HEADER(self):
        return {
        "Authorization": f"token {self.sec.token}",
        "Content-Type": "application/json"
    }
    
    @property
    def AUTH(self):
        return HTTPBasicAuth(self.sec.username, self.sec.token)

    def add_file():
        pass

    def commit():
        pass

    def is_file_locked(self, file_path):
            
            Git.fetch(file_path)

            """
            Returns the lock object if the file is locked, otherwise None.
            file_path: absolute path
            """

            rel_path = self.convert_abs_to_relpath(file_path)
            url = f"{self.sec.root}/{self.sec.owner}/{self.sec.repo}.git/info/lfs/locks"
            
            try:
                response = requests.get(
                    url, 
                    headers=self.LFS_HEADER, 
                    auth=self.AUTH
                )
                
                if response.status_code == 200:
                    locks = response.json().get('locks', [])
                    
                    for lock in locks:
                        if lock.get('path') == rel_path:
                            return lock # Return the whole dict so you have the ID/Owner
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
    
    def is_current_user_lock_owner(lock_owner_name):
        """
        Checks if the owner of the file lock matches the configured username in preferences.
        """
        if not lock_owner_name:
            return False
            
        prefs = get_preferences()
        if not prefs:
            print("Warning: Could not fetch addon preferences.")
            return False
            
        # Compare case-insensitively just to be safe
        return prefs.username.strip().lower() == lock_owner_name.strip().lower()
    
    def authenticate_user(self, username):
        """
        Verifies identity via Forgejo API and checks against the lock owner.
        """
        prefs = get_preferences()
        token = prefs.forgejo_token
        server = prefs.server_url.rstrip('/')
        
        # Forgejo / Gitea 'Get Authenticated User' endpoint
        url = f"{self.sec.root}/api/v1/user"

        try:
            response = requests.get(url, headers=self.GENERIC_HEADER, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                authenticated_username = data.get("username", "")
                print("authenticating username:", authenticated_username)
                
                # Compare the actual account name from the server to the lock owner
                return authenticated_username.lower() == username.lower()
            else:
                print(f"Auth failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Connection error during auth: {e}")
            return False