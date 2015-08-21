import sys

import BestFirstSearch as Bfs
import Board as B
import pygame
Board = B.Board


class BoardSearchRunner:
    def __init__(self, board_specification):
        self.board_specification = board_specification
        self.board = Board(board_specification)
        self.solution = None

    def run_search(self, mode='best_first'):
        self.solution = Bfs.a_star(self.board_specification[1], self.board_specification[2], self.board.get_neighbours,
                                   Board.distance_between, Board.distance_between, mode=mode)

    def draw_board_and_solution(self, width, height):
        cell_width = int(min(height/self.board.y_size, width/self.board.x_size))
        width, height = self.board.x_size*cell_width, self.board.y_size*cell_width
        WHITE = (0xFF, 0xFF, 0xFF)
        RED = (0xFF, 0, 0)
        BLACK = (0, 0, 0)

        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Search visualization")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------

        while not done:
            # --- Main event loop
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

            # Draw the environment
            for i in range(self.board.y_size):
                for j in range(self.board.x_size):
                    if self.board.get_cell((j, i)) == 1:
                        color = RED
                    else:
                        color = WHITE
                    pygame.draw.rect(screen, color, [j*cell_width, i*cell_width, cell_width, cell_width])

            # Draw dots in open spaces
            for i in range(self.board.y_size):
                for j in range(self.board.x_size):
                    if self.board.get_cell((j, i)) == 0:
                        pygame.draw.circle(screen, BLACK, (int(j*cell_width+cell_width/2), int(i*cell_width+cell_width/2)), int(cell_width/16))

            pointlist = []
            for i in range(len(self.solution)):
                x, y = self.solution[i]
                pointlist.append((x*cell_width+int(cell_width/2), y*cell_width+int(cell_width/2)))

            pygame.draw.lines(screen, RED, False, pointlist, int(cell_width/16))
            pygame.display.flip()

            clock.tick(30)


if __name__ == '__main__':
    f = open(sys.argv[1])
    spec_raw = f.readline().split(';')
    spec_final = []
    for i in range(len(spec_raw)):
        split_data = spec_raw[i].split()
        for j in range(len(split_data)):
            split_data[j] = int(split_data[j])

        spec_final.append(tuple(split_data))

    spec_final = tuple(spec_final)

    bsr = BoardSearchRunner(spec_final)
    try:
        mode = sys.argv[2]
    except IndexError:
        mode = "best_first"
    bsr.run_search(mode)
    bsr.draw_board_and_solution(1280, 800)
