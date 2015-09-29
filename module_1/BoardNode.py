

class BoardNode:
    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y

    def get_successors(self):
        return self.board.get_neighbours((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
