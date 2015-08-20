from unittest import TestCase
import module_1.BoardConstructor as bc

class TestConstructBoard(TestCase):
    def setUp(self):

        # The test board from the foils
        self.board_spec = [
            [6, 6],
            [1, 0],
            [5, 5],
            [3, 2, 2, 2],
            [0, 3, 1, 3],
            [2, 0, 4, 2],
            [2, 5, 2, 1]
        ]

        self.expected_board = [
            [0, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 0, 0]
        ]

        self.board = bc.construct_board(self.board_spec)

    def test_board_has_correct_dimensions(self):
        expected_x_size = self.board_spec[0][0]
        expected_y_size = self.board_spec[0][1]
        actual_x_size = len(self.board[0])
        actual_y_size = len(self.board)

        self.assertEqual(expected_x_size, actual_x_size)
        self.assertEqual(expected_y_size, actual_y_size)

    def test_board_has_correct_obstacles(self):
        self.assertEqual(self.expected_board, self.board)
