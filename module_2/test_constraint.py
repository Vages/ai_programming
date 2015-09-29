from unittest import TestCase
from Constraint import Constraint

__author__ = 'eirikvageskar'


class TestConstraint(TestCase):
    def setUp(self):
        self.not_equal_constraint = Constraint(['x', 'y'], 'x != y')
        self.two_numbers_less_than_third_constraint = Constraint(['x', 'y', 'z'], 'x + y < z')

    def test_not_equal_evaluates_to_true_when_two_numbers_are_not_equal(self):
        self.assertTrue(self.not_equal_constraint.evaluate_constraint((2, 1)))

    def test_not_equal_evaluates_to_false_when_two_numbers_are_equal(self):
        self.assertFalse(self.not_equal_constraint.evaluate_constraint((1, 1)))

    def test_three_number_constraint_evaluates_to_true_when_first_two_sum_to_less_than_third(self):
        self.assertTrue(self.two_numbers_less_than_third_constraint.evaluate_constraint((5, 4, 10)))

    def test_three_number_constraint_evaluates_to_false_when_first_two_sum_to_the_same_as_third(self):
        self.assertFalse(self.two_numbers_less_than_third_constraint.evaluate_constraint((5, 5, 10)))