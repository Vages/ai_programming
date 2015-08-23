from unittest import TestCase
from module_1.NPuzzle import NPuzzle


class TestNPuzzle(TestCase):
    def setUp(self):
        self.simple_start_state = ((1, 0, 0),
                                   (0, 0, 0),
                                   (0, 0, 0))

        self.simple_goal_state = ((0, 0, 0),
                                  (0, 0, 0),
                                  (0, 0, 1))

        self.advanced_start_state = ((2, 8, 3),
                                     (1, 6, 4),
                                     (7, 0, 5))

        self.advanced_goal_state = ((1, 2, 3),
                                    (8, 0, 4),
                                    (7, 6, 5))

        self.unsolvable_start_state = ((1, 2, 3, 4),
                                      (5, 6, 7, 8),
                                      (9, 10, 11, 12),
                                      (13, 14, 15, 0))

        self.unsolvable_goal_state = ((1, 2, 3, 4),
                                      (5, 6, 7, 8),
                                      (9, 10, 11, 12),
                                      (13, 15, 14, 0))

        self.my_simple_puzzle = NPuzzle(self.simple_goal_state)
        self.my_advanced_puzzle = NPuzzle(self.advanced_goal_state)
        self.my_unsolvable_puzzle = NPuzzle(self.unsolvable_goal_state)

    def test_manhattan_distance(self):
        simple_manhattan_distance = self.my_simple_puzzle.manhattan_distance(self.simple_start_state,
                                                                             self.simple_goal_state)
        self.assertEqual(4, simple_manhattan_distance)
        advanced_manhattan_distance = self.my_advanced_puzzle.manhattan_distance(self.advanced_start_state,
                                                                                 self.advanced_goal_state)
        self.assertEqual(5, advanced_manhattan_distance)

    def test_generates_next_moves_from_center(self):
        original_state = ((1, 2, 3),
                          (8, 0, 4),
                          (7, 6, 5))

        next_state_1 = ((1, 0, 3),
                        (8, 2, 4),
                        (7, 6, 5))

        next_state_2 = ((1, 2, 3),
                        (8, 6, 4),
                        (7, 0, 5))

        next_state_3 = ((1, 2, 3),
                        (0, 8, 4),
                        (7, 6, 5))

        next_state_4 = ((1, 2, 3),
                        (8, 4, 0),
                        (7, 6, 5))

        possible_next_states = set([next_state_1, next_state_2, next_state_3, next_state_4])

        self.assertEqual(self.my_advanced_puzzle.generate_next_states(original_state), possible_next_states)

    def test_generates_next_moves_from_bottom_right_edge(self):
        original_state = ((1, 2, 3),
                          (4, 5, 6),
                          (7, 8, 0))

        next_state_1 = ((1, 2, 3),
                        (4, 5, 6),
                        (7, 0, 8))

        next_state_2 = ((1, 2, 3),
                        (4, 5, 0),
                        (7, 8, 6))

        possible_next_states = set([next_state_1, next_state_2])

        self.assertEqual(self.my_advanced_puzzle.generate_next_states(original_state), possible_next_states)

    def test_generates_next_moves_from_top_left_edge(self):
        original_state = ((0, 2, 3),
                          (4, 5, 6),
                          (7, 8, 1))

        next_state_1 = ((2, 0, 3),
                        (4, 5, 6),
                        (7, 8, 1))

        next_state_2 = ((4, 2, 3),
                        (0, 5, 6),
                        (7, 8, 1))

        possible_next_states = set([next_state_1, next_state_2])

        self.assertEqual(self.my_advanced_puzzle.generate_next_states(original_state), possible_next_states)

    def test_find_position(self):
        found_position = NPuzzle.find_position(self.advanced_goal_state, 6)
        self.assertEqual((1, 2), found_position)

    def test_finds_two_linear_conflicts(self):
        linear_conflict_for_advanced_state = ((2, 1, 3),
                                              (8, 0, 5),
                                              (7, 6, 4))

        self.assertEqual(4, self.my_advanced_puzzle.linear_conflicts(linear_conflict_for_advanced_state))

    def test_finds_unsolvable_board_is_unsolvable(self):
        self.assertFalse(self.my_unsolvable_puzzle.solvable_from_state(self.unsolvable_start_state))

    def test_finds_solvable_board_is_solvable(self):
        self.assertTrue(self.my_advanced_puzzle.solvable_from_state(self.advanced_start_state))
