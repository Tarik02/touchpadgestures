from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    x: int
    y: int
    force: int
    fingers: int
    area: int

    @property
    def is_end(self):
        return self.force == 0 and self.fingers == 0 and self.area == 0
