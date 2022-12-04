from car import Car
from game import Game
from boardstate import BoardState


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


sample1 = "....B.....B...AAB....C.....CDD......"
sample2 = "B....CB....CAA...C....DD..E.....EFFF"

game = Game(games[5])
game.play()
# board = game.get_board()
# p = print_board(board)
#
# cars = game.get_cars()
# state = BoardState(cars)
# board2 = state.get_board()
# p2 = print_board(board2)

# s1 = state.get_board()
# s2 = state.get_board()
#
# print(s1 is s2)
# print((s1 == s2).all())

# children = state.get_children()
# for car, params in state.cars.items():
#     print(str(params.fuel), end=" ")

# print()
#
# print(children)
#
# print(p == p2)


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
