from __future__ import annotations

from typing import Self, TYPE_CHECKING
import pygame
from random import randint
from abc import ABC, abstractmethod
from dataclasses import replace

from common import Vec2, playerMovement

if TYPE_CHECKING:
    from game import Game


class MovementStrategy(ABC):
    speed: int

    def __init__(self: Self, speed: int = 1):
        self.speed = speed

    def _goToSpawn(self: Self, entity: Enemy):
        move: Vec2 = Vec2(1, 1)
        if entity.spawn.x < 800 // 2:
            move.x *= -1
        if entity.spawn.y < 600 // 2:
            move.y *= -1
        entity.pos += move

    @abstractmethod
    def move(self: Self, entity: Enemy, game: Game):
        pass


class EraticMovement(MovementStrategy):
    def __init__(self: Self, speed: int = 1) -> None:
        super().__init__(speed)

    def move(self: Self, entity: Enemy, game: Game):
        if game.superMode or game.isBoss:
            self._goToSpawn(entity)
        elif randint(0, 1):
            if game.player.pos.x >= entity.pos.x:
                entity.pos.x += 1
            if game.player.pos.x <= entity.pos.x:
                entity.pos.x -= 1
        else:
            if game.player.pos.y >= entity.pos.y:
                entity.pos.y += 1
            if game.player.pos.y <= entity.pos.y:
                entity.pos.y -= 1
        entity.checkBoundaries()
        entity.updateRect()


class NormalMovement(MovementStrategy):
    def __init__(self: Self, speed: int = 1):
        super().__init__(speed)

    def move(self: Self, entity: Enemy, game: Game):
        if game.superMode or game.isBoss:
            self._goToSpawn(entity)
        else:
            entity.pos += (game.player.pos - entity.pos) / self.speed
        entity.checkBoundaries()
        entity.updateRect()


class PlayerMovement(MovementStrategy):
    pass


class Entity:
    def __init__(self: Self, pos: Vec2, spriteColour: tuple, size: float):
        self.pos = pos
        self.size = size
        self.spriteColour = spriteColour
        self.updateRect()

    def updateRect(self: Self):
        self.charRect = pygame.Rect(
            self.pos.x, self.pos.y, self.size, self.size)

    def display(self: Self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.spriteColour, self.charRect)

    def checkBoundaries(self: Self):
        self.pos.x = max(0, min(800 - self.size, self.pos.x))
        self.pos.y = max(0, min(600 - self.size, self.pos.y))

    def checkCollision(self: Self, target: pygame.Rect):
        return self.charRect.colliderect(target)


class Enemy(Entity):
    def __init__(self: Self, pos: Vec2, spriteColour: tuple, size: float, movementStrategy: MovementStrategy, isAlive: bool = True):
        super().__init__(pos, spriteColour, size)
        self.movementStrategy = movementStrategy
        self.isAlive = isAlive
        self.spawn = replace(pos)

    def move(self: Self, game: Game):
        self.movementStrategy.move(self, game)
        self.checkBoundaries()
        self.updateRect()

    def killEnemy(self: Self):
        # Spawn enemy outside of screen when killed
        self.isAlive = False
        self.pos = Vec2(999, 999)
        self.updateRect()

    def resetPosition(self: Self):
        self.pos = self.spawn


class Boss(Entity):
    def __init__(self: Self, pos: Vec2, spriteColour: tuple, size: float):
        super().__init__(pos, spriteColour, size)
        self.isAlive = True

    def move(self: Self, game: Game):
        self.pos += (game.player.pos - self.pos) / 75
        self.checkBoundaries()
        self.updateRect()

    def killBoss(self: Self):
        self.isAlive = False
        self.pos = Vec2(999, 999)
        self.updateRect()


class Player(Entity):
    def __init__(self: Self, pos: Vec2, spriteColour: tuple, size: float):
        super().__init__(pos, spriteColour, size)

    def move(self: Self, game: Game):
        key = pygame.key.get_pressed()
        # Speed multiplier for supermode
        speedMultiplier = 2 if game.superMode else 1
        for keyType in playerMovement:
            if key[keyType]:
                self.pos += playerMovement[keyType] * speedMultiplier
        self.checkBoundaries()
        self.updateRect()


class Collectible(Entity):
    def __init__(self: Self, pos: Vec2, spriteColour: tuple, size: float, isAlive: bool = False):
        super().__init__(pos, spriteColour, size)
        self.isAlive = isAlive

    def spawnCollectible(self: Self):
        # Spawn collectible if not already spawned
        if not self.isAlive:
            self.pos = Vec2(randint(0, 784), randint(0, 584))
            self.isAlive = True
        self.updateRect()
