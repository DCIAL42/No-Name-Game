from typing import Self
import pygame
from dataclasses import dataclass
from collections.abc import Sequence

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
BACKGROUND = (153, 0, 48)


@dataclass
class Vec2:
    x: float
    y: float

    @classmethod
    def from_any(cls: type, value: Sequence | Self):
        if isinstance(value, cls):
            return value
        if isinstance(value, Sequence) and len(value) == 2:
            return cls(*value)

    def __add__(self: Self, other: Sequence | Self):
        other = self.from_any(other)
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self: Self, other: Sequence | Self):
        other = self.from_any(other)
        return Vec2(self.x - other.x, self.y - other.y)

    def __iadd__(self: Self, other: Sequence | Self):
        other = self.from_any(other)
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self: Self, other: Sequence | Self):
        other = self.from_any(other)
        self.x -= other.x
        self.y -= other.y
        return self

    def __truediv__(self: Self, other: float):
        return Vec2(self.x / other, self.y / other)

    def __itruediv__(self: Self, other: float):
        self.x /= other
        self.y /= other
        return self

    def __mul__(self: Self, other: float | int):
        return Vec2(self.x * other, self.y * other)

    def __imul__(self: Self, other: float | int):
        self.x *= other
        self.y *= other
        return self


def timeConvert(sec: float, checker: str):
    # Convert seconds to minutes and seconds
    mins, sec = divmod(sec, 60)
    if checker == "fullTime":
        return f"{int(mins)}:{int(sec)}"
    if mins % 15 == 0 and mins != 0:
        return True


enemyMovement = {
    1: Vec2(1, 1),
    2: Vec2(-1, -1),
    3: Vec2(-1, 1)
}

playerMovement = {
    pygame.K_a: Vec2(-1, 0),
    pygame.K_s: Vec2(0, 1),
    pygame.K_d: Vec2(1, 0),
    pygame.K_w: Vec2(0, -1)
}
