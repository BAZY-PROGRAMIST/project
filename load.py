import pygame
from script import load_image
block_image = pygame.image.load('image/block/block.jpg').convert_alpha()
water_image = pygame.image.load('image/block/water.jpg').convert_alpha()
player_idle = load_image('image/player/idle')
player_run = load_image('image/player/run')
player_atk = load_image('image/player/attack')
box_image = pygame.image.load('image/block/box.png').convert_alpha()