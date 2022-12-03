class bestSearch:

    def __init__(self, node):
        self.node = node
        self.heuristic1 = []
        self.heuristic2 = []
        self.heuristic3 = []
        self.heuristic4 = []
        self.queue = []
        self.parent = []

    def h1(self):
        h_cost = 0
        # for each car, check # cars blocking up, down, left, right
        # when theres a car, h_cost += 1
        # return cars with the h_cost added when arrive at the end of the board
        for car in self.get_cars:
            current_car = self.position
            if car.orientation == 0:  # horizontal
                # right
                for rows in current row:
                    if next car != self.car:
                        h_cost += 1
                        return self.heuristic1.append(h_cost)
                # left
                for rows in current row[::-1]:
                    if next car != self.car:
                        h_cost += 1
                        return self.heuristic1.append(h_cost)
            if car.orientation == 1:  # vertical
                # down
                for cols in current col:
                    if next car != self.car:
                        h_cost += 1
                        return self.heuristic1.append(h_cost)
                # up
                for cols in current col[::-1]:
                    if next car != self.car:
                        h_cost += 1
                        return self.heuristic1.append(h_cost)

    def h2(self):
        h_cost = 0
        # for each car, check  # positions blocking up, down, left, right
        # when next position is not empty, h_cost += 1
        # return cars with the h_cost added when arrive at the end of the board
        for car in self.get_cars:
            current_car = self.position
            if car.orientation == 0:  # horizontal
                # right
                for rows in current row:
                    if next position != '.':
                        h_cost += 1
                        return self.heuristic2.append(h_cost)
                # left
                for rows in current row[::-1]:
                    if next position != '.':
                        h_cost += 1
                        return self.heuristic2.append(h_cost)
            if car.orientation == 1:  # vertical
                # down
                for cols in current col:
                    if next position != '.':
                        h_cost += 1
                        return self.heuristic2.append(h_cost)
                # up
                for cols in current col[::-1]:
                    if next position != '.':
                        h_cost += 1
                        return self.heuristic2.append(h_cost)

    def h3(self):

    def h4(self):

    def find_children(self):
        x = parent[0]
        y = parent[1]



    from queue import PriorityQueue


    def greedy_best_first_search(boardState, visited, ):
        pq = PriorityQueue()
        visited = []
        openQueue = [[(start, 0)]]
        closedQueue = []

        while not pq.empty():
            current = pq.h1_getMin()
            parent = current[1]
            current = current[0]

            visited.insert(current, 0, parent)
            if current == endState:
                break
            else: