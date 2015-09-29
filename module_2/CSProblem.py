from collections import deque, defaultdict
import itertools

class CSProblem:
    def __init__(self):
        self.domains = {}  # A dict of type {var_name: var_domain}
        self.constraints = []  # Contains Constraint instances
        self.queue = deque()

    def revise(self, var_cons_tuple):
        """
        Takes a (var, constraint) tuple. Tries to narrow down the domain of var using constraint.
        :param var_cons_tuple:
        :return:
        """
        focal_variable, constraint = var_cons_tuple

        # Get domains of all variables involved in constraint.
        variables_in_constraint = constraint.variables
        constraint_variable_domains = []
        for v in variables_in_constraint:
            constraint_variable_domains.append(self.domains[v])

        # Make all permutations of the variables
        all_permutations = list(itertools.product(*constraint_variable_domains))

        # Make dict which sorts the permutations by the value of the focal value
        focal_permutation_dict = {}
        focal_variable_domain = self.domains[focal_variable]

        for v in focal_variable_domain:
            focal_permutation_dict[v] = []

        position_of_focal_variable = variables_in_constraint.index(focal_variable)

        for permutation in all_permutations:
            focal_value = permutation[position_of_focal_variable]

            focal_permutation_dict[focal_value].append(permutation)

        values_that_can_satisfy_constraint = []

        for focal_key in focal_permutation_dict:
            if self.can_one_tuple_satisfy_constraint(focal_permutation_dict[focal_key], constraint):
                values_that_can_satisfy_constraint.append(focal_key)

        if len(values_that_can_satisfy_constraint) < len(focal_variable_domain):
            values_that_can_satisfy_constraint.sort()
            self.domains[focal_variable] = values_that_can_satisfy_constraint

    def initialize_queue(self):
        """
        Initializes queue; first formula on page 5 of task.
        :return:
        """
        for constraint in self.constraints:
            for variable in constraint.variables:
                self.queue.append((variable, constraint))

    def can_one_tuple_satisfy_constraint(self, tuple_list, constraint):
        """
        Goes through the tuples in tuple list. If one tuple can satisfy constraint, it returns True. Otherwise False.
        :param tuple_list:
        :param constraint:
        :return:
        """
        for t in tuple_list:
            if constraint.evaluate_constraint(t):
                return True

        return False

    def domain_changed(self, changed_variable):
        """
        Called when domain of a variable has changed. All constraints in which it participates have to be re-evaluated.
        :param changed_variable: Some variable.
        :return:
        """
        for constraint in self.constraints:
            if changed_variable in constraint.variables:
                for var in constraint.variables:
                    if var == changed_variable:
                        continue

                    self.queue.append((var, constraint))

