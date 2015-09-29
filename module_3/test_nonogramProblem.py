from unittest import TestCase
from NonogramProblem import NonogramProblem
__author__ = 'eirikvageskar'


class TestNonogramProblem(TestCase):
    def setUp(self):
        self.ten_zero_array = [0]*10

    def test_fill_five_bits_from_position_three(self):
        a = NonogramProblem._fill_k_bits_in_array_from_position_i(self.ten_zero_array, 5, 3)
        self.assertEqual([0, 0, 0, 1, 1, 1, 1, 1, 0, 0], a)

    def test_fill_a_two_piece_in_every_way_from_position_seven(self):
        res = NonogramProblem._place_piece_in_every_possible_way(self.ten_zero_array, 2, 7)

        self.assertEqual([([0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 10),
                          ([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 11)], res)
