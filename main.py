import pygame
import os
import sys
import random
pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
lvl = 'game'

from load import *
def restart():
    global block_group, water_group, camera_group, player_group
    block_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    camera_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = Player(player_image, (300, 300))
    player_group.add(player)


def game_lvl():
    sc.fill('grey')
    block_group.update()
    block_group.draw(sc)
    water_group.update()
    water_group.draw(sc)
    player_group.update()
    player_group.draw(sc)
    pygame.display.update()


def drawMaps(nameFile):
    maps = []
    source = 'game_lvl/' + str(nameFile)
    with open(source, 'r') as file:
        for i in range(0, 10):
            maps.append(file.readline().replace("\n", "").split(",")[0:-1])
    pos = [0, 0]
    for i in range(0, len(maps)):
        pos[1] = i * 80
        for j in range(0, len(maps[0])):
            pos[0] = j * 80
            if maps[i][j] == '1':
                block = Block(block_image, pos)
                block_group.add(block)
                camera_group.add(block)
            elif maps[i][j] == '1':
                water = Water(water_image, pos)
                water_group.add(water)
                camera_group.add(water)


class Block(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, step):
        self.rect.x += step
class Water(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self, step):
        self.rect.x += step

class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 5
        self.velocity_y = 0
        self.on_ground = True
        self.frame = 0
        self.timer_anime = 0
        self.anime = False
        self.key = pygame.key.get_pressed()
        self.dir = 'right'
        self.timer_attack = 0
    def update(self):
        self.move()
        self.jump()
        self.key = pygame.key.get_pressed()
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.rect.x += self.speed
            self.image = player_image[self.frame]
            self.anime = True
            if self.rect.right > 1000:
                self.rect.right = 1000
                camera_group.update(-self.speed)

        elif key[pygame.K_a]:
            self.rect.x -= self.speed
            self.image = pygame.transform.flip(player_image[self.frame], True, False)
            if self.rect.left > 1000:
                self.rect.left = 1000
                camera_group.update(-self.speed)
            self.anime = True
        else:
            self.anime = False
    def jump(self):
        if self.key[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -25
            self.on_ground = False
        self.rect.y += self.velocity_y
        self.velocity_y += 1
        if self.velocity_y > 10:
            self.velocity_y = 10




restart()
drawMaps('1(2).txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if lvl == 'game':
        game_lvl()
    clock.tick(FPS)