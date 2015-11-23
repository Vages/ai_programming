import random
import time
from math import log
from tkinter import Tk

__author__ = 'eirikvageskar'
from module_4.PowerBoard import PowerBoard
from PowerBoardAnn import PowerBoardAnn
from Visuals import GameWindow
import sys

def convert_board_to_exponents(board):
    a = []
    for x in board:
        if x == 0:
            a.append(0)
        else:
            a.append(int(log(x, 2)))

    return a

def convert_list_to_2d(board_list):

    return [board_list[:4], board_list[4:8], board_list[8:12], board_list[12:]]

if __name__ == '__main__':
    directions = ('u', 'r', 'd', 'l')
    pb = PowerBoard((4, 4))
    pb.add_random_tile()

    hidden_layer_topology = [20, 20]
    error_function = 'binary_cross'
    pba = PowerBoardAnn(18, hidden_layer_topology, 4)
    pba.read_pickle()
    no_of_epochs = 40
    error_rates = pba.do_training(no_of_epochs)

    #root = Tk()
    #gw = GameWindow(root)

    #gw.update_view(pb.get_board())
    #root.mainloop()

    while True:
        if pb.is_game_over():
            break
        network_output = pba.evaluate_one_board(convert_list_to_2d(pb.get_board()))
        direction = directions[network_output]
        if direction not in pb.get_possible_move_directions():
            direction = random.choice(pb.get_possible_move_directions())
        pb.move_and_add_random_tile(direction)
        pb.print_to_console()
        #gw.update_view(convert_board_to_exponents(pb.get_board()))

    """
    while True:

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
    """