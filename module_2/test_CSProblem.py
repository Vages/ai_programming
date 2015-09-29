from unittest import TestCase
from CSProblem import CSProblem
from Constraint import Constraint


class TestCSProblem(TestCase):
    def setUp(self):
        self.simple_csp = CSProblem()
        self.simple_csp.domains['x'] = [1, 2, 3, 4, 5]
        self.simple_csp.domains['y'] = [1, 2, 3, 4, 5]
        self.simple_csp.constraints.append(Constraint(['x', 'y'], 'x > 2*y', ['x', 'y']))

    def test_revise_x_domain(self):
        self.simple_csp.revise(('x', self.simple_csp.constraints[0]))
        self.assertEqual(self.simple_csp.domains['x'], [3, 4, 5])