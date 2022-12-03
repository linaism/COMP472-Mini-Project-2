import numpy as np
import copy

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

    # def h1(self):
    #
    # def h2(self):
    #
    # def h3(self):
    #
    # def h4(self):

    def uniform_cost_search(self):
        closed_list = []
        open_queue = []

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

    # def a_search(self):
    #
    #
    # def greedy_best_first_search(self):
