try:
    import bpy
    from ..constants import get_preferences
except ImportError:
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
        return self.prefs.personal_access_token

    @property
    def owner(self):
        return self.prefs.owner


class API():
    def __init__(self, manual_secrets=None):
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

    @property
    def locks_url(self):
        return f"{self.sec.root}/{self.sec.owner}/{self.sec.repo}.git/info/lfs/locks"

    def add_file(self):
        pass

    def commit(self):
        pass

    def verify_credentials(self):
        try:
            response = requests.get(
                self.locks_url,
                headers=self.LFS_HEADER,
                auth=self.AUTH,
                params={"limit": 1},
                timeout=10
            )
            
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                print("Authentication failed: Invalid credentials")
                return False
            else:
                print(f"Verification failed with status: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print("Connection timeout during verification")
            return False
        except requests.exceptions.ConnectionError:
            print("Connection error during verification")
            return False
        except Exception as e:
            print(f"Verification error: {e}")
            return False

    def get_verified_username(self):
        try:
            response = requests.get(
                self.locks_url,
                headers=self.LFS_HEADER,
                auth=self.AUTH,
                params={"limit": 1},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                locks = data.get('locks', [])
                if locks and len(locks) > 0:
                    return locks[0].get('owner', {}).get('name')
                
                if 'next_cursor' in data:
                    return self.sec.username
                return self.sec.username
            return None
                
        except Exception as e:
            print(f"Error getting verified username: {e}")
            return None

    def get_locked_files(self, path_filter=None):
        all_locks = []
        cursor = None
        
        while True:
            params = {"limit": 100}
            if cursor:
                params["cursor"] = cursor
                
            try:
                response = requests.get(
                    self.locks_url,
                    headers=self.LFS_HEADER,
                    auth=self.AUTH,
                    params=params,
                    timeout=10
                )
                
                if response.status_code != 200:
                    break
                    
                data = response.json()
                locks = data.get('locks', [])
                
                for lock in locks:
                    if path_filter is None or path_filter in lock.get('path', ''):
                        all_locks.append(lock)
                
                cursor = data.get('next_cursor')
                if not cursor:
                    break
                    
            except Exception as e:
                print(f"Error fetching locks: {e}")
                break
                
        return all_locks

    def is_file_locked(self, file_path):
        Git.fetch(file_path)
        
        rel_path = self.convert_abs_to_relpath(file_path)
        
        try:
            response = requests.get(
                self.locks_url, 
                headers=self.LFS_HEADER, 
                auth=self.AUTH,
                params={"path": rel_path}
            )
            
            if response.status_code == 200:
                locks = response.json().get('locks', [])
                
                for lock in locks:
                    if lock.get('path') == rel_path:
                        return lock
                return None
            else:
                print(f"Error checking locks: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Connection failed: {e}")
            return None

    def lock(self, absolute_file_path):
        rel_path = self.convert_abs_to_relpath(absolute_file_path)
        payload = {"path": rel_path}
        
        response = requests.post(
            self.locks_url, 
            headers=self.LFS_HEADER, 
            auth=self.AUTH, 
            data=json.dumps(payload)
        )
        
        if response.status_code == 201:
            print(f"Locked {absolute_file_path}")
            return response.json()
        else:
            print(f"Lock failed: {response.text} for {absolute_file_path}")
            return None

    def unlock(self, lock_id):
        url = f"{self.locks_url}/{lock_id}/unlock"
        
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
        response = requests.get(
            self.locks_url, 
            headers=self.LFS_HEADER, 
            auth=self.AUTH,
            params={"path": rel_path}
        )
        
        if response.status_code == 200:
            locks = response.json().get('locks', [])
            for lock in locks:
                if lock.get('path') == rel_path:
                    return lock.get('id')
        return None
    
    def convert_abs_to_relpath(self, absolute_file_path):
        repo_dir = Git.get_git_repo(absolute_file_path)
        rel_path = os.path.relpath(absolute_file_path, repo_dir)
        rel_path = rel_path.replace(os.sep, '/')
        return rel_path
    
    def is_current_user_lock_owner(self, lock_owner_name):
        if not lock_owner_name:
            return False
            
        prefs = get_preferences()
        if not prefs:
            print("Warning: Could not fetch addon preferences.")
            return False
            
        verified = prefs.verified_username
        if verified:
            return verified.strip().lower() == lock_owner_name.strip().lower()
            
        return prefs.username.strip().lower() == lock_owner_name.strip().lower()
