__author__ = 'eirikvageskar'


class Constraint:
    """
    Class containing a constraint for use in a constraint satisfaction problem.
    """

    def __init__(self, func_var_names, expression, actual_var_names=None):
        """
        Creates a constraint that can be used in a constraint satisfaction problem.

        :param func_var_names: The names of all variables that appear in the expression. The same as would appear
        before the colon in a lambda expression.
        :param expression: Expression that will be evaluated. The same as would appear after the colon
        in a lambda expression.
        :param actual_var_names: Names of actual variables that take part in the constraint satisfaction problem.
        :return:
        """

        if actual_var_names is None:
            actual_var_names = func_var_names

        # Create a string of the variables for use in a lambda expression
        args = func_var_names[0]

        for i in range(1, len(func_var_names)):
            args += ', ' + func_var_names[i]

        # Assign anonymous function as a field variable
        self.constraint_formula = eval('lambda ' + args + ': ' + expression)

        self.variables = tuple(actual_var_names)

    def evaluate_constraint(self, args):
        """
        Evaluates the constraint using the arguments stored in args. Must be a tuple or some other ordered iterable.
        :param args: A tuple containing the arguments
        :return:
        """

        return self.constraint_formula(*args)
