import sys
import os
import time

pid, file_path, root, owner, repo, user, token, addon_path = sys.argv[1:]

sys.path.append(addon_path)
from msc.api import API

class MockSecrets:
    def __init__(self):
        self.root = root
        self.owner = owner
        self.repo = repo
        self.username = user
        self.token = token

def watch_and_unlock():
    # Wait for Blender to die
    while True:
        try:
            os.kill(int(pid), 0)
            print("still running")
        except OSError:
            break
        time.sleep(2)

    # Reconstruct the API with mock secrets
    api = API(manual_secrets=MockSecrets())
    
    lock_id = api.find_lock_id_by_path(file_path)
    if lock_id:
        api.unlock(lock_id)

if __name__ == "__main__":
    watch_and_unlock()