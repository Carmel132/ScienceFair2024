from logger import MazeAction


def out(log: list[MazeAction], filename="out.txt"):
    with open(filename, "w+") as file:
        file.write("\n".join(map(repr, log)))


from logger import LoggerGroup, StateLogger
from state import MazeState, MazeGeneratorFactory

s = LoggerGroup(StateLogger())
m = MazeState(5, 5, s)
MazeGeneratorFactory(m, 1).generate()
out(s.log)
