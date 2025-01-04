from logger import MazeAction


def out(dim: tuple[int, int], log: list[MazeAction], filename="out.txt"):
    with open(filename, "w+") as file:
        file.write("DIM: " + str(dim) + "\n")
        file.write("\n".join(map(repr, log)))


from logger import LoggerGroup, StateLogger
from state import MazeState, MazeGeneratorFactory

s = LoggerGroup(StateLogger())
m = MazeState(5, 6, s)
MazeGeneratorFactory(m, 4).generate()
out((5, 6), s.log)
