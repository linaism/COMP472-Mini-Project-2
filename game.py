from car import Car
from search import Search
from boardstate import BoardState


class Game:
    def __init__(self, game):
        self.game = game
        self.board = self.get_board()
        self.fuel = self.get_fuel()

    def get_fuel(self):
        cars_fuel = {}
        puzzle_split = self.game.split()
        p = puzzle_split[0]
        for f in puzzle_split[1:]:
            cars_fuel[f[0]] = int(f[1])
        for c in p:
            if c.isalpha() and c not in cars_fuel:
                cars_fuel[c] = 100
        return cars_fuel

    def get_board(self):
        puzzle_split = self.game.split()
        p = puzzle_split[0]
        board = []
        for i in range(0, 35, 6):
            board.append(p[i:i + 6])
        return board

    # Gets cars configuration of the board state
    def get_cars(self):
        cars = {}
        for i in range(6):  # iterate over each row
            for j in range(6):  # iterate over each column
                if self.board[i][j].isalpha():  # B # I
                    current_car = self.board[i][j]
                    # If car is horizontal
                    if j < 5 and self.board[i][j + 1] == current_car:
                        pos = j + 1  # pos = 1
                        while pos < 6 and self.board[i][pos] == current_car:
                            pos += 1  # pos = 2
                        if current_car not in cars:
                            length = pos - j
                            cars[current_car] = Car([i, j], length, 'h', self.fuel[current_car])
                    # If car is vertical
                    elif i < 5 and self.board[i + 1][j] == current_car:
                        pos = i + 1  # pos = 1
                        while pos < 6 and self.board[pos][j] == current_car:
                            pos += 1  # pos = 2, pos = 3
                        if current_car not in cars:
                            length = pos - i
                            cars[current_car] = Car([i, j], length, 'v', self.fuel[current_car])

        return cars

    def play(self):
        # Search algorithm
        node = {"state": BoardState(self.get_cars()), "parent": {}, "cost": 0}
        # goal = goal
        search = Search(node, 0)
        ucs = search.uniform_cost_search()
#         B down 1 and H left 1
#         update cars position
#         update rows and cols
#


