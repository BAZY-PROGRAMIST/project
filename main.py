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
from load import *
def restart():
    global block_group, water_group, camera_group, player_group, player, box_group
    block_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    camera_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    player = Player((300, 300),{'idle':player_idle, 'run':player_run, 'atk':player_atk})
    player_group = pygame.sprite.Group()
    player_group.add(player)



def game_lvl():
    sc.fill('grey')
    block_group.update(0)
    block_group.draw(sc)
    box_group.update(0)
    box_group.draw(sc)
    water_group.update(0)
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
            elif maps[i][j] == '2':
                water = Water(water_image, pos)
                water_group.add(water)
                camera_group.add(water)
            elif maps[i][j] == '3':
                box = Box(box_image, pos)
                box_group.add(box)
                camera_group.add(box)




class Block(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, step):
        self.rect.x += step
        if pygame.sprite.spritecollide(self, player_group, False):
            if abs(self.rect.top - player.rect.bottom) < 50:
                player.rect.bottom = self.rect.top
                player.on_ground = True
            if abs(self.rect.bottom - player.rect.top) < 15:
                player.rect.top = self.rect.bottom + 5
                player.velocity_y = 0
            if (abs(self.rect.left - player.rect.right) < 15
                    and abs(self.rect.centery - player.rect.centery) < 50):
                player.rect.right = self.rect.left
            if (abs(self.rect.right - player.rect.left) < 15
                    and abs(self.rect.centery - player.rect.centery) < 50):
                player.rect.left = self.rect.right


class Box(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, step):
        self.rect.x += step
        if pygame.sprite.spritecollide(self, player_group, False):
            if abs(self.rect.top - player.rect.bottom) < 50:
                player.rect.bottom = self.rect.top

            if abs(self.rect.bottom - player.rect.top) < 15:
                player.rect.top = self.rect.bottom
                player.velocity_y = 0
            if (abs(self.rect.left - player.rect.right) < 15
                    and abs(self.rect.centery - player.rect.centery) < 50):
                player.rect.right = self.rect.left
            if (abs(self.rect.right - player.rect.left) < 15
                    and abs(self.rect.centery - player.rect.centery) < 50):
                player.rect.left = self.rect.right



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
    def __init__(self, pos, image_lists):
        pygame.sprite.Sprite.__init__(self)
        self.image_lists = image_lists
        self.image = self.image_lists['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]+200
        self.speed = 5
        self.velocity_y = 0
        self.on_ground = False
        self.frame = 0
        self.timer_anime = 0
        self.anime_idle = False
        self.anime_run = False
        self.anime_atk = False
        self.key = pygame.key.get_pressed()
        self.dir = 'right'
        self.timer_attack = 0
        self.jump = False
        self.jump_step = -20
        self.flag_damage = False
    def update(self):
        if pygame.sprite.spritecollide(self, block_group, False):
            self.on_ground = True
        else:
            self.on_ground = False
        if not self.on_ground:
            self.rect.y += 1
        self.animation()
        self.move()
        self.atk()
        self.Jump()
        self.key = pygame.key.get_pressed()

    def animation(self):
        self.timer_anime += 2
        if self.timer_anime / FPS > 0.1:
            if self.frame == len(self.current_list_image) - 1:
                self.frame = 0
                if self.anime_atk:
                    self.current_list_image = player_idle
                    self.anime_atk = False
                    self.anime_idle = True
            else:
                self.frame += 1
            self.timer_anime = 0
        if self.anime_idle:
            self.current_list_image = self.image_lists['idle']
        if self.anime_run:
            self.current_list_image = self.image_lists['run']
        if self.anime_atk:
            self.current_list_image = self.image_lists['atk']
        try:
            if self.dir == 'right':
                self.image = self.current_list_image[self.frame]
            else:
                self.image = pygame.transform.flip(self.current_list_image[self.frame], True, False)
        except:
            self.frame = 0
    def move(self):
        if self.key[pygame.K_d]:
            if self.rect.right > 1000:
                self.rect.right = 1000
                camera_group.update(-self.speed)
            self.rect.x += 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif self.key[pygame.K_a]:
            if self.rect.right > 1000:
                self.rect.right = 1000
                camera_group.update(-self.speed)
            self.rect.x -= 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk:
                self.anime_idle = True
            self.anime_run = False


        if pygame.sprite.spritecollide(self, water_group, False):
            self.kill()
    def Jump(self):
        if self.key[pygame.K_w]:
            print('54')
            self.jump = True
        if self.jump:
            if self.jump_step <= 20:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.jump = False
                self.jump_step = -20
    def atk(self):
        if self.key[pygame.K_SPACE] and not self.anime_atk:
            self.frame = 0
            self.anime_atk = True
            self.anime_idle = False
            self.anime_run = False
            self.flag_damage = True





restart()
drawMaps('1.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game_lvl()
    clock.tick(FPS)