__author__ = 'eirikvageskar'


class Constraint:
    def __init__(self, func_var_names, expression, actual_var_names=None):
        if actual_var_names is None:
            actual_var_names = func_var_names

        args = func_var_names[0]

        for i in range(1, len(func_var_names)):
            args += ', ' + func_var_names[i]

        self.constraint_formula = eval('lambda ' + args + ': ' + expression)

        self.variables = tuple(actual_var_names)

    def evaluate_constraint(self, args):
        parameters = str(args[0])
        for i in range(1, len(args)):
            parameters += ', ' + str(args[i])

        return eval('self.constraint_formula('+parameters+')')

if __name__ == '__main__':
    neq = Constraint(['x', 'y'], 'x != y')
    print(neq.constraint_formula(0, 1))