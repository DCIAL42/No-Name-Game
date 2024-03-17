import pygame
import time
from random import randint

pygame.init()

pygame.mixer.music.load("Boke, The Soundtrack.mp3")
pygame.mixer.music.play(-1)

deathSound = pygame.mixer.Sound("End.mp3")
collectSound = pygame.mixer.Sound("Collect.mp3")
killSound = pygame.mixer.Sound("Enemy.mp3")
deathSound.set_volume(0.5)
collectSound.set_volume(0.5)
killSound.set_volume(0.5)

enemyMovement = {
        1:(1, 1),
        2:(-1, -1),
        3:(-1, 1)
        }
playerMovement = {
        pygame.K_a: (-1, 0),
        pygame.K_s: (0, 1),
        pygame.K_d: (1, 0),
        pygame.K_w: (0, -1)
        }

class Game:
    def __init__(self):
        self.score = 0
        self.scores = []
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont("Arial", 32)
        self.bigFont = pygame.font.SysFont("Arial", 64)
        self.superMode = False
        self.isBoss = False
        self.lossCount = 0
        self.pauseCount = 0
        self.enemy1 = Enemy(0, 0, (0, 0, 255), 16, 1)
        self.enemy2 = Enemy(784, 0, (0, 0, 255), 64, 2)
        self.enemy3 = Enemy(0, 584, (0, 0, 255), 16, 3)
        self.player = Player(400, 300, (0, 255, 0), 16)
        self.boke = Collectible(0, 0, (255, 0, 0), 16)
        self.enemyList = [self.enemy1, self.enemy2, self.enemy3]
        self.running = True
        self.paused = True
        self.pauseDuration = 0

    def checkQuit(self):
        for event in pygame.event.get():
            pygame.display.quit() if event.type == pygame.QUIT else 0

    def resetValues(self):
        self.score = 0
        self.scores = []
        self.player.x, self.player.y = 400, 300
        self.enemy1.x, self.enemy1.y = 0, 0
        self.enemy2.x, self.enemy2.y = 784, 0
        self.enemy3.x, self.enemy3.y = 0, 584
        self.enemy1.isAlive = True
        self.enemy2.isAlive = True
        self.enemy3.isAlive = True
        self.boke.isAlive = False
        self.isBoss = False

    def pauseScreen(self):
        pauseDisplay = self.bigFont.render(("Game Paused"), True, (255, 255, 255))
        playDisplay = self.font.render(("Press enter to play"), True, (255, 255, 255))
        while self.paused:
            # Display pause screen
            self.screen.fill((153, 0, 48))
            self.screen.blit(pauseDisplay, (225, 200))
            self.screen.blit(playDisplay, (290, 375))
            pygame.display.update()
            self.checkQuit()
            # Check for input
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                self.paused = False

    def endScreen(self, message, messageColour, messagePosition):
        scoreDisplay = self.font.render((f"Score: {self.score}"), True, (255, 255, 255))
        checkMicrobit = self.font.render((f"Press enter to continue"), True, (255, 255, 255))
        outcomeMessage = self.bigFont.render((message), True, messageColour)
        while True:
            # Display end screen
            self.screen.fill((153, 0, 48))
            self.screen.blit(scoreDisplay, (0, 0))
            self.screen.blit(checkMicrobit, (250, 375))
            self.screen.blit(outcomeMessage, messagePosition)
            pygame.display.update()
            self.checkQuit()
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                self.resetValues()
                break

    def finalBoss(self):
        boss = Boss(768, 0, (255, 0, 255), 64)
        while True:
            self.screen.fill((153, 0, 48))
            scoreDisplay = self.font.render((f"Score: {self.score}"), True, (255, 255, 255))
            self.screen.blit(scoreDisplay, (0, 0))
            # Check for supermode
            if self.score % 10 == 0 and self.score not in self.scores and self.score != 0:
                self.superMode = True
                self.boke.isAlive = False
                self.boke.x, self.boke.y = 999, 999
                self.boke.displayChar()
            # Move and display characters
            self.player.move(playerMovement)
            self.player.displayChar()
            if boss.isAlive:
                boss.move()
                boss.displayChar()
            if self.superMode:
                self.player.spriteColour = (255, 255, 0)
            else:
                self.player.spriteColour = (0, 255, 0)
                self.boke.spawnCollectible()
            # Check for collisions
            if self.player.checkCollision(self.boke.charRect):
                self.boke.isAlive = False
                collectSound.play()
                self.score += 1
            if self.player.checkCollision(boss.charRect):
                if self.superMode:
                    if self.player.checkCollision(boss.charRect):
                        boss.killBoss()
                        killSound.play()
                    self.scores.append(self.score)
                else:
                    deathSound.play()
                    self.endScreen("You Lose", (255, 0, 0), (275, 200))
                    break
                self.superMode = False
            # If all enemies dead, display win screen
            if not boss.isAlive:
                self.endScreen("You Win!", (0, 255, 0), (300, 200))
                break
            self.checkQuit()
            pygame.display.update()
            time.sleep(0.001)

    def gameLoop(self):
        while self.running:
            try:
                self.pauseScreen()
                self.screen.fill((153, 0, 48))
                scoreDisplay = self.font.render((f"Score: {self.score}"), True, (255, 255, 255))
                self.screen.blit(scoreDisplay, (0, 0))
                # Check for supermode
                if self.score % 10 == 0 and self.score not in self.scores and self.score != 0:
                    self.superMode = True
                    self.boke.isAlive = False
                    self.boke.x, self.boke.y = 999, 999
                    self.boke.displayChar()
                # Move and display characters
                self.player.move(playerMovement)
                self.player.displayChar()
                for enemy in self.enemyList:
                    if enemy.isAlive:
                        enemy.move(enemyMovement)
                        enemy.displayChar()
                if self.superMode:
                    self.player.spriteColour = (255, 255, 0)
                else:
                    self.player.spriteColour = (0, 255, 0)
                    self.boke.spawnCollectible()
                # Check for collisions
                if self.player.checkCollision(self.boke.charRect):
                    self.boke.isAlive = False
                    collectSound.play()
                    self.score += 1
                if self.player.checkCollision(self.enemy1.charRect) or self.player.checkCollision(self.enemy2.charRect) or self.player.checkCollision(self.enemy3.charRect):
                    if self.superMode:
                        for i in self.enemyList:
                            if self.player.checkCollision(i.charRect):
                                i.killEnemy()
                                killSound.play()
                        self.scores.append(self.score)
                    else:
                        deathSound.play()
                        self.endScreen("You Lose", (255, 0, 0), (275, 200))
                    self.superMode = False
                # If all enemies dead, display win screen
                if all(not i.isAlive for i in self.enemyList):
                    self.isBoss = True
                    self.finalBoss()
                    self.endScreen("You Win!", (0, 255, 0), (300, 200))
                self.checkQuit()
                pygame.display.update()
                time.sleep(0.0025)
            except:
                break

