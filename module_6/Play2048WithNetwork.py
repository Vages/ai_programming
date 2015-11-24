__author__ = 'eirikvageskar'

import random
import statistics
import time
from math import log
import ai2048demo

import datetime

dt = datetime.datetime

from module_4.PowerBoard import PowerBoard
from PowerBoardAnn import PowerBoardAnn
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

    no_of_epochs = int(sys.argv[1])
    raw_topology = sys.argv[2]
    error_function = sys.argv[3]

    hidden_layer_topology = [int(raw) for raw in raw_topology.split(";")]

    pba = PowerBoardAnn(26, hidden_layer_topology, 4)
    pba.read_pickle()
    error_rates = pba.do_training(no_of_epochs)

    start_time = time.time()

    ann_best_tiles = []
    random_best_tiles = []
    for i in range(50):
        pb = PowerBoard((4, 4))
        pb.add_random_tile()
        while True:
            if pb.is_game_over():
                pb.print_to_console()
                ann_best_tiles.append(max(pb.get_board()))
                break
            network_output = pba.evaluate_one_board(convert_list_to_2d(pb.get_board()))
            possible_directions = pb.get_possible_move_directions()
            for choice in network_output:
                if directions[choice] in possible_directions:
                    pb.move_and_add_random_tile(directions[choice])
                    break

    for i in range(50):
        pb = PowerBoard((4, 4))
        pb.add_random_tile()
        while True:
            if pb.is_game_over():
                pb.print_to_console()
                random_best_tiles.append(max(pb.get_board()))
                break
            possible_directions = pb.get_possible_move_directions()
            pb.move_and_add_random_tile(random.choice(possible_directions))

    print(ann_best_tiles)
    ann_mean = statistics.mean(ann_best_tiles)
    print("Mean best tile for ANN:", ann_mean)
    print(random_best_tiles)
    random_mean = statistics.mean(random_best_tiles)
    print("Mean best tile for random:", random_mean)
    print("Welch test score: ", ai2048demo.welch(random_best_tiles, ann_best_tiles))

    with open("play2048log.txt", "a") as logfile:
        timestamp = dt.fromtimestamp(start_time)
        readable_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        logfile.write("\n\nTest started at " + readable_timestamp)
        logfile.write("\nHidden layer topology: " + str(hidden_layer_topology))
        logfile.write("\nNumber of epochs: " + str(no_of_epochs))
        logfile.write("\nANN best tiles: " + str(ann_best_tiles))
        logfile.write("\nANN average tile: " + str(ann_mean))
        logfile.write("\nRandom best tiles: " + str(random_best_tiles))
        logfile.write("\nRandom average tile: " + str(random_mean))
