class Search:
    def __init__(self, node, heuristic):
        self.node = node
        self.heuristic = heuristic

    def h1(self):

    def h2(self):

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