class Character:
    def __init__(self, x, y, spriteColour: tuple, size):
        self.x, self.y = x, y
        self.size = size
        self.spriteColour = spriteColour

    def displayChar(self):
        self.charRect = pygame.Rect((self.x, self.y, self.size, self.size))
        pygame.draw.rect(game.screen, self.spriteColour, self.charRect)

    def checkBoundaries(self):
        if self.x <= 0:
            self.x = 0
        if self.x >= 784:
            self.x = 784
        if self.y <= 0:
            self.y = 0
        if self.y >= 584:
            self.y = 584

    def checkCollision(self, target):
        return self.charRect.colliderect(target)

class Enemy(Character):
    def __init__(self, x, y, spriteColour: tuple, size, charType, isAlive=True):
        super().__init__(x, y, spriteColour, size)
        self.charType = charType
        self.isAlive = isAlive

    def move(self, enemyMovement):
        # Run to corners
        if game.superMode or game.isBoss:
            self.x += enemyMovement[self.charType][0]
            self.y += enemyMovement[self.charType][1]

        else:
            # Follow player
            if self.charType == 1:
                self.x += (game.player.x - self.x)/100
                self.y += (game.player.y - self.y)/100
            elif self.charType == 2:
                self.x += (game.player.x - self.x)/500
                self.y += (game.player.y - self.y)/500
            elif self.charType == 3:
                # Random movement
                if randint(0, 1):
                    if game.player.x >= self.x:
                        self.x += 1
                    if game.player.x <= self.x:
                        self.x -= 1
                else:
                    if game.player.y >= self.y:
                        self.y += 1
                    if game.player.y <= self.y:
                        self.y -=1
        self.checkBoundaries()

    def killEnemy(self):
        # Spawn enemy outside of screen when killed
        self.isAlive = False
        self.x, self.y = 999, 999
        self.displayChar()

class Boss(Character):
    def __init__(self, x, y, spriteColour: tuple, size):
        super().__init__(x, y, spriteColour, size)
        self.isAlive = True

    def move(self):
        self.x += (game.player.x - self.x)/75
        self.y += (game.player.y - self.y)/75
        self.checkBoundaries()

    def killBoss(self):
        self.isAlive = False
        self.x, self.y = 999, 999
        self.displayChar()

class Player(Character):
    def __init__(self, x, y, spriteColour: tuple, size):
        super().__init__(x, y, spriteColour, size)

    def move(self, playerMovement):
        key = pygame.key.get_pressed()
        # Speed multiplier for supermode
        speedMultiplier = 2 if game.superMode else 1
        for keyType in playerMovement:
            if key[keyType]:
                self.x += speedMultiplier * playerMovement[keyType][0]
                self.y += speedMultiplier * playerMovement[keyType][1]
        self.checkBoundaries()

class Collectible(Character):
    def __init__(self, x, y, spriteColour: tuple, size, isAlive=False):
        super().__init__(x, y, spriteColour, size)
        self.isAlive = isAlive

    def spawnCollectible(self):
        # Spawn collectible if not already spawned
        if not self.isAlive:
            self.x, self.y = randint(0, 784), randint(0, 584)
            self.isAlive = True
        if self.isAlive:
            self.displayChar()

def timeConvert(sec, checker):
    # Convert seconds to minutes and seconds
    mins, sec = divmod(sec, 60)
    if checker == "fullTime":
        return f"{int(mins)}:{int(sec)}"
    if mins % 15 == 0 and mins != 0:
        return True

if __name__ == "__main__":
    game = Game()
    game.gameLoop()
    print("Game Over!")
