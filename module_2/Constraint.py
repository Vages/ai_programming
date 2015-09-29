__author__ = 'eirikvageskar'


class Constraint:
    def __init__(self, var_names, expression):
        args = var_names[0]
        for i in range(1, len(var_names)):
            args += ', ' + var_names[i]
        self.constraint_formula = eval('lambda ' + args + ': ' + expression)

    def evaluate_constraint(self, args):
        parameters = str(args[0])
        for i in range(1, len(args)):
            parameters += ', ' + str(args[i])

        return eval('self.constraint_formula('+parameters+')')

if __name__ == '__main__':
    neq = Constraint(['x', 'y'], 'x != y')
    print(neq.constraint_formula(0, 1))