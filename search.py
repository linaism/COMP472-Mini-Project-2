class Search:
    def __init__(self, node, heuristic):
        self.node = node
        self.heuristic = heuristic

    def h1(self):
        h_cost = 0
        for each car, check # cars blocking up, down, left, right
        when theres a car, h_cost += 1
        return cars with the h_cost added when arrive at the end of the board
        for car in self.get_cars:
            current_car = self.position
            if car.orientation == 0:  # horizontal
                # right
                for rows in current row:
                    if next car != self.car:
                        h_cost += 1
                        return get_cars.append(h_cost)
                # left
                for rows in current row[::-1]:
                    if next car != self.car:
                        h_cost += 1
                        return get_cars.append(h_cost)
            if car.orientation == 1:  # vertical
                # down
                for cols in current col:
                    if next car != self.car:
                        h_cost += 1
                        return get_cars.append(h_cost)
                # up
                for cols in current col[::-1]:
                    if next car != self.car:
                        h_cost += 1
                        return get_cars.append(h_cost)

    def h2(self):
        h_cost = 0
        for each car, check  # positions blocking up, down, left, right
        when next position is not empty, h_cost += 1
        return cars with the h_cost added when arrive at the end of the board
        for car in self.get_cars:
            current_car = self.position
            if car.orientation == 0:  # horizontal
                # right
                for rows in current row:
                    if next position != '.':
                        h_cost += 1
                        return get_cars.append(h_cost)
                # left
                for rows in current row[::-1]:
                    if next position != '.':
                        h_cost += 1
                        return get_cars.append(h_cost)
            if car.orientation == 1:  # vertical
                # down
                for cols in current col:
                    if next position != '.':
                        h_cost += 1
                        return get_cars.append(h_cost)
                # up
                for cols in current col[::-1]:
                    if next position != '.':
                        h_cost += 1
                        return get_cars.append(h_cost)

    def h3(self):

    def h4(self):

    def uniform_cost_search(self):
        closed_list = []
        queue = []  # Initialize a queue

        closed_list.append(self.node)
        queue.append(self.node)

        while queue:
            curr = queue.pop(0)
            print(curr, end=" ")

            children = self.node["state"].get_children()

            for child in children:
                if child not in closed_list:
                    closed_list.append(child)
                    queue.append(child)

    def a_search(self):


    def greedy_best_first_search(self):
        visited = []
        openQueue = [[(start, 0)]]
        closedQueue = []

        # while loop


