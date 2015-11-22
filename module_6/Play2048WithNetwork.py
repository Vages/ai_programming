import time
from math import log

__author__ = 'eirikvageskar'
from module_4.PowerBoard import PowerBoard
from PowerBoardAnn import PowerBoardAnn
from Visuals import GameWindow
import sys

if __name__ == '__main__':
    pb = PowerBoard((4, 4))
    pb.add_random_tile()

    """
    hidden_layer_topology = [50, 40, 30, 20]
    error_function = 'binary_cross'

    pba = PowerBoardAnn(17, hidden_layer_topology, 4, preprocessing_method=flatten_lists_and_normalize)
    pba.read_pickle()
    error_rates = pba.do_training(no_of_epochs)
    """

    gw = GameWindow()

    a = []
    for x in pb.get_board():
        if x == 0:
            a.append(0)
        else:
            a.append(int(log(x)))

    gw.update_view(a)

    while True:
        gw.update_view(a)
        time.sleep(1000)

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