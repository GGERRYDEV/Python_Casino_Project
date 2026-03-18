import pygame
import time
pygame.mixer.init()
def horse_racing(player_money):
    print("Horse Racing")
    music = pygame.mixer.Sound("src/Sounds/music.mp3")
    horses = pygame.mixer.Sound("src/Sounds/horses.mp3")
    music.play()
    horses.play()
    time.sleep(20)
    horses.stop()
    music.stop()
    return player_money