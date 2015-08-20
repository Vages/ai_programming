def construct_board(board_specification):
    size_params = board_specification[0]
    x_size = size_params[0]
    y_size = size_params[1]

    board = []

    for i in range(y_size):
        board.append([0]*x_size)

    for j in range(3, len(board_specification)):
        obstacle_spec = board_specification[j]

        x_start = obstacle_spec[0]
        y_start = obstacle_spec[1]
        x_size = obstacle_spec[2]
        y_size = obstacle_spec[3]

        for k in range(y_start, y_start+y_size):
            for l in range(x_start, x_start+x_size):
                board[k][l] = 1

    return board
