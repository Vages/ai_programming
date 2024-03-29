from unittest import TestCase
import itertools
from module_4.PowerBoard import PowerBoard


class TestPowerBoard(TestCase):
    def setUp(self):
        self.four_by_one_board = PowerBoard((4, 1))
        self.normal_board = PowerBoard((4, 4))
        self.normal_board.place_value_at_coordinate(2, (1, 1))
        self.normal_board.place_value_at_coordinate(2, (2, 1))
        self.normal_board.place_value_at_coordinate(2, (1, 2))
        self.normal_board.place_value_at_coordinate(4, (2, 2))

    def test_it_generates_board_of_correct_size(self):
        a = self.four_by_one_board.get_board()
        self.assertEqual(len(a), 1)
        self.assertEqual(len(a[0]), 4)
        b = self.normal_board.get_board()
        self.assertEqual(len(b), 4)
        self.assertEqual(len(b[0]), 4)

    def test_it_places_a_piece_correctly(self):
        x = PowerBoard.ABSENCE
        self.four_by_one_board.place_value_at_coordinate(2, (3, 0))
        self.assertEqual(self.four_by_one_board.get_board(), [x, x, x, 2])

    def test_it_slides_the_piece_all_the_way_to_the_wall_on_a_simple_board(self):
        x = PowerBoard.ABSENCE
        self.four_by_one_board.place_value_at_coordinate(2, (3, 0))
        self.four_by_one_board.move_pieces('l')
        self.assertEqual(self.four_by_one_board.get_board(), [[2, x, x, x]])

    def test_it_combines_two_pieces_with_equal_values_to_one_of_double_value_on_a_simple_board(self):
        x = PowerBoard.ABSENCE
        self.four_by_one_board.place_value_at_coordinate(2, (1, 0))
        self.four_by_one_board.place_value_at_coordinate(2, (3, 0))
        self.assertEqual(self.four_by_one_board.get_board(), (x, 2, x, 2))
        self.four_by_one_board.move_pieces('l')
        self.assertEqual(self.four_by_one_board.get_board(), [4, x, x, x])

    def test_it_does_not_combine_two_pieces_with_unequal_values_on_a_simple_board(self):
        x = PowerBoard.ABSENCE
        self.four_by_one_board.place_value_at_coordinate(2, (1, 0))
        self.four_by_one_board.place_value_at_coordinate(4, (3, 0))
        self.assertEqual(self.four_by_one_board.get_board(), [[x, 2, x, 4]])
        self.four_by_one_board.move_pieces('l')
        self.assertEqual(self.four_by_one_board.get_board(), [[2, 4, x, x]])

    def test_it_generates_pieces_on_normal_board_correctly(self):
        x = PowerBoard.ABSENCE
        supposed_normal_board = list(itertools.chain([x, x, x, x],
                                                     [x, 2, 2, x],
                                                     [x, 2, 4, x],
                                                     [x, x, x, x]))
        self.assertEqual(self.normal_board.get_board(), supposed_normal_board)

    def test_it_moves_left_correctly(self):
        x = PowerBoard.ABSENCE
        supposed_slided_board = list(itertools.chain([x, x, x, x],
                                                     [4, x, x, x],
                                                     [2, 4, x, x],
                                                     [x, x, x, x]))
        self.normal_board.move_pieces('l')
        self.assertEqual(self.normal_board.get_board(), supposed_slided_board)

    def test_it_moves_right_correctly(self):
        x = PowerBoard.ABSENCE
        supposed_slided_board = list(itertools.chain([x, x, x, x],
                                                     [x, x, x, 4],
                                                     [x, x, 2, 4],
                                                     [x, x, x, x]))
        self.normal_board.move_pieces('r')
        self.assertEqual(self.normal_board.get_board(), supposed_slided_board)

    def test_it_moves_up_correctly(self):
        x = PowerBoard.ABSENCE
        supposed_slided_board = list(itertools.chain([x, 4, 2, x],
                                                     [x, x, 4, x],
                                                     [x, x, x, x],
                                                     [x, x, x, x]))
        self.normal_board.move_pieces('u')
        self.assertEqual(self.normal_board.get_board(), supposed_slided_board)

    def test_it_moves_down_correctly(self):
        x = PowerBoard.ABSENCE
        supposed_slided_board = list(itertools.chain([x, x, x, x],
                                                     [x, x, x, x],
                                                     [x, x, 2, x],
                                                     [x, 4, 4, x]))
        self.normal_board.move_pieces('d')
        self.assertEqual(self.normal_board.get_board(), supposed_slided_board)

    def test_it_calculates_score_correctly(self):
        score_before = self.normal_board.points
        self.normal_board.move_pieces('l')
        score_after = self.normal_board.points
        self.assertEqual(score_before+4, score_after, 'Four more points after two 2s are combined')

    def test_it_places_a_random_tile_when_told_to(self):
        a = self.normal_board.get_empty_spaces()
        self.normal_board.add_random_tile()
        b = self.normal_board.get_empty_spaces()
        self.assertEqual(len(b)+1, len(a), "One less empty tile")

    def test_it_gets_the_right_tile_evaluation_sequence_for_each_direction(self):
        u = self.normal_board.get_tile_evaluation_sequence('u')
        d = self.normal_board.get_tile_evaluation_sequence('d')
        l = self.normal_board.get_tile_evaluation_sequence('l')
        r = self.normal_board.get_tile_evaluation_sequence('r')

        expected_u = {((0, 0), (0, 1), (0, 2), (0, 3)),
                      ((1, 0), (1, 1), (1, 2), (1, 3)),
                      ((2, 0), (2, 1), (2, 2), (2, 3)),
                      ((3, 0), (3, 1), (3, 2), (3, 3))}

        expected_d = {((0, 3), (0, 2), (0, 1), (0, 0)),
                      ((1, 3), (1, 2), (1, 1), (1, 0)),
                      ((2, 3), (2, 2), (2, 1), (2, 0)),
                      ((3, 3), (3, 2), (3, 1), (3, 0))}

        expected_l = {((0, 0), (1, 0), (2, 0), (3, 0)),
                      ((0, 1), (1, 1), (2, 1), (3, 1)),
                      ((0, 2), (1, 2), (2, 2), (3, 2)),
                      ((0, 3), (1, 3), (2, 3), (3, 3))}

        expected_r = {((3, 0), (2, 0), (1, 0), (0, 0)),
                      ((3, 1), (2, 1), (1, 1), (0, 1)),
                      ((3, 2), (2, 2), (1, 2), (0, 2)),
                      ((3, 3), (2, 3), (1, 3), (0, 3))}

        self.assertEqual(u, expected_u, "right sequence for up")
        self.assertEqual(d, expected_d, "right sequence for down")
        self.assertEqual(l, expected_l, "right sequence for left")
        self.assertEqual(r, expected_r, "right sequence for right")
