import copy
import numpy as np
import time
from queue import PriorityQueue


class Game:
    def __init__(self, game, game_id):
        self.game = game
        self.fuel = self.get_fuel()
        self.board = self.get_board()
        self.cars = self.get_cars()
        self.states_visited = 0
        self.solution_path = []
        self.search_path = []
        self.game_id = game_id

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

    def h1(self, state):
        # find ambulance and that becomes the current node
        # for loop to check the next index after the ambulance
        # if it is a car, h_cost +=1
        # if current car == next car, skip
        # if next position is empty, skip
        h_cost = 0
        current_car = state["cars"]["A"]
        current_posi = current_car["position"]
        j = current_posi + current_car["length"] - 1
        board = state["board"]
        for i in range(j, 6):
            if i < 5 and board[2, i] == board[2, i+1] or '.':
                continue
            else:
                h_cost += 1
            return h_cost

    def h2(self, state):
        h_cost = 0
        current_car = state["cars"]["A"]
        current_posi = current_car["position"]
        j = current_posi + current_car["length"] - 1
        board = state["board"]
        for i in range(j, 6):
                if i < 5 and board[2, i] != ".":
                    h_cost += 1
            return h_cost

    def h3(self, state):
        constant = 3
        h_cost = 0
        current_car = state["cars"]["A"]
        current_posi = current_car["position"]
        j = current_posi + current_car["length"] - 1
        board = state["board"]
        for i in range(j, 6):
            if i < 5 and board[2, i] == board[2, i + 1] or '.':
                continue
            else:
                h_cost += 1

            new_h = h_cost * constant
            return new_h

    def h4(self, state): # # vertical blocking vehicles
        h_cost = 0
        current_car = state["cars"]["A"]
        current_posi = current_car["position"]
        i = current_posi + current_car["length"] - 1
        board = state["board"]
        for j in range(i, 6):
            if j < 5 and board[j, i] == board[j + 1, i] or '.':
                continue
            else:
                h_cost += 1
            return h_cost

    # Greedy Best First Search
    def greedy_best_first_search(self, head_node, heuristic):
        closed_list = []
        open_queue = PriorityQueue()

        open_queue.put((0, head_node))
        closed_list.append(head_node)

        while not open_queue.empty():
            node = open_queue.get()
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
                        if heuristic == "h1":
                            open_queue.put((self.h1(child_state), child_node))
                        if heuristic == "h2":
                            open_queue.put((self.h2(child_state), child_node))
                        if heuristic == "h3":
                            open_queue.put((self.h3(child_state), child_node))
                        if heuristic == "h4":
                            open_queue.put((self.h4(child_state), child_node))
                else:
                    print("No solution found")
                    return node
        print("No solution found")

    def write_solution(self, node, algo, i, runtime):
        filename = algo + "-" + i + "-sol-" + str(i) + ".txt"
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

    def write_search_path(self, algo, i):
        # f(n) g(n) h(n) board fuels
        filename = "ucs-search-" + str(i) + ".txt"
        f = open(filename, "w")
        for node in self.search_path:
            cost = node["cost"]
            board = node["state"]["board"]
            f.write(str(cost) + " " + str(cost) + " 0 ")
            for c in board.flatten():
                f.write(c)
            f.write(" ")
            for car, params in node["state"]["cars"].items():
                if params["fuel"] < 100:
                    f.write(car + str(params["fuel"]) + " ")
            f.write("\n")

    def write_to_output_stats(self):
        filename = "output_file.txt"
        f = open(filename, "w")

    # Start the game
    def play(self):
        # Search algorithm
        state = {"board": self.board, "cars": self.cars, "move": []}
        node = {"state": state, "parent": {}, "cost": 0}
        print(self.board)
        print(self.cars)

        # Uniform Cost Search
        # algorithm = "ucs"
        # start = time.time()
        # final_node = self.uniform_cost_search(node)
        # end = time.time()
        # self.get_solution(node)
        # filename = "output_file.txt"
        # f = open(filename, "a")
        # f.write(str(self.game_id) + "\t\t\t\t" + "UCS" + "\t\t\t" + "NA" + "\t\t\t")
        # f.write(str(len(self.solution_path)) + "\t\t\t\t\t\t" + str(len(self.search_path)) + "\t\t\t\t\t" + str(
        #     round(end - start, 3)) + "\n")
        # f.close()
        # self.write_solution(final_node, algorithm, self.game_id, round(end - start, 3))
        # self.write_search_path(self.game_id)

        # TODO: Comment these back in once two other algoithms are implemented.
        #  Changes can be made to include heuristic info if needed.
        #  Make sure output files generates are right then comment out the write to file function calls
        #  and replace with lines to write to output file for 50 inputs
        # # A*
        # algorithm = "a"
        # start = time.time()
        # final_node = self.uniform_cost_search(node)
        # end = time.time()
        # self.write_solution(final_node, algorithm, self.game_id, round(end - start, 3))
        # self.write_search_path(self.game_id)
        #
        # # GBFS
        algorithm = "gbfs"
        start = time.time()
        final_node = self.greedy_best_first_search(node, heuristic="h1")
        end = time.time()
        self.write_solution(final_node, algorithm, self.game_id, round(end - start, 3))
        self.write_search_path(self.game_id)


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
