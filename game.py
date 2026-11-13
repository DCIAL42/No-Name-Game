from typing import Tuple
from typing import Self
from types import TracebackType
import pygame
import time

from common import Vec2
from entity import Boss, Player, Enemy, Collectible, NormalMovement, EraticMovement

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
BACKGROUND = (153, 0, 48)

pygame.init()

pygame.mixer.music.load("Boke, The Soundtrack.mp3")
pygame.mixer.music.play(-1)

deathSound = pygame.mixer.Sound("End.mp3")
collectSound = pygame.mixer.Sound("Collect.mp3")
killSound = pygame.mixer.Sound("Enemy.mp3")
deathSound.set_volume(0.5)
collectSound.set_volume(0.5)
killSound.set_volume(0.5)


class Game:
    def __init__(self: Self):
        self.score = 0
        self.scores = [self.score]
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont("Arial", 32)
        self.bigFont = pygame.font.SysFont("Arial", 64)
        self.superMode = False
        self.isBoss = False
        self.lossCount = 0
        self.pauseCount = 0
        self.boss = Boss(Vec2(736, 0), PURPLE, 64)
        self.player = Player(Vec2(400, 300), GREEN, 16)
        self.boke = Collectible(Vec2(0, 0), RED, 16)
        self.enemies = [
            Enemy(Vec2(0, 0), BLUE, 16, NormalMovement(100)),
            Enemy(Vec2(784, 0), BLUE, 64, NormalMovement(500)),
            Enemy(Vec2(0, 584), BLUE, 16, EraticMovement())
        ]
        self.running = True
        self.paused = True
        self.pauseDuration = 0

    def checkQuit(self: Self):
        if pygame.QUIT in [e.type for e in pygame.event.get()]:
            pygame.display.quit()

    def resetValues(self: Self):
        self.score = 0 if not self.isBoss else 30
        self.scores = [self.score]
        self.player.pos = Vec2(400, 300)
        for e in self.enemies:
            e.pos = e.spawn
            e.isAlive = True
        self.boke.isAlive = False
        self.boss.isAlive = True

    def pauseScreen(self: Self):
        pauseDisplay = self.bigFont.render(
            ("Game Paused"), True, WHITE)
        playDisplay = self.font.render(
            ("Press enter to play"), True, WHITE)
        while self.paused:
            # Display pause screen
            self.screen.fill(BACKGROUND)
            self.screen.blit(pauseDisplay, (225, 200))
            self.screen.blit(playDisplay, (290, 375))
            pygame.display.update()
            self.checkQuit()
            # Check for input
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                self.paused = False

    def creditsScreen(self: Self):
        titleDisplay = self.bigFont.render(
            ("Boke, The Game"), True, WHITE)
        creditsDisplay = self.bigFont.render(
            ("Credits"), True, WHITE)
        credits1 = self.font.render(
            ("Lead Programmer: Daniel Cooke"), True, WHITE)
        credits2 = self.font.render(
            ("Music By: Conor Lyons"), True, WHITE)
        titleDisplayy = 600
        creditsDisplayy = 750
        credits1y = 925
        credits2y = 1000
        while True:
            # Display credits screen
            self.screen.fill(BACKGROUND)
            self.screen.blit(titleDisplay, (210, titleDisplayy))
            self.screen.blit(creditsDisplay, (325, creditsDisplayy))
            self.screen.blit(credits1, (200, credits1y))
            self.screen.blit(credits2, (200, credits2y))
            titleDisplayy -= 0.1
            creditsDisplayy -= 0.1
            credits1y -= 0.1
            credits2y -= 0.1
            pygame.display.update()
            self.checkQuit()
            if credits2y < 0:
                break

    def endScreen(self: Self, message: str, messageColour: Tuple[int, int, int], messagePosition: Tuple[int, int]):
        if message == "You Win!":
            pygame.mixer.music.load("Boke, Win Theme.mp3")
            pygame.mixer.music.play(-1)
            self.creditsScreen()
        scoreDisplay = self.font.render(
            (f"Score: {self.score}"), True, WHITE)
        checkMicrobit = self.font.render(
            ("Press enter to continue"), True, WHITE)
        outcomeMessage = self.bigFont.render((message), True, messageColour)
        while True:
            # Display end screen
            self.screen.fill(BACKGROUND)
            self.screen.blit(scoreDisplay, (0, 0))
            self.screen.blit(checkMicrobit, (250, 375))
            self.screen.blit(outcomeMessage, messagePosition)
            pygame.display.update()
            self.checkQuit()
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                self.resetValues()
                break

    def spawnBoss(self: Self):
        self.boss.pos = Vec2(736, 0)
        self.boss.size = 0
        while True:
            self.screen.fill(BACKGROUND)
            scoreDisplay = self.font.render(
                (f"Score: {self.score}"), True, WHITE)
            self.screen.blit(scoreDisplay, (0, 0))
            spawningBossRect = pygame.Rect(
                (800-self.boss.size, 0, self.boss.size, self.boss.size))
            pygame.draw.rect(self.screen, PURPLE, spawningBossRect)
            self.boss.size += 0.01
            self.player.move(self)
            self.player.display(self.screen)
            if self.player.checkCollision(spawningBossRect):
                deathSound.play()
                self.endScreen("You Lose", RED, (275, 200))
            self.checkQuit()
            pygame.display.update()
            if self.boss.size > 64:
                break

    def updateGame(self: Self):
        if self.paused:
            self.pauseScreen()
        # Check for supermode
        if not self.score % 10 and self.score not in self.scores:
            self.superMode = True
            self.boke.isAlive = False
            self.boke.pos = Vec2(999, 999)
            self.boke.updateRect()
        # Move and display characters
        self.player.move(self)
        for enemy in self.enemies:
            if enemy.isAlive:
                enemy.move(self)
        if self.superMode:
            self.player.spriteColour = (255, 255, 0)
        else:
            self.player.spriteColour = GREEN
            self.boke.spawnCollectible()
        # Check for collisions
        if self.player.checkCollision(self.boke.charRect):
            self.boke.isAlive = False
            collectSound.play()
            self.score += 10
        if any(self.player.checkCollision(e.charRect) for e in self.enemies):
            if self.superMode:
                for e in self.enemies:
                    if self.player.checkCollision(e.charRect):
                        e.killEnemy()
                        killSound.play()
                self.scores.append(self.score)
            else:
                deathSound.play()
                self.endScreen("You Lose", RED, (275, 200))
            self.superMode = False
        # If all enemies dead, display win screen
        if all(not i.isAlive for i in self.enemies):
            pygame.mixer.music.load("Boke, Boss theme v2.mp3")
            pygame.mixer.music.play(-1)
            self.isBoss = True
            self.finalBoss()
        self.checkQuit()

    def drawGame(self: Self):
        self.screen.fill(BACKGROUND)
        scoreDisplay = self.font.render(
            (f"Score: {self.score}"), True, WHITE)
        self.screen.blit(scoreDisplay, (0, 0))
        # Check for supermode
        if not self.score % 10 and self.score not in self.scores:
            self.boke.display(self.screen)
        # Move and display characters
        self.player.display(self.screen)
        for enemy in self.enemies:
            if enemy.isAlive:
                enemy.display(self.screen)
        if not self.superMode:
            self.boke.display(self.screen)
        # Check for collisions
        pygame.display.update()

    def finalBoss(self: Self):
        self.spawnBoss()
        while True:
            self.screen.fill(BACKGROUND)
            scoreDisplay = self.font.render(
                (f"Score: {self.score}"), True, WHITE)
            self.screen.blit(scoreDisplay, (0, 0))
            # Check for supermode
            if not self.score % 10 and self.score not in self.scores:
                self.superMode = True
                self.boke.isAlive = False
                self.boke.pos = Vec2(999, 999)
                self.boke.updateRect()
                self.boke.display(self.screen)
            # Move and display characters
            self.player.move(self)
            self.player.display(self.screen)
            if self.boss.isAlive:
                self.boss.move(self)
                self.boss.display(self.screen)
            if self.superMode:
                self.player.spriteColour = (255, 255, 0)
            else:
                self.player.spriteColour = GREEN
                self.boke.spawnCollectible()
                self.boke.display(self.screen)
            # Check for collisions
            if self.player.checkCollision(self.boke.charRect):
                self.boke.isAlive = False
                collectSound.play()
                self.score += 10
            if self.player.checkCollision(self.boss.charRect):
                if self.superMode:
                    self.boss.killBoss()
                    killSound.play()
                    self.scores.append(self.score)
                else:
                    deathSound.play()
                    self.endScreen("You Lose", RED, (275, 200))
                    self.spawnBoss()
                self.superMode = False
            # If all enemies dead, display win screen
            if not self.boss.isAlive:
                self.endScreen("You Win!", GREEN, (300, 200))
                self.isBoss = False
                pygame.mixer.music.load("Boke, The Soundtrack.mp3")
                pygame.mixer.music.play(-1)
                break
            self.checkQuit()
            pygame.display.update()
            time.sleep(0.001)

    def gameLoop(self: Self):
        while self.running:
            try:
                self.updateGame()
                self.drawGame()
                time.sleep(0.0025)
            except Exception as e:
                tb: TracebackType | None = e.__traceback__
                if tb is None:
                    break
                print(
                    f"{tb.tb_frame.f_code.co_filename} {tb.tb_lineno}: Error: {e}")
                break
