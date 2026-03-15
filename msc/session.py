from .api import API
from .git import Git
from ..constants import get_preferences

class Session():
    api = None
    authentication = None

    @staticmethod
    def get_api():
        if Session.api is None:
            Session.api = API()
        return Session.api
    
    
    @staticmethod
    def get_session():
        """Return the singleton session, lazily creating the API client if needed."""
        if Session.api is None:
            Session.api = API()

        if Session.authentication is None:
            username = get_preferences().username
            Session.authentication = Session.api.authenticate_user(username)
        return Session