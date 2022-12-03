import numpy as np


class BoardState:
    def __init__(self, cars):
        self.cars = cars

    def get_board(self):
        board = np.full((6, 6), '.')
        for car, params in self.cars.items():
            if params.orientation == 'h':
                rows = [params.position[0]] * params.length
                cols = list(range(params.position[1], params.position[1] + params.length))
                board[rows, cols] = car
            elif params.orientation == 'v':
                rows = list(range(params.position[0], params.position[0] + params.length))
                cols = [params.position[1]] * params.length
                board[rows, cols] = car
        return board

    def get_children(self):
        children = []
        board = self.get_board()
        for car, params in self.cars.items():
            # get position of first car
            i = params.position[0]
            j = params.position[1]
            fuel = params.fuel
            # Horizontal cars
            if params.orientation == 'h':
                n = j - 1
                # Check the left side
                while n >= 0 and board[i, n] == '.' and fuel > 0:
                    child = [car, "left", j-n]
                    children.append(child)
                    n -= 1
                    fuel -= 1
                # Check the right side
                j += params.length - 1
                n = j + 1
                while n < 6 and board[i, n] == '.' and fuel > 0:
                    child = [car, "right", n-j]
                    children.append(child)
                    n += 1
                    fuel -= 1
            # Vertical cars
            elif params.orientation == 'v':
                n = i - 1
                # Check the top side
                while n >= 0 and board[n, j] == '.' and fuel > 0:
                    child = [car, "up", i-n]
                    children.append(child)
                    n -= 1
                    fuel -= 1
                i += params.length - 1
                n = i + 1
                while n < 6 and board[n, j] == '.' and fuel > 0:
                    child = [car, "down", n-i]
                    children.append(child)
                    n += 1
                    fuel -= 1
        return np.array(children)
