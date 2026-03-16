class Session:
    _instance = None

    username = None
    repository_url = None
    authenticated = False
    git_bin = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.username = None
            cls._instance.repository_url = None
            cls._instance.authenticated = False
            cls._instance.git_bin = None
        return cls._instance

def get_session() -> Session:
    return Session()