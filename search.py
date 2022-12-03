import numpy as np
from boardstate import BoardState
import copy

from queue import PriorityQueue

from boardstate import BoardState


def translate_move_to_state(move, board_state):
    # Translate move into state
    car_id = move[0]
    direction = move[1]
    quantity = int(move[2])
    new_cars = copy.deepcopy(board_state.cars)
    new_state = BoardState(new_cars)
    parent_pos = board_state.cars[car_id].position
    if direction == "left":
        new_state.cars[car_id].position[1] = parent_pos[1] - quantity
    elif direction == "right":
        new_state.cars[car_id].position[1] = parent_pos[1] + quantity
    elif direction == "up":
        new_state.cars[car_id].position[0] = parent_pos[0] - quantity
    else: #down
        print("translate move down")
        print(parent_pos)
        print(quantity)
        new_state.cars[car_id].position[0] = parent_pos[0] + quantity
    new_state.cars[car_id].fuel -= quantity
    return new_state


def is_goal_state(state):
    board = state.get_board()
    after_A = state.cars["A"].position[1] + state.cars["A"].length
    goal = True
    while after_A <= 5:
        if board[2, after_A] != '.':
            goal = False
            break
        after_A += 1
    return goal

class Search:
    def __init__(self, head_node, heuristic):
        self.head_node = head_node
        self.heuristic = heuristic

    def h1(self):
        # find ambulance and that becomes the current node
        # for loop to check the next index after the ambulance
        # if it is a car, h_cost +=1
        # if current car == next car, skip
        # if next position is empty, skip
        h_cost = 0
        current = self.head_node.cars["A"].length
        for row in np.board[2]:
            if current + 1 == current or '.':
                continue
            else:
                h_cost += 1
            return self.heuristic.append(h_cost)

    def h2(self):
        x = 5
        h_cost = 0
        while x > 0 :
            cell = np.board[2][x]
            if cell == "A" :
                x = 0
                break
            else :
                if cell != "." :
                    h_cost += 1
                    x -= 1
            return self.heuristic.append(h_cost)

    def h3(self):
        constant = 3
        for i in self.heuristic:
            new_h = self.heuristic * constant
            return self.heuristic.append(new_h)

    # def h4(self):

    def uniform_cost_search(self):
        closed_list = []
        open_queue = []
        # open_queue = PriorityQueue()
        # open_queue.put(cost+heuristic(state), node)

        closed_list.append(self.head_node)
        open_queue.append(self.head_node)

        while open_queue:
            node = open_queue.pop(0)
            print("Open queue")
            print(node["state"].get_board())
            print(node["cost"])
            children_moves = node["state"].get_children()
            children_states = []
            # Check each move
            for move in children_moves:
                new_state = translate_move_to_state(move, node["state"])
                children_states.append(new_state)

            for state in children_states:
                print("Any children...")
                if is_goal_state(state):
                    self.get_solution_path(node)
                    print("Solution found. Exiting")
                    break
                if closed_list:
                    for node in closed_list:
                        a1 = node["state"].get_board()
                        a2 = state.get_board()
                        if not np.array_equal(a1, a2):
                            child_node = {"state": state, "parent": node, "cost": node["cost"] + 1}
                            closed_list.append(child_node)
                            open_queue.append(child_node)
                else:
                    child_node = {"state": state, "parent": node, "cost": node["cost"] + 1}
                    closed_list.append(child_node)
                    open_queue.append(child_node)

    # def get_solution_path(node):
        # node = [state, parent node, cost
        # get the parent node and recursively call the function on that node to get its parent
        # if node parent is empty, return


    # def a_search(self):
    #
    #
    def greedy_best_first_search(self):
        visited = []
        pq = PriorityQueue()
        start = self.head_node
        pq.put((0, start))
        visited[start] = True

        while not pq.empty():
            current = pq.get()[1]
            parent = current[1]
            current = current[0]

            visited.insert(current, 0, parent)
            if current == is_goal_state():
                break
