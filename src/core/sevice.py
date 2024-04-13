from src.core.depends import InjectSession


class Service:
    def __init__(self, session: InjectSession) -> None:
        self.session = session
