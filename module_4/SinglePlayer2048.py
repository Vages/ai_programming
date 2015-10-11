from module_4.GraphicsModule4 import Gfx
from module_4.PowerBoard import PowerBoard
import pygame
import sys

if __name__ == '__main__':
    pb = PowerBoard((4, 4))
    pb.add_random_tile()
    gfx = Gfx(pb, 30, (600, 600))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pb.move_and_add_random_tile('d')
                if event.key == pygame.K_UP:
                    pb.move_and_add_random_tile('u')
                if event.key == pygame.K_RIGHT:
                    pb.move_and_add_random_tile('r')
                if event.key == pygame.K_LEFT:
                    pb.move_and_add_random_tile('l')

        gfx.draw()
