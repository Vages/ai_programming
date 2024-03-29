from collections import deque
from copy import deepcopy
from module_2.Constraint import Constraint
import itertools

class CSProblem:
    """
    Class containing a bare bones constraint satisfaction problem.
    """

    def __init__(self):
        self.domains = {}  # A dict of type {var_name: var_domain_as_a_set}
        self.constraints = []  # Contains Constraint instances
        self.queue = deque()  # Queue for revise algorithm. Tuples of type (var_name, constraint).

    def add_constraint(self, func_var_names, expression, actual_variables):
        """
        Passes the arguments on to the Constraint constructor and appends the generated constraint to this instance’s
        constraints list.
        """
        self.constraints.append(Constraint(func_var_names, expression, actual_variables))

    def create_constraint_from_text(self, text):
        """
        Takes a text string and converts it to a constraint. Format: "x y; x==y; 0 1".
        """
        lambda_list, expression, actual_variables = text.split(';')
        lambda_list = lambda_list.split()
        actual_variables = actual_variables.split()

        self.add_constraint(lambda_list, expression, actual_variables)

    def initialize_queue_and_filter(self):
        self.initialize_queue()
        self.domain_filtering()

    def _domains_as_tuples(self):
        """
        Returns a tuple of (key, values) tuples, in order for the object to be hashable.
        """
        keys = list(self.domains.keys())
        keys.sort()
        key_item_tuples = []

        for key in keys:
            domain_items = list(self.domains[key])
            domain_items.sort()
            item_tuple = tuple(domain_items)
            key_item_tuple = (key, item_tuple)
            key_item_tuples.append(key_item_tuple)

        return tuple(key_item_tuples)

    def __eq__(self, other):
        return self.domains == other.domains  # This should work as long as dictionary equality works right.

    def __lt__(self, other):
        return self.domain_sizes_minus_one(self) < self.domain_sizes_minus_one(other)

    def __hash__(self):
        return hash(self._domains_as_tuples())

    def revise(self, var_cons_tuple):
        """
        Takes a (var, constraint) tuple. Tries to narrow down the domain of var using constraint.
        :param var_cons_tuple: Tuple of form (variable_name, constraint)
        """
        focal_variable, constraint = var_cons_tuple

        # Get domains of all variables involved in constraint.
        variables_in_constraint = constraint.variables
        constraint_variable_domains = []
        for v in variables_in_constraint:
            constraint_variable_domains.append(self.domains[v])

        # Make all permutations of the variables
        all_permutations = list(itertools.product(*constraint_variable_domains))

        # Make dict which splits the permutations by the value of the focal value
        focal_permutation_dict = {}
        focal_variable_domain = self.domains[focal_variable]

        for v in focal_variable_domain:
            focal_permutation_dict[v] = []

        position_of_focal_variable = variables_in_constraint.index(focal_variable)

        for permutation in all_permutations:
            focal_value = permutation[position_of_focal_variable]

            focal_permutation_dict[focal_value].append(permutation)

        # Will contain only the values of x’s domain which satisfy the constraint
        values_that_can_satisfy_constraint = set()

        for focal_key in focal_permutation_dict:
            if self._can_one_tuple_satisfy_constraint(focal_permutation_dict[focal_key], constraint):
                values_that_can_satisfy_constraint.add(focal_key)

        # Check if domain has been reduced
        if len(values_that_can_satisfy_constraint) < len(focal_variable_domain):
            self.domains[focal_variable] = values_that_can_satisfy_constraint
            return True  # True signalizes that the domain was changed

        return False  # False signalizes that the domain is unchanged

    @staticmethod
    def _can_one_tuple_satisfy_constraint(tuple_list, constraint):
        """
        Goes through the tuples in tuple list. If one tuple can satisfy constraint, it returns True. Otherwise False.
        """
        for t in tuple_list:
            if constraint.evaluate_constraint(t):
                return True

        return False

    def initialize_queue(self):
        """
        Initializes queue. First formula on page 5 of task.
        :return:
        """
        for constraint in self.constraints:
            for variable in constraint.variables:
                self.queue.append((variable, constraint))

    def domain_filtering(self):
        """
        Runs the domain filtering loop. Second formula on page 5 of task.
        :return:
        """
        while self.queue:
            todo_revise_tuple = self.queue.popleft()
            if self.revise(todo_revise_tuple):
                focal_variable, constraint = todo_revise_tuple
                self._domain_changed(focal_variable)

    def rerun(self, focal_variable):
        """
        Run when a focal variable has been given an assumed value. Third formula on page 5 of task.
        """
        self._domain_changed(focal_variable)
        self.domain_filtering()

    def _domain_changed(self, changed_variable):
        """
        Called when domain of a variable has changed. All constraints in which it participates have to be re-evaluated.
        :param changed_variable: Some variable.
        """
        for constraint in self.constraints:
            if changed_variable in constraint.variables:
                for var in constraint.variables:
                    if var == changed_variable:
                        continue

                    self.queue.append((var, constraint))

    @staticmethod
    def domain_sizes_minus_one(problem):
        """
        A simple heuristic function: Estimates the distance from the goal is the sum of each variable’s domain size,
        minus one for each domain (because one option needs to be left in order to have a solution).
        See top of page 7 in the task for details.
        """
        domains = problem.domains

        domain_size_sum = 0

        for v in domains:
            t = len(domains[v])
            if t == 0:
                return float('inf')  # Return infinity if any domain has size 0, because it can never yield a solution
            domain_size_sum += len(domains[v])

        domain_size_sum -= len(domains)

        return domain_size_sum

    @staticmethod
    def all_domains_have_size_one(problem):
        """
        Tells if all domains have size one, which means the problem is solved.
        """
        domains = problem.domains

        for v in domains:
            if len(domains[v]) != 1:
                return False

        return True

    def get_successors(self):
        """
        Picks a variable with the smallest number of remaining values left in its domain.
        It then makes one copy of itself, one for each possible value of the domain.
        It will return a list containing one possible version of the CSP, each assuming one of possible values of
        the variable’s domain to be true.
        """
        variable_with_smallest_domain = self._find_variable_with_smallest_domain()

        successors = []

        for value in self.domains[variable_with_smallest_domain]:
            new_successor = deepcopy(self)
            new_successor.domains[variable_with_smallest_domain] = set([value])
            new_successor.rerun(variable_with_smallest_domain)
            successors.append(new_successor)

        return successors

    def _find_all_variables_with_domains_without_size_1(self):
        """
        Helper method in order to avoid selecting domains of size 1 for successor generation.
        This made the algorithm halt prematurely.
        """
        candidates = []
        for k in self.domains:
            if len(self.domains[k]) != 1:
                candidates.append(k)

        return candidates

    def _find_variable_with_smallest_domain(self):
        """
        Helper method used in generating successors.
        """
        return min(self._find_all_variables_with_domains_without_size_1(), key=lambda x: len(self.domains[x]))
