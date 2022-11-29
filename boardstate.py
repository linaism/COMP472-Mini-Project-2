import numpy as np


class BoardState:
    def __init__(self, cars):
        self.cars = cars
        self.board = self.get_board()

    def get_board(self):
        board = np.full((6, 6), '.')
        for cars, params in self.cars.items():
            board[params.rows, params.cols] = cars
        return board

    def get_children(self):
        children = []
        for car, params in self.cars.items():
            i = params.position[0]
            j = params.position[1]

            # check left of horizontal cars
            if params.orientation == 'h':
                if j - 1 >= 0 and board[i][j - 1] == '.':
                    # Add state
                    child = cars.copy()
                    child[car].position = [i, j - 1]
                    child[car].fuel -= 1

                # check right side of horizontal cars
                j += child[car].length - 1

                if j + 1 < 6 and board[i][j + 1] == '.':
                # handle this case
                i += params.length - 1
            elif params.orientation == 'v':
                if i - 1 >= 0 and board[i - 1][j] == '.':
                # handle this case
                if i + 1 < 6 and board[i - 1][j] == '.':
