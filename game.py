import copy
import numpy as np
import time
from queue import PriorityQueue


class Game:
    def __init__(self, game, game_id, algorithm, heuristic):
        self.game = game
        self.fuel = self.get_fuel()
        self.board = self.get_board()
        self.cars = self.get_cars()
        self.states_visited = 0
        self.solution_path = []
        self.search_path = []
        self.game_id = game_id
        self.algorithm = algorithm
        self.heuristic = heuristic

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

    def h1(self, state):
        h_cost = 0
        current_car = state["cars"]["A"]
        current_posi = current_car["position"]
        j = current_posi[1] + current_car["length"] - 1
        board = state["board"]
        for i in range(j, 6):
            if i < 5 and board[2, i] != board[2, i + 1] and board[2, i + 1] != '.':
                h_cost += 1
        return h_cost

    def h2(self, state):
        h_cost = 0
        current_car = state["cars"]["A"]
        current_posi = current_car["position"]
        j = current_posi[1] + current_car["length"]
        board = state["board"]
        for i in range(j, 6):
            if board[2, i] != ".":
                h_cost += 1
        return h_cost

    def h3(self, state):
        constant = 3
        h_cost = 0
        current_car = state["cars"]["A"]
        current_posi = current_car["position"]
        j = current_posi[1] + current_car["length"] - 1
        board = state["board"]
        for i in range(j, 6):
            if i < 5 and board[2, i] != board[2, i + 1] and board[2, i + 1] != '.':
                h_cost += 1
        new_h = h_cost * constant
        return new_h

    def h4(self, state):  # # vertical blocking vehicles
        h_cost = 0
        current_car = state["cars"]["A"]
        current_posi = current_car["position"]
        j = current_posi[1] + current_car["length"]
        board = state["board"]
        for i in range(j, 6):
            if board[2, i] != '.' and state["cars"][board[2, i]]["orientation"] == 'v':
                h_cost += 1
        return h_cost

    def get_heuristic(self, state):
        if self.heuristic == "h1":
            return self.h1(state)
        elif self.heuristic == "h2":
            return self.h2(state)
        elif self.heuristic == "h3":
            return self.h3(state)
        elif self.heuristic == "h4":
            return self.h4(state)
        else:
            return 0

    # UCS Search
    def uniform_cost_search(self, head_node):
        closed_list = []
        open_queue = []

        closed_list.append(head_node)
        open_queue.append(head_node)

        while open_queue:
            node = open_queue.pop(0)
            self.states_visited += 1
            self.search_path.append(node)
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

    # Greedy Best First Search
    def greedy_best_first_search(self, head_node):
        closed_list = []
        open_queue = []

        open_queue.append((0, head_node))
        closed_list.append(head_node)

        while open_queue:
            node_tuple = open_queue.pop(0)
            node = node_tuple[1]
            self.states_visited += 1
            self.search_path.append(node)
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
                        h = self.get_heuristic(child_state)
                        open_queue.append((h, child_node))
                        open_queue.sort(key=lambda x: x[0], reverse=True)
                else:
                    print("No solution found")
                    return node
        print("No solution found")

    # A/A* (when using an admissible heuristic)
    def a_algorithm(self, head_node):
        closed_list = []
        open_queue = []

        open_queue.append((0, head_node))
        closed_list.append(head_node)

        while open_queue:
            node_tuple = open_queue.pop(0)
            node = node_tuple[1]
            self.states_visited += 1
            self.search_path.append(node)
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
                        h = self.get_heuristic(child_state)
                        cost = node["cost"]
                        open_queue.append((h + cost, child_node))
                        open_queue.sort(key=lambda x: x[0], reverse=True)
                else:
                    print("No solution found")
                    return node
        print("No solution found")

    def write_solution(self, node, runtime):
        filename = self.algorithm + "-sol-" + self.heuristic + ".txt"
        f = open(filename, "w")
        f.write("Initial board configuration: ")
        f.write(self.game + "\n\n")
        b = self.game.split()[0]
        for i in range(0, 35, 6):
            f.write(b[i:i + 6] + "\n")
        f.write("\nCar fuel available: ")
        for car, qty in self.fuel.items():
            f.write(car + ": " + str(qty) + ", ")

        self.get_solution(node)
        if self.solution_path:
            f.write("\n\nRuntime: " + str(runtime) + " seconds")
            f.write("\nSearch path length: " + str(self.states_visited))
            f.write("\nSolution path length: " + str(len(self.solution_path)))
            f.write("\nSolution path: ")
            for move in self.solution_path:
                f.write(move[0] + "; ")
            f.write("\n\n")
            for move in self.solution_path:
                f.write(move[0] + "\t\t")
                f.write(move[2] + " ")
                for c in move[1]:
                    f.write(c)
                f.write("\n")
            f.write("\n")
            for i in range(6):
                for j in range(6):
                    f.write(node["state"]["board"][i, j])
                f.write("\n")
        else:
            f.write("\n\nSorry, could not solve the puzzle as specififed.\nError: No solution found.")
            f.write("\n\nRuntime: " + str(runtime) + " seconds")
        f.close()

    def get_solution(self, node):
        if not node:
            return

        if not node["state"]["move"]:
            return
        self.get_solution(node["parent"])

        car = node["state"]["move"][0]
        fuel = node["state"]["cars"][car]["fuel"] if car in node["state"]["cars"] else 0
        move = node["state"]["move"][0] + " " + node["state"]["move"][1] + " " + str(node["state"]["move"][2])

        flattened_board = node["state"]["board"].flatten()
        self.solution_path.append([move, flattened_board, str(fuel)])

    def write_search_path(self):
        # f(n) g(n) h(n) board fuels
        filename = self.algorithm + "-search-" + self.heuristic + ".txt"
        f = open(filename, "w")
        for node in self.search_path:
            h = self.get_heuristic(node["state"])
            cost = node["cost"]
            fn = cost + h
            board = node["state"]["board"]
            f.write(str(fn) + " " + str(cost) + " " + str(h))
            for c in board.flatten():
                f.write(c)
            f.write(" ")
            for car, params in node["state"]["cars"].items():
                if params["fuel"] < 100:
                    f.write(car + str(params["fuel"]) + " ")
            f.write("\n")

    # Start the game
    def play(self):
        # Search algorithm
        state = {"board": self.board, "cars": self.cars, "move": []}
        node = {"state": state, "parent": {}, "cost": 0}
        print(self.board)

        if self.algorithm == "ucs":
            start = time.time()
            final_node = self.uniform_cost_search(node)
            end = time.time()
            self.get_solution(node)
            filename = "output_file.txt"
            f = open(filename, "a")
            f.write(str(self.game_id) + "\t\t\t\t" + "UCS" + "\t\t\t" + "NA" + "\t\t\t")
            f.write(str(len(self.solution_path)) + "\t\t\t\t\t\t" + str(len(self.search_path)) + "\t\t\t\t\t" + str(
                round(end - start, 3)) + "\n")
            f.close()
            # self.write_solution(final_node, round(end - start, 3))
            # self.write_search_path()
        elif self.algorithm == "a":
            start = time.time()
            final_node = self.a_algorithm(node)
            end = time.time()
            self.get_solution(node)
            filename = "output_file.txt"
            f = open(filename, "a")
            f.write(str(self.game_id) + "\t\t\t\t" + "A" + "\t\t\t" + self.heuristic + "\t\t\t")
            f.write(str(len(self.solution_path)) + "\t\t\t\t\t\t" + str(len(self.search_path)) + "\t\t\t\t\t" + str(
                round(end - start, 3)) + "\n")
            f.close()
            # self.write_solution(final_node, round(end - start, 3))
            # self.write_search_path()
        elif self.algorithm == "gbfs":
            start = time.time()
            final_node = self.greedy_best_first_search(node)
            end = time.time()
            self.get_solution(node)
            filename = "output_file.txt"
            f = open(filename, "a")
            f.write(str(self.game_id) + "\t\t\t\t" + "GBFS" + "\t\t\t" + self.heuristic + "\t\t\t")
            f.write(str(len(self.solution_path)) + "\t\t\t\t\t\t" + str(len(self.search_path)) + "\t\t\t\t\t" + str(
                round(end - start, 3)) + "\n")
            f.close()
            # self.write_solution(final_node, round(end - start, 3))
            # self.write_search_path()


def is_goal_state(board):
    return board[2, 5] == 'A'


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
            # Verify if a blocking horizontal car can be removed
            if i == 2 and j_end == 5 and car != 'A':
                params["fuel"] -= 1
                move = [car, "removed", 0]
                params["position"][1] += 1
                new_cars = copy.deepcopy(cars)
                removed_car = new_cars.pop(car)
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
