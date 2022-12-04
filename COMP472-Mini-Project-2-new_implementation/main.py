from car import Car
from game import Game
from boardstate import BoardState

file = open('sample-input.txt')
content = file.readlines()

puzzles = []
for line in content:
    if line[0] != '#' and line[0] != '\n':
        puzzles.append(line.strip())

game_id = 1
filename = "output_file.txt"
f = open(filename, "w")
f.write("Puzzle number" + "\t" + "Algorithm" + "\t" + "Heuristic" + "\t" + "Length of solution" + "\t")
f.write("Length of search path" + "\t" + "Execution time" + "\n")
f.close()
for puzzle in puzzles:
    game = Game(puzzle, game_id)
    game.play()
    game_id += 1


