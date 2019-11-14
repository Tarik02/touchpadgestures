import abc
from typing import List


class Detector(abc.ABC):
    def __init__(self, app):
        self.app = app

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    def begin(self):
        pass

    def end(self, cancel: bool):
        pass

    @abc.abstractmethod
    def handle(self, time: float, x: int, y: int, force: int, fingers: int, area: int) -> bool:
        pass

    def handle_timer(self, time: float):
        pass

    def set_timer(self, time: float):
        self.app.set_timer(self, time)

    def exec(self, action: str, *args: str):
        self.app.exec(self, action, args)
