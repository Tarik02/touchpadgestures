from dataclasses import dataclass


@dataclass(frozen=True)
class Info:
    left: int
    top: int
    right: int
    bottom: int
