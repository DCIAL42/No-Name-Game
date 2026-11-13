import pygame

from game import Game

pygame.init()

pygame.mixer.music.load("Boke, The Soundtrack.mp3")
pygame.mixer.music.play(-1)

deathSound = pygame.mixer.Sound("End.mp3")
collectSound = pygame.mixer.Sound("Collect.mp3")
killSound = pygame.mixer.Sound("Enemy.mp3")
deathSound.set_volume(0.5)
collectSound.set_volume(0.5)
killSound.set_volume(0.5)

if __name__ == "__main__":
    game = Game()
    game.gameLoop()
    print("Game Over!")
