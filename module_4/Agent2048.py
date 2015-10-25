from module_4.GraphicsModule4 import Gfx
from module_4.PowerBoard import PowerBoard
from module_4.PowerBoardState import PowerBoardState
import pygame
import sys
from time import time

if __name__ == '__main__':
    pb = PowerBoard((4, 4))
    pb.add_random_tile()
    gfx = Gfx(pb, 30, (600, 600))
    a = time()
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        b = time()
        if not game_over:

            empties = len(pb.get_empty_spaces())

            search_state = PowerBoardState(PowerBoardState.get_recursion_depth_roof(empties))
            search_state.board = pb.get_board()
            decision = search_state.decision()
            pb.move_and_add_random_tile(decision)
            c = time()
            print(c-b)
            if pb.is_game_over():
                game_over = True

                print('Game over after', c-a)

            gfx.draw()
