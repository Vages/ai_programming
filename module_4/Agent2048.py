from module_4.GraphicsModule4 import Gfx
from module_4.PowerBoard import PowerBoard
from module_4.PowerBoardState import PowerBoardState
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

        empties = len(pb.get_empty_spaces())

        search_state = PowerBoardState(PowerBoardState.get_recursion_depth_roof(empties))
        search_state.board = pb.get_board()
        decision = search_state.decision()
        pb.move_and_add_random_tile(decision)

        gfx.draw()
