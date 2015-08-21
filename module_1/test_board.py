from unittest import TestCase
import module_1.Board
import module_1.BestFirstSearch as Bfs

Board = module_1.Board.Board


class TestBoard(TestCase):
    def setUp(self):
        # The test board from the report
        self.board_spec = (
            (6, 6),
            (1, 0),
            (5, 5),
            (3, 2, 2, 2),
            (0, 3, 1, 3),
            (2, 0, 4, 2),
            (2, 5, 2, 1)
        )

        self.expected_board = [
            [0, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 0, 0]
        ]

        self.board = Board(self.board_spec)

    def test_get_board(self):
        self.assertEqual(self.expected_board, self.board.get_board())

    def test_distance_between(self):
        self.assertEqual(1, round(self.board.distance_between((1, 1), (1, 2))))
        self.assertEqual(1, round(self.board.distance_between((1, 1), (2, 1))))
        self.assertEqual(1.414, round(self.board.distance_between((1, 1), (2, 2)), 3))

    def test_it_finds_the_correct_neighbours_in_bottom_left_corner(self):
        home_cell = (0, 0)

        expected_neighbours = {(1, 0), (1, 1), (0, 1)}

        self.assertEqual(expected_neighbours, self.board.get_neighbours(home_cell))

    def test_it_finds_the_correct_neighbours_in_top_right_corner(self):
        home_cell = (5, 5)

        expected_neighbours = {(4, 5), (4, 4), (5, 4)}

        self.assertEqual(expected_neighbours, self.board.get_neighbours(home_cell))

    def test_it_finds_the_correct_neighbours_close_to_an_obstacle(self):
        home_cell = (2, 2)

        expected_neighbours = {(1, 1), (1, 2), (1, 3), (2, 3)}

        self.assertEqual(expected_neighbours, self.board.get_neighbours(home_cell))

    def test_get_cell(self):
        self.assertEqual(self.expected_board[0][2], self.board.get_cell((2, 0)))
        self.assertEqual(self.expected_board[2][0], self.board.get_cell((0, 2)))

    def test_best_first_search_finds_best_solution(self):
        possible_shortest_paths = {
            ((1, 0), (1, 1), (2, 2), (2, 3), (3, 4), (4, 5), (5, 5)),
            ((1, 0), (1, 1), (2, 2), (2, 3), (3, 4), (4, 4), (5, 5))
        }

        found_path = Bfs.a_star(self.board_spec[1], self.board_spec[2],
                                self.board.get_neighbours, Board.distance_between, Board.distance_between)

        self.assertIn(found_path, possible_shortest_paths)

    def test_best_first_search_does_not_find_impossible_path(self):
        found_path = Bfs.a_star(self.board_spec[1], (2, 0),
                                self.board.get_neighbours, Board.distance_between, Board.distance_between)

        self.assertFalse(found_path)
