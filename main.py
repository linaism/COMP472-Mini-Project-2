from car import Car
from game import Game
from boardstate import State


# i basically want to use the car dict as the board to modify and evaluate every time
# ultimately,  i'm using the car dict as the state
# maybe i should call it a state instead of a car? but it's a map between the car id and the car params
# cars works fine tbh
#
# so i have my initial cars positions
#
# then i want to generate all its children, and keep track of who the parent is
#
# now who are the children
#
# they could be cars as well
#
# but people were mentioning the cost of re-generating states which can be costly
#
# i can generate children by creating a priority queue (unnecessary in this case tho so let's just make it a queue)
# of all the moves
# ex: B.. wait
#
# ok so we have the board as a cars dict
# then we can make children that consist of moves
# then we can store these children in a queue if they are not already in the visited list
#     ***** how to verify visited at low cost
# then we can get the next item in the queue
# and create its children, store in queue, until the queue becomes empty
#
# that's how we get to the solution we want
#
# but then
#
# how do we get the solution
#
# basically once we make a child, we should keep track of the cost it took to get there
# and its parent
#
# that is the constitution of the node
#
# meaning that a node is a dict consisting of cars dict, parent node, and cumulative cost
#
# for the solution, we go back to the parent and its parent until we reach no parent

# open the sample file used

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

file = open('Sample/sample-input.txt')

# read the content of the file opened
content = file.readlines()

games = []
# fuel = {}
for line in content:
    if line[0] != '#' and line[0] != '\n':
        games.append(line.strip())

print(games)

game = Game(games[0])
board = game.get_board()
p = print_board(board)

cars = game.get_cars()
state = State(cars)
board2 = state.get_board()
p2 = print_board(board2)

print(p == p2)
# for line in filtered_content:
#     line_split = line.split()
#     p = line_split[0]
#
#     # get puzzle in array form
#     board = []
#     for i in range(0, 35, 6):
#         board.append(p[i:i + 6])
#     boards.append(board)



# THIS IS THE PUZZLE THAT WILL BE USED
# puzzle = filtered_content[0]
# board = get_board(filtered_content[0])
# fuel = get_fuel(filtered_content[0])
# print_board(board)


