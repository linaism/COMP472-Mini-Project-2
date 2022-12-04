import copy
import numpy as np
import time


class Game:
    def __init__(self, game):
        self.game = game
        self.fuel = self.get_fuel()
        self.board = self.get_board()
        self.cars = self.get_cars()

    # Get cars fuels given initial string input
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

    # Get the board configuration given initial string input
    def get_board(self):
        puzzle_split = self.game.split()
        p = puzzle_split[0]
        A = np.array(list(p))
        return np.reshape(A, (-1, 6))

    # Gets cars configuration of the board state at the beginning
    def get_cars(self):
        cars = {}
        for i in range(6):  # iterate over each row
            for j in range(6):  # iterate over each column
                if self.board[i, j].isalpha():  # B # I
                    current_car = self.board[i, j]
                    # If car is horizontal
                    if j < 5 and self.board[i, j + 1] == current_car:
                        pos = j + 1  # pos = 1
                        while pos < 6 and self.board[i, pos] == current_car:
                            pos += 1  # pos = 2
                        if current_car not in cars:
                            length = pos - j
                            cars[current_car] = {"position": [i, j], "length": length, "orientation": 'h',
                                                 "fuel": self.fuel[current_car]}
                    # If car is vertical
                    elif i < 5 and self.board[i + 1, j] == current_car:
                        pos = i + 1  # pos = 1
                        while pos < 6 and self.board[pos, j] == current_car:
                            pos += 1  # pos = 2, pos = 3
                        if current_car not in cars:
                            length = pos - i
                            cars[current_car] = {"position": [i, j], "length": length, "orientation": 'v',
                                                 "fuel": self.fuel[current_car]}
        return cars

    def get_solution(self, node, i):
        filename = "ucf-sol-" + str(i) + ".txt"
        f = open(filename, "w")
        f.write("Initial board configuration: ")
        f.write(self.game)
        
        write_solution(node)

    # Start the game
    def play(self):
        # Search algorithm
        state = {"board": self.board, "cars": self.cars, "move": []}
        node = {"state": state, "parent": {}, "cost": 0}
        print(self.board)
        print(self.cars)

        start = time.time()
        final_node = uniform_cost_search(node)
        end = time.time()
        print(F'Evaluation time: {round(end - start, 7)}s')

        f = open("ucf-sol.txt", "w")
        get_solution(final_node)


def is_goal_state(board):
    return board[2, 5] == 'A'


# UCS Search
def uniform_cost_search(head_node):
    closed_list = []
    open_queue = []

    closed_list.append(head_node)
    open_queue.append(head_node)

    while open_queue:
        node = open_queue.pop(0)
        # print(node)
        if is_goal_state(node["state"]["board"]):
            print("Solution found")
            return node
        children_states = get_children(node)

        for child_state in children_states:
            if closed_list:
                is_in_closed = False
                for visited_node in closed_list:
                    if (visited_node["state"]["board"] == child_state["board"]).all():
                        is_in_closed = True
                if not is_in_closed:
                    child_node = {"state": child_state, "parent": node, "cost": node["cost"] + 1}
                    closed_list.append(child_node)
                    open_queue.append(child_node)
            else:
                print("No solution found")
                return node
    print("No solution found")





def write_solution(node):
    if not node:
        f = open("ucf-sol.txt", "a")
        f.write("No solution found.")
        f.close()
        return

    if not node["state"]["move"]:
        return
    get_solution(node["parent"])
    print(node["state"]["board"])
    f = open("ucf-sol.txt", "a")
    move = node["state"]["move"][0] + " " + node["state"]["move"][1] + " " + str(node["state"]["move"][2])
    f.write(move + ", ")
    f.close()

def get_children(node):
    state = node["state"]
    board = state["board"]
    cars = state["cars"]

    children = []
    for car, params in cars.items():
        # get position of first car
        i = params["position"][0]
        j = params["position"][1]
        fuel = params["fuel"]
        # Horizontal cars
        if params["orientation"] == 'h':
            n = j - 1
            # Check the left side
            while n >= 0 and board[i, n] == '.' and params["fuel"] > 0:
                move = [car, "left", j - n]
                params["position"][1] -= 1
                params["fuel"] -= 1
                new_board = get_board(cars)
                state = {"board": new_board, "cars": copy.deepcopy(cars), "move": move}
                children.append(state)
                n -= 1
            params["fuel"] = fuel
            params["position"][1] = j
            # Check the right side
            j_end = j + params["length"] - 1
            n = j_end + 1
            if i == 2 and j_end == 5 and car != 'A':
                params["fuel"] -= 1
                move = [car, "removed", 0]
                params["position"][1] += 1
                new_cars = copy.deepcopy(cars)
                removed_car = new_cars.pop(car)
                print(removed_car)
                new_board = get_board(new_cars)
                state = {"board": new_board, "cars": new_cars, "move": move}
                children.append(state)
            while n < 6 and board[i, n] == '.' and params["fuel"] > 0:
                if i == 2 and n == 5 and car != 'A':
                    params["fuel"] -= 1
                    move = [car, "right", n - j_end]
                    params["position"][1] += 1
                    new_cars = copy.deepcopy(cars)
                    removed_car = new_cars.pop(car)
                    print(removed_car)
                    new_board = get_board(new_cars)
                    state = {"board": new_board, "cars": new_cars, "move": move}
                    children.append(state)
                else:
                    params["fuel"] -= 1
                    move = [car, "right", n - j_end]
                    params["position"][1] += 1
                    new_board = get_board(cars)
                    state = {"board": new_board, "cars": copy.deepcopy(cars), "move": move}
                    children.append(state)
                n += 1
            params["fuel"] = fuel
            params["position"][1] = j
        # Vertical cars
        elif params["orientation"] == 'v':
            n = i - 1
            # Check the top side
            while n >= 0 and board[n, j] == '.' and params["fuel"] > 0:
                params["fuel"] -= 1
                move = [car, "up", i - n]
                params["position"][0] -= 1
                new_board = get_board(cars)
                state = {"board": new_board, "cars": copy.deepcopy(cars), "move": move}
                children.append(state)
                n -= 1
            params["fuel"] = fuel
            params["position"][0] = i
            i_end = i + params["length"] - 1
            n = i_end + 1
            while n < 6 and board[n, j] == '.' and params["fuel"] > 0:
                params["fuel"] -= 1
                move = [car, "down", n - i_end]
                params["position"][0] += 1
                new_board = get_board(cars)
                state = {"board": new_board, "cars": copy.deepcopy(cars), "move": move}
                children.append(state)
                n += 1
            params["fuel"] = fuel
            params["position"][0] = i
    return children


def get_board(cars):
    board = np.full((6, 6), '.')
    for car, params in cars.items():
        if params["orientation"] == 'h':
            rows = [params["position"][0]] * params["length"]
            cols = list(range(params["position"][1], params["position"][1] + params["length"]))
            board[rows, cols] = car
        elif params["orientation"] == 'v':
            rows = list(range(params["position"][0], params["position"][0] + params["length"]))
            cols = [params["position"][1]] * params["length"]
            board[rows, cols] = car
    return board


def print_board(board):
    print('   0 1 2 3 4 5')
    print('   ------------')
    i = 0
    for row in board:
        i += 1
        print(str(i - 1) + '|', end=' ')
        for c in row:
            print(c, end=' ')
        print()