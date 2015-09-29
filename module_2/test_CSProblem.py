from unittest import TestCase
from CSProblem import CSProblem
from Constraint import Constraint

class TestCSProblem(TestCase):
    def setUp(self):
        self.simple_csp = CSProblem()
        self.simple_csp.domains['x'] = set([1, 2, 3, 4, 5])
        self.simple_csp.domains['y'] = set([1, 2, 3, 4, 5])
        self.simple_csp.constraints.append(Constraint(['x', 'y'], 'x > 2*y', ['x', 'y']))

    def test_revise_x_domain(self):
        self.simple_csp.revise(('x', self.simple_csp.constraints[0]))
        self.assertEqual(self.simple_csp.domains['x'], set([3, 4, 5]))

    def test_finding_variable_with_smallest_domain(self):
        self.simple_csp.revise(('x', self.simple_csp.constraints[0]))
        self.assertEqual('x', self.simple_csp._find_variable_with_smallest_domain())

    def test_it_makes_the_right_number_of_successors(self):
        self.simple_csp.revise(('x', self.simple_csp.constraints[0]))
        children = self.simple_csp.generate_successors_from_assumption()
        self.assertEqual(3, len(children))
